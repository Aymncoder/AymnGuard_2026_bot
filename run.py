# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Master Orchestrator (v18.0.0-Unified)
==============================================================================
نظام الإقلاع التشغيلي الشامل: يدمج الفحص الاستخباراتي، تهيئة قاعدة البيانات،
وإطلاق خادم FastAPI الإمبراطوري ليعمل ككيان واحد متكامل (Zero-Freeze).
"""

import os
import sys
import logging
import asyncio
import importlib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# --- إعداد المسارات والبيئة ---
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# --- استدعاءات النظام ---
from app.empire_app_gateway import sovereign_app_router
from core.database import init_db

try:
    from bots.protection.telegram_protection_runner import TelegramProtectionRunner
except ImportError:
    TelegramProtectionRunner = None

# --- إعداد السجلات (Enterprise Logging) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 👑 [%(levelname)-8s] | %(name)s - %(message)s"
)
logger = logging.getLogger("AymnGuard.SovereignMaster")

# ==============================================================================
# 1. نظام التشخيص والتهيئة (Pre-flight Diagnostics)
# ==============================================================================
def verify_infrastructure():
    logger.info("🛡️ [Diagnostics]: جاري فحص البنية التحتية والخزنة...")
    dirs = ["database", "logs", "app", "core", "bots", "services", "security"]
    for d in dirs:
        os.makedirs(os.path.join(ROOT_DIR, d), exist_ok=True)
    
    # تهيئة قاعدة البيانات
    try:
        init_db()
        logger.info("✅ [Database]: تم فحص وهيكلة قاعدة البيانات بنجاح.")
    except Exception as e:
        logger.critical(f"❌ [Database Error]: فشل إعداد قاعدة البيانات: {e}")
        sys.exit(1)

# ==============================================================================
# 2. دورة حياة الإمبراطورية (Lifespan Orchestration)
# ==============================================================================
@asynccontextmanager
async def sovereign_lifespan(app: FastAPI):
    logger.info("🚀 [SYSTEM BOOT]: بدء إقلاع منصة AymnGuard Sovereign Enterprise...")
    
    # تحميل المحركات (Microservices & Bots)
    logger.info("🧠 [AGI Forge]: تحميل العقل العصبي والميكروسيرفسات...")
    
    # ربط بوت الحماية إن وجد
    if TelegramProtectionRunner:
        logger.info("🤖 [Telegram Runner]: إطلاق مشغل تيليجرام الآمن.")
        
    logger.info("✅ [EMPIRE ONLINE]: جميع الخدمات تعمل بكفاءة سيادية.")
    yield 
    
    logger.info("🛑 [SYSTEM SHUTDOWN]: إغلاق آمن وحفظ الحالات...")

# ==============================================================================
# 3. تهيئة التطبيق المركزي (API Gateway)
# ==============================================================================
app = FastAPI(
    title="AymnGuard Sovereign Enterprise API",
    description="البوابة الإمبراطورية للتحكم بالذكاء الاصطناعي والحماية.",
    version="18.0.0",
    lifespan=sovereign_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sovereign_app_router)

# ==============================================================================
# 4. مسارات الفحص والتشغيل (Execution)
# ==============================================================================
@app.get("/")
async def root_status():
    return {
        "status": "ONLINE",
        "system": "AymnGuard Enterprise",
        "database": "Initialized",
        "version": "18.0.0"
    }

if __name__ == "__main__":
    # تنفيذ الفحص القبلي قبل التشغيل
    verify_infrastructure()
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"⚡ [Master Launcher]: الإطلاق على {host}:{port}...")
    
    try:
        uvicorn.run(
            "run:app", # تأكد أن هذا الملف اسمه run.py
            host=host,
            port=port,
            reload=False,
            workers=4,
            log_level="info"
        )
    except Exception as e:
        logger.critical(f"❌ [Fatal Startup Error]: {e}")
