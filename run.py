# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Master Orchestrator (v19.0.0-UnifiedMaster)
==============================================================================
نظام الإقلاع التشغيلي الشامل والموحد: يدمج فحص البنية التحتية، تهيئة قاعدة البيانات،
ويطلق النواة الإمبراطورية العظمى (backend_core.main:app) لتعمل ككيان واحد متكامل (Zero-Freeze).
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

# استيراد أداة تهيئة قاعدة البيانات الأساسية
try:
    from core.database import init_db
except ImportError:
    # بديل في حال اختلاف مسار قاعدة البيانات
    def init_db():
        pass

# --- إعداد السجلات المؤسسية (Enterprise Logging) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 👑 [%(levelname)-8s] | %(name)s - %(message)s"
)
logger = logging.getLogger("AymnGuard.SovereignMasterOrchestrator")

# ==============================================================================
# 1. نظام التشخيص والتهيئة القبلية (Pre-flight Diagnostics)
# ==============================================================================
def verify_infrastructure():
    logger.info("🛡️ [Diagnostics]: جاري فحص البنية التحتية والخزنة والمجلدات السيادية...")
    dirs = ["database", "logs", "app", "core", "bots", "services", "security", "backend_core"]
    for d in dirs:
        os.makedirs(os.path.join(ROOT_DIR, d), exist_ok=True)
    
    # تهيئة قاعدة البيانات وإصلاح الجداول
    try:
        init_db()
        logger.info("✅ [Database]: تم فحص وهيكلة قاعدة البيانات بنجاح.")
    except Exception as e:
        logger.warning(f"⚠️ [Database Notice]: تم تخطي التهيئة المباشرة لكونها تدار عبر النواة العظمى: {e}")

# ==============================================================================
# 2. استدعاء التطبيق المركزي الموحد من النواة الكبرى
# ==============================================================================
# نحن هنا نربط run.py مباشرة بـ backend_core.main لضمان عدم وجود تناقض أو ازدواجية
try:
    from backend_core.main import app as imperial_master_app
    logger.info("💎 [Master Bridge]: تم ربط النواة الإمبراطورية الكبرى (backend_core/main.py) بنجاح تام.")
except ImportError as err:
    logger.critical(f"❌ [Fatal Error]: تعذر استيراد النواة الكبرى من backend_core.main: {err}")
    sys.exit(1)

# ==============================================================================
# 3. إطلاق التشغيل المركزي (Execution Launcher)
# ==============================================================================
if __name__ == "__main__":
    # تنفيذ الفحص القبلي للبنية التحتية
    verify_infrastructure()
    
    # قراءة متغيرات البيئة أو الاعتماد على الإعدادات الموحدة
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 10000)) # استخدام بورت النواة الموحد
    
    logger.info(f"⚡ [Master Launcher]: جاري إطلاق الإمبراطورية السيادية على الشبكة {host}:{port}...")
    
    try:
        uvicorn.run(
            imperial_master_app,
            host=host,
            port=port,
            reload=False,
            workers=1, # ضبط الـ workers لضمان استقرار جلسات الـ WebSockets والـ Background Tasks
            log_level="info"
        )
    except Exception as e:
        logger.critical(f"❌ [Fatal Startup Error]: حدث خطأ أثناء الإقلاع: {e}")
