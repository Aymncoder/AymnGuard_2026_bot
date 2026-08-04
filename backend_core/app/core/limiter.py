# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Distributed Rate Limiter Engine
==============================================================================
محرك حماية السرعة والتحكم في معدل الطلبات (Rate Limiting) الموزع عبر Redis،
مصمم وفق أعلى المعايير المؤسسية العالمية لحماية مسارات الـ API من الهجمات والتخمين.
"""

import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

logger = logging.getLogger("AegisAICore.RateLimiter")

# قراءة إعدادات البيئة لـ Redis والحدود الافتراضية مع دعم التخصيص الكامل
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DEFAULT_RATE_LIMIT = os.getenv("DEFAULT_RATE_LIMIT", "100/minute")

def get_real_client_ip(request: Request) -> str:
    """
    استخراج عنوان الـ IP الحقيقي للمستخدم بدقة فائقة ومعالجة التواجد 
    خلف شبكات التوجيه العكسي، منصات الحماية (مثل Cloudflare)، أو خوادم Nginx.
    """
    try:
        # فحص ترويسات Cloudflare المباشرة
        cf_connecting_ip = request.headers.get("CF-Connecting-IP")
        if cf_connecting_ip:
            return cf_connecting_ip.strip()

        # فحص سلسلة العناوين المحولة القياسية
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
            if client_ip:
                return client_ip
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
            
        if request.client and request.client.host:
            return request.client.host
            
    except Exception as e:
        logger.error(f"⚠️ [RateLimiter IP Extraction Error]: فشل استخراج الـ IP بدقة: {str(e)}")
        
    return get_remote_address(request)

# إعداد محرك محدد السرعة الموزع بمعايير المؤسسات الكبرى مع آلية أمان استباقية (Fallback)
try:
    limiter = Limiter(
        key_func=get_real_client_ip,
        storage_uri=REDIS_URL,
        default_limits=[DEFAULT_RATE_LIMIT],
        strategy="fixed-window",
        enabled=True
    )
    logger.info("🛡️ [RateLimiter Engine]: تم تهيئة محرك حماية السرعة الموزع عبر Redis بنجاح.")
except Exception as e:
    logger.critical(f"❌ [RateLimiter Critical Failure]: تعذر تهيئة محرك السرعة مع Redis: {str(e)}")
    # تفعيل نظام احتياطي محلي لمنع توقف الخادم في حال انقطاع اتصال Redis الموزع
    limiter = Limiter(
        key_func=get_real_client_ip,
        default_limits=[DEFAULT_RATE_LIMIT],
        strategy="fixed-window"
    )
