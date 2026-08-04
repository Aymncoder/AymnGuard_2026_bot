# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Rate Limit Exception Middleware
==============================================================================
معالج استثناءات تجاوز حد الطلبات (Rate Limit Exceeded Exception Handler)
المصمم بمعايير المؤسسات الكبرى لحماية المنصة من الهجمات، التسجيل اللحظي،
وتوفير استجابات منظمة ومؤمنة للمستخدمين عبر العُقد الموزعة.
"""

import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger("AegisAICore.RateLimitMiddleware")

async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    معالج مركزي متطور لتجاوز حد الاستخدام (Rate Limiting):
    - التقاط تفاصيل الطلب وعنوان الـ IP والمحطة المستهدفة بدقة.
    - تسجيل التنبيه الأمني لمراقبة محاولات الضغط العالي أو الهجمات السيبرانية.
    - إرجاع استجابة JSON موحدة واحترافية للعميل مع توضيح مهلة الانتظار.
    """
    # استخراج الـ IP الحقيقي مع مراعاة البروكسي
    forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else (request.client.host if request.client else "unknown")
    path = request.url.path
    
    logger.warning(
        f"🚨 [Security Alert - Rate Limit Exceeded]: "
        f"IP: {client_ip} | Path: {path} | Limit Detail: {exc.detail}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "status": "error",
            "code": 429,
            "error_type": "RateLimitExceeded",
            "message": "⚠️ لقد تجاوزت الحد المسموح به من الطلبات في الوقت الحالي. حماية لاستقرار المنصة، يرجى الانتظار قليلاً قبل إعادة المحاولة.",
            "details": {
                "path": path,
                "limit_info": str(exc.detail)
            }
        },
        headers={
            "Retry-After": "60",
            "X-RateLimit-Error": "Too Many Requests"
        }
    )
