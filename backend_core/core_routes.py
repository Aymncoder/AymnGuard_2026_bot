# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Core Routes (Communication Bridge)
==============================================================================
جسر التواصل والمسارات: الطبقة المسؤولة عن استقبال الطلبات الخارجية 
(مثل واجهات الويب، تطبيقات الهاتف، أو Webhooks) 
وتوجيهها إلى المحرك العصبي أو وسيط المهام دون التكدس في ملف التشغيل الرئيسي.
مصمم بنمط (APIRouter) لعزل المسارات برمجياً.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

# استيراد الوحدات السيادية التي قمنا ببنائها (بافتراض وضعها في نفس مسار الحزمة)
from .context_vault import ContextVault
from .task_broker import broker

# إعداد مسجل الأحداث
logger = logging.getLogger("AymnGuard.CoreRoutes")

# إنشاء الموجه المستقل (Router) لمنع تداخل المسارات مستقبلاً في main.py
router = APIRouter(prefix="/v5/api", tags=["Sovereign Gateway"])

@router.get("/health")
async def system_health_check() -> Dict[str, str]:
    """
    نبض النظام (Health Check): نقطة فحص سريعة للتأكد من استقرار الخوادم 
    وعمل وسيط المهام. مفيدة جداً للمراقبة المستمرة.
    """
    return {
        "system": "AymnGuard v5.0",
        "status": "Online and Fully Operational",
        "broker_active": str(broker._is_running)
    }

@router.post("/process-command")
async def process_external_command(user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    نقطة الاستقبال الذكية للأوامر المعقدة:
    - تسترجع سياق المستخدم من خزنة الذاكرة لحظياً.
    - تحيل العملية الثقيلة إلى وسيط المهام في الخلفية.
    - ترد فوراً على المستخدم لضمان سرعة الاستجابة (Zero-Lag Experience).
    """
    try:
        # 1. التفاعل مع الذاكرة السياقية (Context Vault)
        context = await ContextVault.retrieve_context(user_id)
        if not context:
            # بدء جلسة جديدة آمنة
            await ContextVault.store_context(user_id, {"last_action": "command_received"})
            logger.info(f"🆕 [Core Routes]: Secure session initiated for user: {user_id}")
        else:
            logger.debug(f"🔄 [Core Routes]: Existing secure context retrieved for user: {user_id}")

        # 2. تعريف مهمة معالجة داخلية (سيتم ربطها بالمحرك العصبي لاحقاً)
        async def cognitive_processing_task(uid: str, data: dict):
            import asyncio
            # محاكاة لعملية تحليل ثقيلة تستغرق وقتاً
            await asyncio.sleep(1)  
            logger.info(f"🧠 [Background Engine]: Successfully processed payload for {uid}")

        # 3. توجيه المهمة المعقدة إلى الخلفية (Task Broker)
        await broker.submit_task(cognitive_processing_task, user_id, payload)

        # 4. الاستجابة الفورية والسريعة للمستخدم أو التطبيق الخارجي
        return {
            "status": "success",
            "message": "Payload securely received and dispatched to background queue.",
            "user_id": user_id,
            "security_layer": "AymnGuard Active"
        }

    except Exception as e:
        logger.error(f"❌ [Core Routes]: Critical routing error -> {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Sovereign Gateway Error")

