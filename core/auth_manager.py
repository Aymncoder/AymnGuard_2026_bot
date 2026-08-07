# core/auth_manager.py
import logging
from typing import Dict, Any, Optional
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired
from pyrogram.raw.types.auth import SentCodeTypeSms, SentCodeTypeApp, SentCodeTypeCall

logger = logging.getLogger("SovereignAuthManager")

class SovereignAuthManager:
    """
    محرك المصادقة السيادي: يدير دورة حياة تسجيل الدخول (OTP & 2FA) 
    بشكل آمن، ويستخرج الجلسات المشفرة (Session Strings) مع تحديد ذكي لطريقة الإرسال.
    """
    
    # ذاكرة مؤقتة لحفظ الحسابات التي لا تزال قيد تسجيل الدخول
    _auth_sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    async def send_verification_code(cls, session_name: str, phone_number: str, api_id: int, api_hash: str) -> Dict[str, Any]:
        """الخطوة 1: الاتصال بخوادم تيليجرام وطلب كود التحقق (OTP) مع تحديد جهة الاستلام."""
        logger.info(f"🔑 [Auth Engine]: Requesting code for {phone_number} [{session_name}]")
        
        client = Client(session_name, api_id=api_id, api_hash=api_hash, in_memory=True)
        
        try:
            await client.connect()
            sent_code = await client.send_code(phone_number)
            
            # تحديد جهة استلام الكود (نظام مؤسسي شفاف)
            code_type = sent_code.type
            delivery_method = "غير معروف"
            
            if isinstance(code_type, SentCodeTypeSms):
                delivery_method = "رسالة نصية (SMS)"
            elif isinstance(code_type, SentCodeTypeApp):
                delivery_method = "تطبيق تيليجرام (App)"
            elif isinstance(code_type, SentCodeTypeCall):
                delivery_method = "مكالمة هاتفية (Call)"
            
            # حفظ الجلسة المؤقتة في الذاكرة حتى يدخل المستخدم الكود
            cls._auth_sessions[session_name] = {
                "client": client,
                "phone_number": phone_number,
                "phone_code_hash": sent_code.phone_code_hash,
                "api_id": api_id,
                "api_hash": api_hash
            }
            
            return {
                "status": "code_sent", 
                "session_name": session_name,
                "delivery_method": delivery_method,
                "is_new_account": isinstance(code_type, SentCodeTypeSms),
                "message": f"✅ تم إرسال كود التحقق بنجاح عبر {delivery_method} للرقم {phone_number}."
            }
        except Exception as e:
            await client.disconnect()
            logger.error(f"❌ [Auth Engine Error]: {str(e)}")
            return {"status": "error", "message": f"حدث خطأ أثناء إرسال الكود: {str(e)}"}

    @classmethod
    async def verify_code(cls, session_name: str, phone_code: str) -> Dict[str, Any]:
        """الخطوة 2: إرسال كود التحقق وتأكيد الدخول."""
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة أو انتهت صلاحيتها."}
            
        client: Client = auth_data["client"]
        logger.info(f"🔐 [Auth Engine]: Verifying OTP for {session_name}")

        try:
            await client.sign_in(auth_data["phone_number"], auth_data["phone_code_hash"], phone_code)
            session_string = await client.export_session_string()
            await client.disconnect()
            del cls._auth_sessions[session_name] 
            
            return {
                "status": "success", 
                "session_string": session_string, 
                "message": "✅ تم تسجيل الدخول بنجاح! تم استخراج مفتاح الجلسة السيادي."
            }
            
        except SessionPasswordNeeded:
            logger.warning(f"⚠️ [Auth Engine]: 2FA Password needed for {session_name}")
            return {"status": "2fa_required", "message": "⚠️ الحساب محمي بكلمة مرور (2FA). يرجى إرسال كلمة المرور."}
            
        except (PhoneCodeInvalid, PhoneCodeExpired) as e:
            return {"status": "error", "message": "❌ الكود غير صحيح أو منتهي الصلاحية."}
        except Exception as e:
            return {"status": "error", "message": f"❌ فشل تسجيل الدخول: {str(e)}"}

    @classmethod
    async def verify_2fa_password(cls, session_name: str, password: str) -> Dict[str, Any]:
        """الخطوة 3: إدخال كلمة المرور (2FA)."""
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة."}
            
        client: Client = auth_data["client"]
        logger.info(f"🗝️ [Auth Engine]: Verifying 2FA for {session_name}")

        try:
            await client.check_password(password)
            session_string = await client.export_session_string()
            await client.disconnect()
            del cls._auth_sessions[session_name]
            
            return {
                "status": "success", 
                "session_string": session_string, 
                "message": "✅ تم تخطي حماية 2FA وتسجيل الدخول بنجاح!"
            }
        except Exception as e:
            return {"status": "error", "message": f"❌ كلمة المرور خاطئة أو حدث خطأ: {str(e)}"}
