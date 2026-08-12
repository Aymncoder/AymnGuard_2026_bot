# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Master Orchestrator (v19.1.1-Port8000)
==============================================================================
نظام الإقلاع التشغيلي الشامل والموحد والمحصن ضد الانهيار: يدمج فحص البنية التحتية، 
تهيئة قاعدة البيانات بأمان تام، ويطلق النواة الإمبراطورية العظمى على البورت 8000.
==============================================================================
"""

import os
import sys
import logging
import asyncio
import uvicorn
from contextlib import asynccontextmanager

# --- إعداد المسارات والبيئة السيادية ---
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# استيراد أداة تهيئة قاعدة البيانات الأساسية مع حماية شاملة ضد التعطل
try:
    from core.database import init_db
except ImportError:
    def init_db():
        pass

# --- إعداد السجلات المؤسسية (Enterprise Logging) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 👑 [%(levelname)-8s] | %(name)s - %(message)s"
)
logger = logging.getLogger("AymnGuard.SovereignMasterOrchestrator")

# ==============================================================================
# 1. نظام التشخيص والتهيئة القبلية الآمنة (Pre-flight Diagnostics)
# ==============================================================================
def verify_infrastructure():
    logger.info("🛡️ [Diagnostics]: جاري فحص البنية التحتية والخزنة والمجلدات السيادية...")
    dirs = ["database", "logs", "app", "core", "bots", "services", "security", "backend_core"]
    for d in dirs:
        try:
            os.makedirs(os.path.join(ROOT_DIR, d), exist_ok=True)
        except Exception as e:
            logger.error(f"❌ [Directory Error]: تعذر إنشاء المجلد {d}: {e}")
    
    # تهيئة قاعدة البيانات مع التقاط أي استثناء لتجنب الانهيار المفاجئ
    try:
        init_db()
        logger.info("✅ [Database]: تم فحص وهيكلة قاعدة البيانات بنجاح.")
    except Exception as e:
        logger.warning(f"⚠️ [Database Notice]: تنبيه أثناء تهيئة قاعدة البيانات، سيتم الاعتماد على النواة العظمى: {e}")

# ==============================================================================
# 2. استدعاء التطبيق المركزي الموحد من النواة الكبرى
# ==============================================================================
try:
    from backend_core.main import app as imperial_master_app
    logger.info("💎 [Master Bridge]: تم ربط النواة الإمبراطورية الكبرى (backend_core/main.py) بنجاح تام.")
except ImportError as err:
    logger.critical(f"❌ [Fatal Error]: تعذر استيراد النواة الكبرى من backend_core.main: {err}")
    sys.exit(1)

# ==============================================================================
# 3. إطلاق التشغيل المركزي الآمن على البورت 8000
# ==============================================================================
if __name__ == "__main__":
    # تنفيذ الفحص القبلي للبنية التحتية
    verify_infrastructure()
    
    # قراءة متغيرات البيئة وضبط البورت الافتراضي على 8000
    host = os.getenv("HOST", "0.0.0.0")
    
    raw_port = os.getenv("PORT", "8000")
    try:
        port = int(raw_port)
    except (TypeError, ValueError):
        port = 8000
        logger.warning(f"⚠️ [Config Notice]: قيمة البورت المستلمة غير صالحة ('{raw_port}'). تم استخدام البورت الافتراضي 8000.")
    
    logger.info(f"⚡ [Master Launcher]: جاري إطلاق الإمبراطورية السيادية على الشبكة {host}:{port}...")
    
    try:
        uvicorn.run(
            imperial_master_app,
            host=host,
            port=port,
            reload=False,
            workers=1, # ضمان استقرار جلسات الـ WebSockets والـ Background Tasks
            log_level="info"
        )
    except Exception as e:
        logger.critical(f"❌ [Fatal Startup Error]: حدث خطأ فادح أثناء إقلاع خادم Uvicorn: {e}")
        sys.exit(1)
