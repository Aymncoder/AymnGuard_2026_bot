# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Request Logging Middleware
==============================================================================
وسيط التسجيل والرقابة اللحظية (Logging Middleware)،
لمتابعة حركة الطلبات والردود، توليد معرفات التتبع الفريدة (Request ID)،
وقياس زمن الاستجابة بدقة متناهية لمراقبة أداء النواة السيادية.
"""

import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("AegisAICore.RequestLogger")

class EnterpriseLoggingMiddleware(BaseHTTPMiddleware):
    """وسيط مراقبة وتسجيل حركة الشبكة والطلبات بمعايير المؤسسات الكبرى."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # توليد معرف تتبع فريد (Correlation / Request ID) لكل طلب وارد أو التقاطه إن وجد
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # حساب زمن البداية لقياس الأداء والزمن المستغرق (Latency)
        start_time = time.perf_counter()
        
        # استخراج معلومات العميل والطلب
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        logger.info(f"📥 [Incoming Request] ID: {request_id} | IP: {client_ip} | Method: {method} | Path: {path}")
        
        response = None
        try:
            # تنفيذ الطلب والانتظار لاستكمال المعالجة
            response = await call_next(request)
            
            # حساب زمن التنفيذ بالمللي ثانية
            process_time = (time.perf_counter() - start_time) * 1000
            
            # حقن معرف التتبع وزمن الاستجابة في ترويسات الرد (Response Headers) للعميل
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
            
            status_code = response.status_code
            logger.info(f"📤 [Outgoing Response] ID: {request_id} | Status: {status_code} | Latency: {process_time:.2f}ms")
            
            return response
            
        except Exception as e:
            process_time = (time.perf_counter() - start_time) * 1000
            logger.error(f"❌ [Request Failed Error] ID: {request_id} | Path: {path} | Latency: {process_time:.2f}ms | Error: {str(e)}")
            raise e
