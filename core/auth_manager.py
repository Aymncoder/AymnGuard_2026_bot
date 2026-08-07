# core/auth_manager.py
import logging
from typing import Dict, Any, Optional
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

logger = logging.getLogger("SovereignAuthManager")

class SovereignAuthManager:
    """
    محرك المصادقة السيادي: يدير دورة حياة تسجيل الدخول (OTP & 2FA) 
    بشكل آمن، ويستخرج الجلسات المشفرة (Session Strings) لاستخدامها لاحقاً.
    """
    
    # ذاكرة مؤقتة لحفظ الحسابات التي لا تزال قيد قيد تسجيل الدخول
    _auth_sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    async def send_verification_code(cls, session_name: str, phone_number: str, api_id: int, api_hash: str) -> Dict[str, Any]:
        """الخطوة 1: الاتصال بخوادم تيليجرام وطلب كود التحقق (OTP)."""
        logger.info(f"🔑 [Auth Engine]: Requesting code for {phone_number} [{session_name}]")
        
        # إنشاء جلسة في الذاكرة العشوائية لتجنب قفل الملفات (File Locking)
        client = Client(session_name, api_id=api_id, api_hash=api_hash, in_memory=True)
        
        try:
            await client.connect()
            sent_code = await client.send_code(phone_number)
            
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
                "message": f"✅ تم إرسال كود التحقق بنجاح إلى الرقم {phone_number} عبر تيليجرام."
            }
        except Exception as e:
            await client.disconnect()
            logger.error(f"❌ [Auth Engine Error]: {str(e)}")
            return {"status": "error", "message": f"حدث خطأ أثناء إرسال الكود: {str(e)}"}

    @classmethod
    async def verify_code(cls, session_name: str, phone_code: str) -> Dict[str, Any]:
        """الخطوة 2: إرسال كود التحقق الذي أدخله المستخدم وتأكيد الدخول."""
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة أو انتهت صلاحيتها. يرجى طلب الكود مجدداً."}
            
        client: Client = auth_data["client"]
        logger.info(f"🔐 [Auth Engine]: Verifying OTP for {session_name}")

        try:
            # محاولة تسجيل الدخول بالكود
            await client.sign_in(auth_data["phone_number"], auth_data["phone_code_hash"], phone_code)
            
            # استخراج مفتاح الجلسة المشفر (Session String)
            session_string = await client.export_session_string()
            await client.disconnect()
            del cls._auth_sessions[session_name] # تنظيف الذاكرة
            
            return {
                "status": "success", 
                "session_string": session_string, 
                "message": "✅ تم تسجيل الدخول بنجاح! تم استخراج مفتاح الجلسة السيادي."
            }
            
        except SessionPasswordNeeded:
            # إذا كان الحساب محمياً بخطوتين (2FA)
            logger.warning(f"⚠️ [Auth Engine]: 2FA Password needed for {session_name}")
            return {"status": "2fa_required", "message": "⚠️ الحساب محمي بكلمة مرور (التحقق بخطوتين). يرجى إرسال كلمة المرور."}
            
        except (PhoneCodeInvalid, PhoneCodeExpired) as e:
            return {"status": "error", "message": "❌ الكود غير صحيح أو منتهي الصلاحية."}
        except Exception as e:
            return {"status": "error", "message": f"❌ فشل تسجيل الدخول: {str(e)}"}

    @classmethod
    async def verify_2fa_password(cls, session_name: str, password: str) -> Dict[str, Any]:
        """الخطوة 3 (اختياري): إدخال كلمة المرور (2FA) إذا كان الحساب محمياً."""
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة."}
            
        client: Client = auth_data["client"]
        logger.info(f"🗝️ [Auth Engine]: Verifying 2FA for {session_name}")

        try:
            # فك تشفير 2FA
            await client.check_password(password)
            
            # استخراج الجلسة بعد تخطي 2FA
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
