# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign FastAPI Production Core (v5.0 Ultimate)
النواة المركزية الموحدة: ربط الـ API، قاعدة البيانات الدائمة، محركات الذكاء الاصطناعي، واستقبال الـ Webhooks
=============================================================================
"""

import os
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import Update

# استيراد محركات الخدمة والنواة مع حماية المسارات المطلقة
try:
    from backend_core.bot.bot_main import bot, dp
    from backend_core.api.v1.ai_studio_router import router as ai_studio_router
    from backend_core.api.v1.search_media_router import router as search_router
    from backend_core.api.v1.subscription_router import router as subscription_router
    from backend_core.database import init_db
except ImportError:
    try:
        from bot.bot_main import bot, dp
        from api.v1.ai_studio_router import router as ai_studio_router
        from api.v1.search_media_router import router as search_router
        from api.v1.subscription_router import router as subscription_router
        from database import init_db
    except ImportError:
        from ..bot.bot_main import bot, dp
        from ..api.v1.ai_studio_router import router as ai_studio_router
        from ..api.v1.search_media_router import router as search_router
        from ..api.v1.subscription_router import router as subscription_router
        from ..database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AymnGuardCore")

app = FastAPI(
    title="AymnGuard Enterprise Sovereign API",
    version="5.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تفعيل سياسة المشاركة المتبادلة (CORS) للواجهات والـ Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل مسارات الـ API السيادية (الاشتراكات، استوديو التصميم، البحث الشامل)
app.include_router(subscription_router)
app.include_router(ai_studio_router)
app.include_router(search_router)

WEBHOOK_PATH = f"/webhook/{os.getenv('TELEGRAM_BOT_TOKEN', 'secure_token')}"
WEBHOOK_URL = f"{os.getenv('PUBLIC_DOMAIN', 'https://your-domain.com')}{WEBHOOK_PATH}"

@app.on_event("startup")
async def startup_event():
    """
    حدث إقلاع النواة: تهيئة قاعدة البيانات الدائمة وربط الـ Webhook مع تيليجرام تلقائياً.
    """
    logger.info("🚀 [Core Startup]: جاري إقلاع النواة السيادية وتهيئة جداول القاعدة الدائمة...")
    try:
        # تهيئة وإنشاء جداول قاعدة البيانات عند الإقلاع الأول
        await init_db()
        logger.info("✅ [Database Initialized]: تم تهيئة وعمل جداول قاعدة البيانات الدائمة بنجاح.")

        # ربط الـ Webhook
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        logger.info(f"✅ [Webhook Connected]: تم ربط البوت بنجاح على المسار: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ [Startup Error]: فشل في تهيئة النواة أو ربط الـ Webhook - التفاصيل: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    حدث الإيقاف: تنظيف الاتصالات وإغلاق جلسات البوت بأمان.
    """
    logger.info("🛑 [Core Shutdown]: جاري إيقاف النواة وإغلاق الجلسات السيادية...")
    await bot.session.close()

@app.post(WEBHOOK_PATH)
async def telegram_webhook_endpoint(request: Request):
    """
    نقطة استقبال تحديثات تيليجرام وتليجرام الأعمال عبر الـ Webhook الفوري.
    """
    try:
        json_data = await request.json()
        update = Update.model_validate(json_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"❌ [Webhook Processing Error]: خطأ في معالجة تحديث الـ Webhook - التفاصيل: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"status": "error", "detail": str(e)})

@app.get("/health", tags=["System Health"])
async def health_check():
    """
    فحص صحة النواة وحالة النظام اللحظية.
    """
    return {
        "status": "healthy",
        "system": "AymnGuard Enterprise Core",
        "version": "5.0.0",
        "database": "Active Async SQLAlchemy",
        "security": "Active & Sovereign"
    }
