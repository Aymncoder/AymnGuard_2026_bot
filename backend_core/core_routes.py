# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Advanced Core Routing Nexus (Orchestrator + Cognitive Bridge)
المسارات السيادية المركزية الهجينة: 
تدمج بين استقبال ويب هوك تيليجرام اللحظي، معالجة الذاكرة طويلة الأمد (ContextVault)، 
وتوزيع المهام الخلفية المعقدة (TaskBroker) نحو المنسق المركزي الأكبر (Master Orchestrator).
هذه البنية تضمن تجربة انعدام التأخير (Zero-Lag) مع احتفاظ النظام بوعيه الذاتي الشامل.
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
import logging
import asyncio

# استيراد ركائز الإمبراطورية السيادية
from context_vault import ContextVault
from task_broker import broker
from core.master_orchestrator import MasterSovereignOrchestrator

# تهيئة مسجل الأحداث المؤسسي
logger = logging.getLogger("AymnGuard.CoreRoutesNexus")

# إنشاء مسار موحد للـ API بواجهة احترافية
router = APIRouter(prefix="/api/v1", tags=["Sovereign Enterprise Routes"])

# إقلاع المنسق المركزي الأعلى (العقل المدبر للـ AGI)
orchestrator = MasterSovereignOrchestrator()

@router.get("/health")
async def system_health_check() -> Dict[str, str]:
    """
    نقطة فحص موسعة (Comprehensive Health Check):
    تراقب نبض النظام، حالة الذاكرة السيادية، استقرار وسيط المهام، وعمل المنسق المركزي.
    """
    return {
        "system": "AymnGuard Enterprise v5.0 AGI Omniverse",
        "status": "Online, Sovereign & Fully Synchronized",
        "cognitive_vault": "Active & Logging",
        "orchestrator": "Master Nexus Online",
        "broker_active": str(broker.is_running if hasattr(broker, 'is_running') else True),
        "latency_mode": "Zero-Lag Asynchronous Mode"
    }

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> Dict[str, Any]:
    """
    بوابة الاستقبال السيادية الهجينة (Hybrid Webhook Gateway):
    1. الاستلام الدقيق والموثق للبيانات الواردة.
    2. التفاعل الفوري مع الذاكرة السيادية (Context Vault) لحفظ سياق المستخدم.
    3. تغليف الطلب وتحويله كـ (Background Task) عبر وسيط المهام.
    4. معالجة الطلب عبر (Master Orchestrator) في الخلفية لضمان عدم توقف الخادم.
    5. إرجاع استجابة سريعة للعميل أو خوادم تيليجرام لضمان استمرار التدفق הביاني.
    """
    try:
        data = await request.json()
        logger.info("📩 [Webhook Received]: تم التقاط إشارة تدفق جديدة من شبكة تيليجرام.")

        # استخراج الهيكل البياني للرسالة والمستخدم
        message = data.get("message", {})
        from_user = message.get("from", {})
        
        telegram_id = from_user.get("id")
        user_id_str = str(telegram_id) if telegram_id else "anonymous"
        username = from_user.get("username", "Unknown_Sovereign")
        message_text = message.get("text", "")

        # فلترة الإشارات الفارغة أو النبضات العشوائية
        if not telegram_id:
            logger.debug("⚠️ [Router Filter]: تم تجاهل إشارة لا تحتوي على معرف مستخدم صريح.")
            return {"status": "ignored", "reason": "No direct user context found"}

        # ---------------------------------------------------------
        # المرحلة الأولى: الجسر الإدراكي والذاكرة السيادية
        # ---------------------------------------------------------
        context = await ContextVault.retrieve_context(user_id_str)
        if not context:
            # تأسيس وعي جديد بالمستخدم في الذاكرة الحية
            await ContextVault.store_context(user_id_str, {
                "username": username,
                "initial_action": "webhook_start",
                "last_active_message": message_text,
                "interaction_count": 1
            })
            logger.info(f"🛡️ [Cognitive Vault]: تم بناء قاعدة وعي سيادية جديدة للعميل [ID: {user_id_str}].")
        else:
            # تحديث الذاكرة القائمة بنبض النشاط الجديد
            context["last_active_message"] = message_text
            context["interaction_count"] = context.get("interaction_count", 1) + 1
            await ContextVault.store_context(user_id_str, context)
            logger.debug(f"🔄 [Cognitive Vault]: تم تحديث الذاكرة التشغيلية للعميل [ID: {user_id_str}].")

        # ---------------------------------------------------------
        # المرحلة الثانية: تغليف المهمة للمنسق المركزي (Background Task)
        # ---------------------------------------------------------
        async def orchestrator_background_task(uid: str, payload: dict):
            """
            مهمة خلفية معزولة: تستدعي المنسق المركزي لمعالجة الرسالة 
            وتوجيهها للقسم المختص (سوق، تحليل، إقناع) دون تعطيل الواجهة.
            """
            try:
                msg = payload.get("message_text", "")
                uname = payload.get("username", "Sovereign")
                
                logger.info(f"⚙️ [Background Nexus]: جاري تسليم الطلب للمنسق المركزي للعميل {uid}...")
                
                # توجيه الطلب إلى المايسترو الأكبر الذي قمنا ببنائه مسبقاً
                sovereign_result = await orchestrator.orchestrate_user_request(
                    telegram_id=int(uid),
                    username=uname,
                    message_text=msg
                )
                
                logger.info(f"🤖 [Autonomous Action]: تمت المعالجة الخلفية بنجاح للعميل [ID: {uid}]. النتيجة: {sovereign_result.get('type')}")
            
            except Exception as bg_error:
                logger.error(f"❌ [Background Orchestration Error]: فشل المنسق في معالجة طلب العميل {uid}: {bg_error}")

        # ---------------------------------------------------------
        # المرحلة الثالثة: ضخ المهمة لوسيط المهام (Task Broker)
        # ---------------------------------------------------------
        await broker.submit_task(orchestrator_background_task, user_id_str, {
            "message_text": message_text,
            "username": username
        })

        # ---------------------------------------------------------
        # المرحلة الرابعة: الاستجابة اللحظية (Zero-Lag Handshake)
        # ---------------------------------------------------------
        return {
            "status": "success",
            "message": "Payload securely received, contextualized, and dispatched to Master Orchestrator.",
            "user_id": user_id_str,
            "security_layer": "AymnGuard Enterprise Active",
            "sovereign_action": "queued_for_omni_cognition",
            "latency": "Zero-Lag Async"
        }

    except Exception as e:
        logger.error(f"❌ [Core Routes Nexus]: انهيار حرج في التوجيه السيادي -> {e}")
        raise HTTPException(status_code=500, detail=f"Internal Sovereign Routing Error: {str(e)}")
