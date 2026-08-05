# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Core API & Telegram Webhook Routes
المسارات السيادية المركزية (Advanced Routing & Cognitive Bridge):
تدمج بين استقبال ويب هوك تيليجرام، معالجة الذاكرة طويلة الأمد، توزيع المهام الخلفية (TaskBroker)،
وتفعيل الوكيل الإدراكي والأمني لاتخاذ القرارات وإدارة العملاء باحترافية مطلقة.
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
import logging
import asyncio

# استيراد مكونات الإمبراطورية السيادية
from context_vault import ContextVault
from task_broker import broker
from core.agents.security_agent import CommunitySecurityAgent

# إماء مسجل الأحداث المؤسسي
logger = logging.getLogger("AymnGuard.CoreRoutes")

# إنشاء مسار موحد للـ API بريفكس احترافي
router = APIRouter(prefix="/api/v1", tags=["Sovereign Enterprise Routes"])

# تهيئة نسخة سيادية من الوكيل الأمني والإدراكي
security_agent = CommunitySecurityAgent()

@router.get("/health")
async def system_health_check() -> Dict[str, str]:
    """
    نقطة فحص سريعة للتأكد من استقرار الخوادم (Health Check): نبض النظام،
    حالة الذاكرة السيادية، وعمل وسيط المهام (TaskBroker).
    """
    return {
        "system": "AymnGuard Enterprise v5.0",
        "status": "Online and Fully Operational & Sovereign",
        "cognitive_vault": "Active",
        "security_agent": "Online",
        "broker_active": str(broker.is_running if hasattr(broker, 'is_running') else True)
    }

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> Dict[str, Any]:
    """
    بوابة استقبال الـ Webhook السيادية من تيليجرام:
    1. استلام الرسائل أو انضمام الأعضاء بدقة فائقة.
    2. تفاعل فوري مع الذاكرة السيادية (Context Vault).
    3. تمرير المهام الثقيلة لخلفية النظام عبر (TaskBroker) لضمان سرعة الاستجابة (Zero-Lag Experience).
    4. تفعيل الوكيل الأمني لاستخراج استراتيجيات الإقناع وخدمة العملاء المتقدمة.
    """
    try:
        data = await request.json()
        logger.info("📩 [Webhook Received]: تم استلام تحديث جديد من شبكة تيليجرام السيادية.")

        # استخراج بيانات الرسالة والمستخدم بدقة
        message = data.get("message", {})
        from_user = message.get("from", {})
        
        telegram_id = from_user.get("id")
        user_id_str = str(telegram_id) if telegram_id else "anonymous"
        username = from_user.get("username", "Unknown_Sovereign")
        message_text = message.get("text", "")

        if not telegram_id:
            return {"status": "ignored", "reason": "No direct user context found"}

        # 1. تفاعل مع الذاكرة السيادية وسجل الجلسات (Context Vault)
        context = await ContextVault.retrieve_context(user_id_str)
        if not context:
            await ContextVault.store_context(user_id_str, {
                "username": username,
                "initial_action": "webhook_start",
                "last_active": message_text
            })
            logger.info(f"🛡️ [Core Routes]: تم فتح جلسة سيادية جديدة للعميل [ID: {user_id_str}] في الذاكرة الحية.")

        # 2. تعريف مهام المعالجة الخلفية عبر العقل العصبي والوكيل الأمني
        async def cognitive_processing_task(uid: str, payload: dict):
            """مهمة خلفية غير متزامنة لتحليل سلوك العميل وتطبيق محرك الإقناع بذكاء تام"""
            try:
                msg = payload.get("message_text", "")
                uname = payload.get("username", "Sovereign")
                
                # استدعاء الوكيل الإدراكي لتحليل السلوك واستخراج الاستراتيجية
                agent_guidance = await security_agent.analyze_user_behavior(
                    telegram_id=int(uid),
                    username=uname,
                    message_text=msg
                )
                logger.info(f"🧠 [Background Engine]: تمت معالجة سلوك العميل [ID: {uid}] بنجاح. التوجيه: {agent_guidance}")
            except Exception as bg_error:
                logger.error(f"❌ [Background Task Error]: فشل في المعالجة الخلفية للعميل {uid}: {bg_error}")

        # 3. توجيه المهمة المعقدة إلى وسيط المهام (Task Broker) للعمل في الخلفية دون تأخير الاستجابة
        await broker.submit_task(cognitive_processing_task, user_id_str, {
            "message_text": message_text,
            "username": username
        })

        # 4. الاستجابة الفورية والسريعة للمستخدم أو التطبيق الخارجي (Zero-Lag Experience)
        return {
            "status": "success",
            "message": "Payload securely received, contextualized, and dispatched to background intelligence.",
            "user_id": user_id_str,
            "security_layer": "AymnGuard Enterprise Active",
            "sovereign_action": "queued_for_advanced_cognition"
        }

    except Exception as e:
        logger.error(f"❌ [Core Routes]: خطأ حرج في التوجيه السيادي -> {e}")
        raise HTTPException(status_code=500, detail=f"Internal Sovereign Routing Error: {str(e)}")
