# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Standalone Telegram Protection Bot Runner (v18.0.0)
==============================================================================
مشغل بوت الحماية المستقل لتيليجرام: يعمل كـ Adapter خارجي يتلقى الأحداث
ويوجهها حصرياً إلى ميكروسيرفس الحماية عبر الممر المركزي (SovereignPlatformHub)
دون أي تداخل أو تشابك مع النواة أو باقي الخدمات.
"""

import logging
import asyncio
from typing import Dict, Any
from core.sovereign_platform_hub import SovereignPlatformHub

logger = logging.getLogger("AegisAICore.TelegramProtectionRunner")
logger.setLevel(logging.INFO)

class TelegramProtectionRunner:
    """
    مشغل بوت الحماية المستقل: مسؤول عن الاستماع لأحداث تيليجرام وتمريرها 
    للميكروسيرفس المعزول وتنفيذ العقوبات السيادية فوراً.
    """

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        logger.info("🛡️ [Telegram Protection Runner]: جاري تهيئة مشغل بوت الحماية المستقل...")

    async def handle_incoming_telegram_update(self, update_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        معالجة وتوجيه تحديث تيليجرام الوارد:
        1. استخلاص بيانات الرسالة أو العضو الجديد.
        2. إرسالها لميكروسيرفس الحماية عبر SovereignPlatformHub.
        3. تطبيق الإجراء الفوري (حذف، كتم، حظر، أو إغلاق مؤقت).
        """
        message = update_payload.get("message", {}) or update_payload.get("edited_message", {})
        chat_info = message.get("chat", {})
        chat_id = chat_info.get("id", 0)
        
        user_info = message.get("from", {})
        user_id = user_info.get("id", 0)
        
        # 1. فحص أحداث الانضمام أو هجمات الـ Raid
        if "new_chat_members" in message:
            for member in message.get("new_chat_members", []):
                member_id = member.get("id", 0)
                logger.info(f"👥 [Raid Watcher]: رصد انضمام العضو {member_id} في الشات {chat_id}")
                
                raid_payload = {
                    "event_type": "evaluate_raid",
                    "new_member_id": member_id,
                    "chat_id": chat_id
                }
                
                raid_res = await SovereignPlatformHub.dispatch_request_to_service(
                    service_id="sovereign_protection_bot",
                    payload=raid_payload
                )
                
                result_data = raid_res.get("result", {})
                if result_data.get("emergency_status") == "LOCKDOWN_ACTIVE":
                    logger.critical(f"🛑 [LOCKDOWN ENFORCED]: تم تفعيل الطوارئ في الشات {chat_id} بسبب هجوم Raid.")
                    return {
                        "status": "lockdown_triggered",
                        "action": "restrict_new_joins",
                        "chat_id": chat_id
                    }

        # 2. فحص الرسائل النصية والروابط الخبيثة والبلاغات الكيدية
        text_content = message.get("text", "") or message.get("caption", "")
        if text_content or "new_chat_members" in message or "left_chat_member" in message:
            
            inspection_payload = {
                "event_type": "inspect_message",
                "message_payload": message
            }
            
            # التوجيه الآمن عبر الممر المركزي للميكروسيرفس
            service_response = await SovereignPlatformHub.dispatch_request_to_service(
                service_id="sovereign_protection_bot",
                payload=inspection_payload
            )
            
            action_result = service_response.get("result", {})
            action_taken = action_result.get("action_taken", "allow")
            
            if action_taken != "allow":
                logger.warning(f"🚨 [Protection Action Enforced]: إجراء '{action_taken}' ضد الكيان {user_id} في الشات {chat_id}")
                return {
                    "status": "action_required",
                    "chat_id": chat_id,
                    "message_id": message.get("message_id"),
                    "action": action_taken,
                    "reason": action_result.get("reason"),
                    "feedback_message": action_result.get("message")
                }

        return {
            "status": "clean",
            "action": "allow"
        }

    async def start_polling_simulation(self):
        """حلقة التشغيل المستقلة للمشغل (Standalone Polling Loop)."""
        logger.info("🚀 [Protection Runner]: مشغل بوت الحماية يعمل الآن بشكل مستقل ومؤمن تماماً.")
