# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Auth Manager (v18.0.0-Master Enterprise Unified)
==============================================================================
محرك المصادقة السيادي الموحد: إدارة دورة حياة تسجيل الدخول (OTP & 2FA) 
بشكل آمن، معالجة استباقية للأخطاء، تحديد دقيق لجهات الاستلام، وتصدير Session Strings.
"""

import logging
from typing import Dict, Any, Optional
from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded, 
    PhoneCodeInvalid, 
    PhoneCodeExpired, 
    FloodWait, 
    BadRequest
)
from pyrogram.raw.types.auth import SentCodeTypeSms, SentCodeTypeApp, SentCodeTypeCall

logger = logging.getLogger("SovereignAuthManager")

class SovereignAuthManager:
    """
    المدير السيادي للمصادقة: نظام مؤسسي متكامل يدير تدفقات المصادقة المؤقتة،
    يمنع تسريب الاتصالات، ويدعم استخراج سلاسل الجلسات المشفرة للخزنة الأبدية.
    """
    
    # سجل مركزي موحد وآمن لبيانات المصادقة المؤقتة قيد التنفيذ
    _auth_sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    async def send_verification_code(
        cls, 
        session_name: str, 
        phone_number: str, 
        api_id: int, 
        api_hash: str
    ) -> Dict[str, Any]:
        """الخطوة الأولى: الاتصال بخوادم تيليجرام وطلب كود التحقق (OTP) مع تحديد جهة الاستلام بدقة."""
        logger.info(f"🔑 [Auth Engine]: Requesting verification code for phone: {phone_number} [Session: {session_name}]")
        
        # تنظيف أي جلسة سلقة معلقة بنفس الاسم لضمان عدم تداخل البيانات
        await cls._safe_cleanup_session(session_name)
        
        client = Client(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True
        )
        
        try:
            await client.connect()
            sent_code = await client.send_code(phone_number)
            
            # تحليل ذكي لجهة استلام كود التحقق
            code_type = sent_code.type
            delivery_method = "غير معروف"
            
            if isinstance(code_type, SentCodeTypeSms):
                delivery_method = "رسالة نصية (SMS)"
            elif isinstance(code_type, SentCodeTypeApp):
                delivery_method = "تطبيق تيليجرام الرسمي (App)"
            elif isinstance(code_type, SentCodeTypeCall):
                delivery_method = "مكالمة هاتفية (Call)"
            
            # تخزين البيانات في السجل المركزي الموحد
            cls._auth_sessions[session_name] = {
                "client": client,
                "phone_number": phone_number,
                "phone_code_hash": sent_code.phone_code_hash,
                "api_id": api_id,
                "api_hash": api_hash
            }
            
            logger.info(f"✅ [Auth Engine]: Code sent successfully via {delivery_method} for session '{session_name}'")
            return {
                "status": "code_sent", 
                "session_name": session_name,
                "delivery_method": delivery_method,
                "is_new_account": isinstance(code_type, SentCodeTypeSms),
                "message": f"✅ تم إرسال كود التحقق بنجاح عبر {delivery_method} للرقم {phone_number}."
            }
            
        except FloodWait as e:
            await cls._safe_disconnect_client(client)
            logger.error(f"🛑 [Auth FloodWait]: Must wait {e.value} seconds for session '{session_name}'.")
            return {"status": "error", "message": f"🛑 تجاوزت الحد المسموح من المحاولات. يجِب الانتظار لمدة {e.value} ثانية."}
            
        except Exception as e:
            await cls._safe_disconnect_client(client)
            logger.error(f"❌ [Auth Engine Error]: Failed to send code for '{session_name}': {str(e)}")
            return {"status": "error", "message": f"❌ حدث خطأ تقني أثناء إرسال الكود: {str(e)}"}

    @classmethod
    async def verify_code(
        cls, 
        session_name: str, 
        phone_code: str
    ) -> Dict[str, Any]:
        """الخطوة الثانية: استقبال كود الـ OTP، إتمام تسجيل الدخول، واستخراج مفتاح الجلسة (Session String)."""
        logger.info(f"🔐 [Auth Engine]: Verifying OTP code for session: {session_name}")
        
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة، انتهت صلاحيتها، أو لم يتم طلب كود مسبقاً."}
            
        client: Client = auth_data["client"]
        phone_number = auth_data["phone_number"]
        phone_code_hash = auth_data["phone_code_hash"]

        try:
            await client.sign_in(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                phone_code=phone_code.strip()
            )
            
            # استخراج كنز الجلسة المشفر النهائي
            session_string = await client.export_session_string()
            await cls._safe_disconnect_client(client)
            cls._auth_sessions.pop(session_name, None)
            
            logger.info(f"🎉 [Auth Success]: Session '{session_name}' successfully authenticated & string exported.")
            return {
                "status": "success", 
                "session_name": session_name,
                "session_string": session_string, 
                "message": "✅ تم تسجيل الدخول بنجاح! تم استخراج مفتاح الجلسة السيادي وتأمينه."
            }
            
        except SessionPasswordNeeded:
            logger.warning(f"⚠️ [Auth 2FA Required]: Session '{session_name}' requires Two-Step Verification password.")
            return {
                "status": "2fa_required", 
                "session_name": session_name,
                "message": "⚠️ الحساب محمي بكلمة مرور التحقق بخطوتين (2FA). يرجى إرسال كلمة المرور."
            }
            
        except (PhoneCodeInvalid, PhoneCodeExpired, BadRequest) as e:
            logger.warning(f"⚠️ [Auth Invalid Code]: Code error for session '{session_name}': {str(e)}")
            return {"status": "error", "message": "❌ كود التحقق غير صحيح، منتهي الصلاحية، أو تم إدخاله بشكل خاطئ."}
            
        except Exception as e:
            logger.error(f"❌ [Auth Verification Error]: Unexpected exception for '{session_name}': {str(e)}")
            return {"status": "error", "message": f"❌ فشل تسجيل الدخول بسبب خطأ غير متوقع: {str(e)}"}

    @classmethod
    async def verify_2fa_password(
        cls, 
        session_name: str, 
        password: str
    ) -> Dict[str, Any]:
        """الخطوة الثالثة: إدخال وتأكيد كلمة مرور التحقق بخطوتين (2FA) وتصدير الجلسة النهائية."""
        logger.info(f"🗝️ [Auth Engine]: Verifying 2FA password for session: {session_name}")
        
        auth_data = cls._auth_sessions.get(session_name)
        if not auth_data:
            return {"status": "error", "message": "❌ الجلسة غير موجودة أو انتهت صلاحية بيانات المصادقة المؤقتة."}
            
        client: Client = auth_data["client"]

        try:
            await client.check_password(password.strip())
            
            session_string = await client.export_session_string()
            await cls._safe_disconnect_client(client)
            cls._auth_sessions.pop(session_name, None)
            
            logger.info(f"🎉 [Auth 2FA Success]: Session '{session_name}' authenticated via 2FA and string exported.")
            return {
                "status": "success", 
                "session_name": session_name,
                "session_string": session_string, 
                "message": "✅ تم تخطي حماية 2FA وتوليد سلسلة الجلسة السيادية بنجاح تام!"
            }
            
        except Exception as e:
            logger.error(f"❌ [Auth 2FA Error]: Invalid password or connection issue for '{session_name}': {str(e)}")
            return {"status": "error", "message": f"❌ كلمة مرور التحقق بخطوتين غير صحيحة أو حدث خطأ تقني: {str(e)}"}

    @classmethod
    async def _safe_disconnect_client(cls, client: Optional[Client]):
        """دالة مساعدة لإغلاق اتصال العميل بشكل آمن ودون رمي استثناءات."""
        if client:
            try:
                if client.is_connected:
                    await client.disconnect()
            except Exception as e:
                logger.debug(f"ℹ️ [Cleanup Notice]: Error while disconnecting temp client: {e}")

    @classmethod
    async def _safe_cleanup_session(cls, session_name: str):
        """تنظيف شامل وآمن لأي جلسة مؤقتة سابقة في الذاكرة."""
        existing = cls._auth_sessions.pop(session_name, None)
        if existing and "client" in existing:
            await cls._safe_disconnect_client(existing["client"])
