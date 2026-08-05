# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise Logistics Platform - V1 API Router Aggregator
مجمع المسارات المركزي (النسخة الأولى) - ربط وتوجيه كافة النقاط النهائية 
مع ضمان عزل النطاقات (Domain Isolation) ومنع التداخل.
=============================================================================
"""

import logging
from fastapi import APIRouter

# استيراد نقاط النهاية (Endpoints)
from app.api.v1.endpoints import auth
# from app.api.v1.endpoints import ai_core, logistics, users # مسارات مستقبلية

logger = logging.getLogger("AymnGuardV1Aggregator")

# ==============================================================================
# 1. تهيئة الموجه المركزي للإصدار الأول (V1 Router)
# 🛡️ تصحيح التسمية: تم تغيير الاسم إلى api_v1_router ليتطابق مع البوابة العظمى
# ==============================================================================
api_v1_router = APIRouter()


# ==============================================================================
# 2. تجميع المسارات بنظام النطاقات المعزولة (Domain-Driven Routing)
# ==============================================================================

# 🔒 نطاق المصادقة والأمان السيادي (Identity & Security Domain)
api_v1_router.include_router(
    auth.router,
    # يمكن إضافة prefix هنا إذا لم يكن موجوداً في ملف auth.py، 
    # ولكن الأفضل تركه هناك لضمان الاستقلالية
)

# 🧠 نطاق الذكاء الاصطناعي والأتمتة (AI & Autonomy Domain) - (جاهز للتفعيل)
# api_v1_router.include_router(
#     ai_core.router,
#     prefix="/ai",
#     tags=["AI Autonomous Engines"]
# )

# 📦 نطاق اللوجستيات والتحكم المركزي (Logistics & Control Domain) - (جاهز للتفعيل)
# api_v1_router.include_router(
#     logistics.router,
#     prefix="/logistics",
#     tags=["Global Logistics Management"]
# )

logger.debug("🌐 [V1 Aggregator]: تم تجميع وتأمين مسارات النسخة الأولى بنجاح، النظام جاهز لتلقي النبضات.")
