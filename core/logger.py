import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def setup_logger(name: str = "AymnGuard") -> logging.Logger:
    """
    إعداد نظام تسجيل مركزي (Enterprise Logger).
    يدعم الطباعة المباشرة لـ Docker، وتدوير الملفات التلقائي لحماية سعة التخزين.
    """
    logger = logging.getLogger(name)
    
    # منع تكرار إنشاء الـ Handlers إذا تم استيراد الملف في أكثر من مكان
    if getattr(logger, '_init_done', False):
        return logger

    # تحديد المستوى الأساسي (يمكن جعله يتغير بناءً على ملف .env مستقبلاً)
    logger.setLevel(logging.INFO)

    # تنسيق احترافي يوضح: الوقت | مستوى الخطأ | اسم الملف ورقم السطر | الرسالة
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. معالج الشاشة (Console Handler) - ضروري لتتبع السجلات عبر أمر docker logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. معالج الملفات (File Handler) - مع نظام التدوير
    # ينشئ مجلد logs إذا لم يكن موجوداً
    os.makedirs("logs", exist_ok=True)
    
    # يحتفظ بملفات حجمها 5MB كحد أقصى، ويحتفظ بـ 3 نسخ احتياطية فقط
    file_handler = RotatingFileHandler(
        filename="logs/aymnguard_sys.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.WARNING) # نسجل في الملفات الأخطاء والتحذيرات فقط لتقليل الحجم
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger._init_done = True
    return logger

# كائن جاهز للاستيراد المباشر: from core.logger import logger
logger = setup_logger()

