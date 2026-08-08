# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Protection Microservice Adapter (v18.0.0)
==============================================================================
مهايئ ميكروسيرفس الحماية المستقل: يغلف درع الحماية السيبراني ويسجله كخدمة 
مستقلة داخل المأوى المركزي (SovereignPlatformHub) دون أي تداخل برمجي.
"""

import logging
from typing import Dict, Any
from security.protection_bot import SovereignProtectionEngine
from core.sovereign_platform_hub import SovereignPlatformHub

logger = logging.getLogger("AegisAICore.ProtectionMicroserviceAdapter")
logger.setLevel(logging.INFO)

async def protection_service_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    معالج الخدمة المستقل: يستقبل حمولة الرسالة أو العضو الجديد،
    يوجهها حصرياً لمحرك الدفاع السيادي، ويعيد نتيجة الفحص والعقوبة.
    """
    event_type = payload.get("event_type", "message")
    
    if event_type == "inspect_message":
        message_data = payload.get("message_payload", {})
        inspection_result = await SovereignProtectionEngine.inspect_incoming_message(message_data)
        return {
            "service": "cyber_defense_protection",
            "action_taken": inspection_result.get("action"),
            "reason": inspection_result.get("reason"),
            "message": inspection_result.get("message")
        }
        
    elif event_type == "evaluate_raid":
        member_id = payload.get("new_member_id", 0)
        chat_id = payload.get("chat_id", 0)
        raid_result = await SovereignProtectionEngine.evaluate_raid_attempt(member_id, chat_id)
        return {
            "service": "anti_raid_shield",
            "emergency_status": raid_result.get("emergency_status"),
            "action": raid_result.get("action"),
            "message": raid_result.get("message")
        }
        
    return {
        "status": "error",
        "message": "نوع الحدث غير معروف في ميكروسيرفس الحماية."
    }

# تسجيل الميكروسيرفس تلقائياً فور تحميل الملف في المنصة المستقلة
SovereignPlatformHub.register_service(
    service_id="sovereign_protection_bot",
    service_name="Enterprise Cyber Defense & Protection Microservice",
    handler_func=protection_service_handler,
    metadata={
        "version": "18.0.0",
        "isolation_level": "absolute",
        "capabilities": ["anti_flood", "anti_raid", "scam_filter", "admin_immunity"]
    }
)

logger.info("🛡️ [Protection Microservice]: تم عزل وتسجيل بوت الحماية بنجاح كخدمة مستقلة داخل النواة الأم.")
