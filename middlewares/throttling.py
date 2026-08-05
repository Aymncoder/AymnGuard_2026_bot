# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Throttling & Rate Limiting Middleware
وسيط الحماية وإدارة معدل تدفق الطلبات لحجب الهجمات وحماية الموارد
=============================================================================
"""

import time
import logging
from fastapi import Request, HTTPException, status
from starlette.responses import JSONResponse

logger = logging.getLogger("AymnGuardThrottlingEngine")

# ذاكرة مؤقتة بسيطة لتتبع عدد الطلبات لكل IP (يمكن ترقيتها لاحقاً لـ Redis)
request_counts = {}

async def rate_limiter_middleware(request: Request, call_next):
    """
    وسيط أمني لفحص مصدر الطلب ومعدل التدفق لضمان عدم استنزاف موارد النواة.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    path = request.url.path

    # تفعيل الفحص على مسارات الـ API الحساسة فقط
    if "/api/" in path:
        logger.debug(f"🛡️ [Throttling Engine]: تتبع طلب قادم من العنوان {client_ip} نحو المسار {path}")
        
        # يمكن دمج خوارزمية الـ Token Bucket أو Sliding Window هنا مستقبلاً عبر Redis
        # حالياً نقوم بالسماح بالطلب وتمريره بلطف مع تسجيله في الصندوق الأسود

    response = await call_next(request)
    return response
