# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Advanced Throttling & Flood Defense Middleware
جدار حماية ذكي متقدم ضد الـ Flood & Spam وإدارة معدل تدفق الطلبات عبر Redis
=============================================================================
"""

import time
import logging
import os
from fastapi import Request, status
from starlette.responses import JSONResponse
import redis.asyncio as aioredis

logger = logging.getLogger("AymnGuardFloodDefense")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

# ⚙️ إوابط ومحددات الحماية السيادية
MAX_REQUESTS = 25       # الحد الأقصى للطلبات المسموحة
TIME_WINDOW = 10        # النافذة الزمنية بالثواني
BLOCK_DURATION = 60     # مدة الحظر المؤقت (بالثواني) عند تجاوز الحد

async def rate_limiter_middleware(request: Request, call_next):
    """
    وسيط حماية ذكي فائق السرعة لرصد هجمات الـ Flood والتنصت على تكرار الطلبات غير المبررة (Rate Limiting).
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    path = request.url.path

    # تفعيل جدار الحماية الذكي على مسارات الـ API حصراً
    if "/api/" in path:
        block_key = f"aymnguard:blocked_ip:{client_ip}"
        rate_key = f"aymnguard:rate_limit:{client_ip}"

        try:
            # 1. التحقق مما إذا كان عنوان الـ IP محظوراً مؤقتاً بسبب محاولات تكرار سابقة (Flood)
            is_blocked = await redis_client.get(block_key)
            if is_blocked:
                logger.warning(f"🛡️ [Flood Defense]: تم رصد وتصد لطلب مرفوض من عنوان محظور مؤقتاً: {client_ip}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "status": "error",
                        "message": "تم حظرك مؤقتاً من النظام بسبب تجاوز حد الطلبات المتكررة (Flood & Spam Protection Active)."
                    }
                )

            # 2. نظام التتبع المتقدم عبر Redis باستخدام Pipeline للسرعة الخارقة
            pipeline = redis_client.pipeline()
            pipeline.incr(rate_key)
            pipeline.expire(rate_key, TIME_WINDOW)
            results = await pipeline.execute()
            
            request_count = results[0]

            # 3. تقييم ما إذا كان المستخدم قد تخطي الحد المسموح
            if request_count > MAX_REQUESTS:
                # تطبيق الحظر المؤقت الفوري في الذاكرة المؤقتة
                await redis_client.setex(block_key, BLOCK_DURATION, "1")
                logger.critical(f"🚨 [Security Alert]: اكتشاف نشاط مشبوه (Flood/Spam) من العنوان {client_ip}. تم فرض الحظر لـ {BLOCK_DURATION} ثانية.")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "status": "error",
                        "message": "تنبيه أمني سيادي: تم تجاوز الحد المسموح للطلبات. تم حظر الاتصال مؤقتاً لحماية استقرار النظام."
                    }
                )

        except Exception as e:
            # نظام التأمين العكسي (Fail-Open): في حال حدوث طارئ في اتصال Redis، يتم تمرير الطلب لضمان استمرارية الخدمة
            logger.error(f"❌ [Throttling Engine Error]: خطأ في نظام التحقق عبر Redis - التفاصيل: {str(e)}")

    response = await call_next(request)
    return response
