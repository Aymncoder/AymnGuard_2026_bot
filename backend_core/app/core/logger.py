"""
=============================================================================
AymnGuard Enterprise Logistics Platform - Central Enterprise Logger
النظام التسجيلي المركزي المؤسسي - تتبع ذكي، تدوير آلي للملفات، وأمان مطلق.
=============================================================================
"""

import sys
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_enterprise_logger(name: str = "AymnGuardEnterpriseCore") -> logging.Logger:
    """
    إعداد ونشر محرك التسجيل المؤسسي المركزي مع دعم التدوير الآلي للذاكرة 
    والتعامل مع العمليات اللوجستية الضخمة دون فقدان أي سجل.
    """
    # التأكد من وجود مجلد السجلات المؤسسي
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # تصميم صيغة السجل المؤسسي المتقدمة (تشمل الوقت، المستوى، الملف ورقم السطر)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | [Core-Engine] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 1. معالج العرض المباشر على الطرفية (Stream Handler)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
        # 2. معالج الحفظ الآلي في الملفات مع تدوير الحجم (Rotating File Handler)
        # يحفظ حتى 10 ميجابايت لكل ملف ويحتفظ بـ 5 نسخ احتياطية لمنع تضخم المساحة
        log_file_path = os.path.join("logs", "aymnguard_enterprise.log")
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=10 * 1024 * 1024, 
            backupCount=5, 
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # منع تضاعف السجلات
        logger.propagate = False

    return logger

# إنشاء النسخة المركزية المعتمدة للاستخدام في كافة قطاعات المنصة
logger = setup_enterprise_logger()
