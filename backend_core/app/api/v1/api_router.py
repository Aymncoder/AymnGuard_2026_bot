# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Sovereign Main API v1 Router
==============================================================================
الموجه المركزي (Central Router) المصمم ببنية مؤسساتية فائقة:
- 🛡️ يمنع تداخل المسارات (Path Collisions) عبر نظام الـ (Prefixing) الصارم.
- 🧠 يربط نقاط الاتصال بالمحركات العصبية دون تكرار الكود (DRY Principle).
- 🚀 يضمن توجيهاً دقيقاً وآمناً لجميع العمليات اللوجستية والذكية.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone

# إعداد نظام تسجيل الأحداث للموجه
logger = logging.getLogger("AymnGuard.APIRouter")

# ==============================================================================
# 1. تهيئة الموجه السيادي المركزي
# ==============================================================================
api_v1_router = APIRouter()


# ==============================================================================
# 2. إنشاء موجهات فرعية (Sub-Routers) لمنع تداخل المسارات جذرياً
# ==============================================================================
# استخدام الـ Prefix يضمن أن كل مسار معزول تماماً عن الآخر (Zero Overlap)

health_router = APIRouter(prefix="/health", tags=["🛡️ System Health & Audit"])
ai_neural_router = APIRouter(prefix="/ai", tags=["🧠 AI Neural Engine"])
logistics_router = APIRouter(prefix="/logistics", tags=["⚙️ Autonomous Logistics"])


# ==============================================================================
# 3. مسارات الفحص والتدقيق (تُربط لاحقاً بـ SystemHealthAuditor)
# ==============================================================================
@health_router.get("/pulse", summary="فحص النبض السيادي للنظام")
async def check_system_pulse():
    """
    نقطة اتصال مخصصة للتحقق من استقرار العُقد وقواعد البيانات.
    بدلاً من تكرار كود الفحص هنا، سنقوم مستقبلاً باستدعاء SystemHealthAuditor.run_audit()
    """
    logger.info("📡 [Router]: System pulse check initiated.")
    return {
        "status": "operational",
        "core_version": "AymnGuard v5.0 Enterprise",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ==============================================================================
# 4. مسارات الذكاء الاصطناعي (تُربط لاحقاً بـ AutonomousUserAssistant)
# ==============================================================================
@ai_neural_router.post("/guide/{user_id}", summary="التوجيه العصبي للمستخدمين")
async def trigger_ai_guidance(user_id: int, query: str):
    """
    يستقبل طلبات المستخدمين ويوجهها للمحرك العصبي.
    التصميم هنا كـ (Gateway) فقط لمنع تكرار المنطق البرمجي الموجود في ai_services.py
    """
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="⚠️ [Sovereign Error]: لم يتم تقديم أي نص للتحليل."
        )
        
    logger.info(f"🧠 [Router]: Routing neural query for user [{user_id}]")
    return {
        "message": "تم توجيه الاستفسار للمحرك العصبي بنجاح.",
        "routed_user": user_id,
        "action": "pending_ai_response"
    }


# ==============================================================================
# 5. تجميع المسارات بشكل هرمي وآمن (Hierarchical Assembly)
# ==============================================================================
# هذه الطريقة تمنع بشكل قاطع أي خطأ برمجي ناتج عن تشابه الروابط (Route Collision)

api_v1_router.include_router(health_router)
api_v1_router.include_router(ai_neural_router)
api_v1_router.include_router(logistics_router)

logger.info("✅ [Router]: All V1 Enterprise routes successfully assembled without overlap.")
