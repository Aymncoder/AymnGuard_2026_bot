# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise - Sovereign Telemetry & Logging System (v18.0.0-Master)
==============================================================================
نظام الاستشعار المركزي: تسجيل الأحداث المؤسسية مع دعم التتبع العميق للعمليات،
التدوير التلقائي للملفات، والحماية من امتلاء المساحة التخزينية.
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
import os
from pathlib import Path

class SovereignFormatter(logging.Formatter):
    """
    منسق متقدم يعالج السجلات:
    يضيف بصمة تتبع (request_id) لكل عملية، مما يمنع تداخل المسارات ويضمن وجود بصمة للتاريخ.
    """
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, 'request_id'):
            # إذا كان الحدث داخلياً (من النظام نفسه وليس من مستخدم)، نوسمه بـ SYSTEM-CORE
            record.request_id = 'SYSTEM-CORE'
        return super().format(record)

def setup_logger(name: str = "AymnGuard", default_level: int = logging.INFO) -> logging.Logger:
    """إعداد نظام التسجيل المؤسسي مع حماية من تكرار التهيئة وتأمين المسارات."""
    
    logger = logging.getLogger(name)
    
    # منع التكرار القاتل للمسارات في حال استدعاء الملف أكثر من مرة
    if getattr(logger, '_init_done', False):
        return logger

    logger.setLevel(default_level)
    logger.handlers.clear() # مسح أي معالجات قديمة لضمان نظافة السجلات

    # التنسيق المؤسسي: الوقت | المستوى | البصمة الأمنية | الملف:السطر | الرسالة
    log_format = "%(asctime)s | %(levelname)-8s | [%(request_id)s] | %(module)s:%(lineno)d | %(message)s"
    formatter = SovereignFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # 1. معالج الشاشة (Console - stdout) لبيانات Docker & AI Monitoring
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. معالج الملفات (File Handler) مع التدوير الذاتي (Self-Healing Storage)
    try:
        # التأكد من إنشاء مجلد السجلات بأمان تام ودون أخطاء صلاحيات
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file_path = log_dir / "aymnguard_sys.log"
        
        file_handler = RotatingFileHandler(
            filename=str(log_file_path),
            maxBytes=10 * 1024 * 1024,  # رفع السعة إلى 10 ميجابايت للمسحة
            backupCount=5,              # الاحتفاظ بـ 5 نسخ تاريخية
            encoding="utf-8"
        )
        
        # مسجل الملف يلتقط تحذيرات النظام والأخطاء بشكل افتراضي
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"⚠️ [Logger Warning]: تعذر إنشاء ملف السجلات المحلي، سيتم الاكتفاء بالشاشة: {e}\n")

    logger._init_done = True
    
    # تسجيل لحظة الاستيقاظ
    logger.info("🔭 [Telemetry Engine]: تم تشغيل نظام الاستشعار المركزي بنجاح.")

    return logger

# كائن جاهز للاستيراد المباشر في كافة أرجاء المنصة
logger = setup_logger()
