# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : HMAC-SHA256 Cryptographic Security Layer (v18.0.0)
==============================================================================
طبقة التوثيق المشفر: تؤمن الاتصالات المتبادلة بين المشغلات والميكروسيرفسات
عبر توقيع الحمولة (Payload) ببصمة مشفرة تمنع التلاعب أو الهجمات الوسيطة (MitM).
"""

import hmac
import hashlib
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("AegisAICore.HMACSecurityGuard")
logger.setLevel(logging.INFO)

# مفتاح التوقيع السري الخاص بالسيادة المؤسسية (يُفضل حفظه في متغيرات البيئة Environment Variables)
SECRET_SOVEREIGN_KEY = b"AG-SOVEREIGN-MASTER-SECURE-KEY-2026"

class HMACSecurityGuard:
    """
    حارس الأمن المشفر: يتولى عملية توليد التواقيع والتحقق من صحتها لكل رسالة تمر عبر الممر المركزي.
    """

    @staticmethod
    def generate_signature(payload: Dict[str, Any]) -> str:
        """توليد توقيع مشفر (HMAC-SHA256) بناءً على محتوى الحمولة."""
        payload_string = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        signature = hmac.new(
            SECRET_SOVEREIGN_KEY,
            payload_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    @staticmethod
    def verify_request_signature(payload: Dict[str, Any], provided_signature: str) -> bool:
        """التحقق الصارم من مطابقة التوقيع الوارد للحمولة قبل السماح بتنفيذها."""
        if not provided_signature:
            return False
            
        expected_signature = HMACSecurityGuard.generate_signature(payload)
        # مقارنة آمنة ضد هجمات التوقيت (Timing Attack Safe)
        is_valid = hmac.compare_digest(expected_signature, provided_signature)
        
        if not is_valid:
            logger.warning("🚨 [HMAC Security Alert]: فشل التحقق من توقيع الطلب! تم رصد محاولة تلاعب أو حقن.")
            
        return is_valid
