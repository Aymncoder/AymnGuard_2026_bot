# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Telemetry & Logging System
نظام الاستشعار المركزي - تسجيل الأحداث المؤسسية مع دعم التتبع العميق للعمليات
=============================================================================
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
import os

class SovereignFormatter(logging.Formatter):
    """
    منسق متقدم يعالج السجلات. 
    يضمن وجود بصمة التتبع (request_id) لكل عملية، مما يمنع تداخل المسارات.
    """
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, 'request_id'):
            # إذا كان الحدث داخلياً (من النظام نفسه وليس من مستخدم)، نوسمه بـ SYSTEM
            record.request_id = 'SYSTEM-CORE'
        return super().format(record)

def setup_logger(name: str = "AymnGuard", default_level: int = logging.INFO) -> logging.Logger:
    """إعداد نظام التسجيل المؤسسي مع حماية من تكرار التهيئة"""
    
    logger = logging.getLogger(name)
    
    # منع التكرار القاتل للمسارات في حال استدعاء الملف أكثر من مرة
    if getattr(logger, '_init_done', False):
        return logger

    logger.setLevel(default_level)
    
    # 🔍 التنسيق المؤسسي: الوقت | المستوى | [بصمة العملية] | الملف:السطر | الرسالة
    log_format = "%(asctime)s | %(levelname)-8s | [%(request_id)s] | %(module)s:%(lineno)d | %(message)s"
    formatter = SovereignFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # 1. معالج النافذة (Console - stdout) لبيئات Docker و AI Monitoring
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. معالج الملفات (File Handler) مع التدوير الذاتي (Self-Healing Storage)
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        filename="logs/aymnguard_sys.log",
        maxBytes=10 * 1024 * 1024,  # رفعنا السعة إلى 10 ميجابايت للنسخة
        backupCount=5,              # الاحتفاظ بـ 5 نسخ تاريخية
        encoding="utf-8"
    )
    
    # سنجعل الملف يلتقط تحذيرات النظام والأخطاء بشكل افتراضي
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger._init_done = True
    
    # تسجيل لحظة الاستيقاظ
    logger.info("📡 [Telemetry Engine]: تم تشغيل نظام الاستشعار المركزي بنجاح.")
    
    return logger

# كائن جاهز للاستيراد المباشر في كافة أنحاء المنصة
logger = setup_logger()
