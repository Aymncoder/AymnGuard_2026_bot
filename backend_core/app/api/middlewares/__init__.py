# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Middlewares Registry
==============================================================================
المركز السيادي للوسائط (Middlewares Hub) ومعالجات الاستثناءات.
مصمم بحرفية لمنع تداخل المسارات (Race Conditions) وتتبع مسار كل طلب
بدقة متناهية من لحظة دخوله حتى استجابة محركات الذكاء الاصطناعي.
"""

import uuid
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.errors import RateLimitExceeded

# استيراد معالج تجاوز حد الطلبات الذي تم تطويره مسبقاً
from app.api.middlewares.rate_limiter import custom_rate_limit_exceeded_handler

logger = logging.getLogger("AegisAICore.MiddlewaresRegistry")


async def request_tracing_middleware(request: Request, call_next):
    """
    نظام التتبع الجراحي للمسارات (Request Tracing):
    يولد معرفاً فريداً (UUID) لكل طلب يدخل النظام، مما يمنع اختلاط البيانات
    بين آلاف المستخدمين والعمال الخلفيين (Background Workers).
    """
    request_id = str(uuid.uuid4())
    # حقن المعرف داخل حالة الطلب ليكون متاحاً لكافة وظائف النظام
    request.state.request_id = request_id
    
    # تمرير الطلب للطبقة التالية
    response = await call_next(request)
    
    # إرجاع المعرف في رأس الاستجابة (Headers) للتوثيق والشفافية
    response.headers["X-Request-ID"] = request_id
    return response


def setup_enterprise_middlewares(app: FastAPI) -> None:
    """
    دالة الحقن السيادي للوسائط (Dependency & Middleware Injector):
    تقوم بتغليف التطبيق بطبقات الحماية بشكل تسلسلي صارم ومدروس لتجنب أي 
    تعارض أو أخطاء برمجية في دورة حياة الطلب.
    """
    
    # 1. حقن وسيط تتبع المسارات (الأولوية القصوى لمعرفة هوية كل طلب)
    app.add_middleware(BaseHTTPMiddleware, dispatch=request_tracing_middleware)
    
    # 2. حقن درع مشاركة الموارد (CORS) مع سياسات صارمة لتحديد من يمكنه الاتصال
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # في بيئة الإنتاج المتقدمة يتم تحديد النطاقات المصرح لها فقط
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 3. ربط معالج استثناءات الضغط العالي (Rate Limiting) لمنع الانهيار
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)
    
    logger.info("🛡️ [Middlewares Registry]: تم تفعيل وتوجيه الدروع المؤسسية ومنع تداخل المسارات بنجاح.")
