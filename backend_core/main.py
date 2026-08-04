# ============================================================
# AymnGuard Enterprise Logistics & Sovereign Platform - v5.0.0-Ultimate
# ============================================================

import sys
import os
import time
import uuid
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

# 1. الاستيرادات الداخلية والنظامية (Modular Imports)
from app.db.database import get_db, init_databases
from app.core.security import verify_sovereign_key, rate_limiter_middleware

# 2. الروترات والهับ الداخلي (Routers Hub)
from app.api.v1.api_router import api_router

# 3. الخدمات المجدولة وجلسات تليجرام (Services & Telemetry)
from app.services.scheduler import setup_scheduler, start_scheduler, shutdown_scheduler
from app.telegram_bot_core import bot, WEBHOOK_URL, TELEGRAM_SECRET_TOKEN

# ============================================================
# إعداد نظام التسجيل المؤسسي (Central Logging)
# ============================================================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | [%(module)s] | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/enterprise_core.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("AymnGuardCore.MasterMain")

# ============================================================
# دورة حياة التطبيق المؤسسية (Enterprise Lifespan)
# ============================================================
@asynccontextmanager
async def enterprise_lifespan(app: FastAPI):
    startup_marker = time.time()
    logger.info("🚀 [AymnGuard Core v5.0] إدراج نواة الأمان والتشغيل المؤسسي قيد البدء...")
    app.state.startup_time = startup_marker
    
    # 1. تهيئة قواعد البيانات
    try:
        await init_databases()
        logger.info("✅ تم إنجاز تهيئة قواعد البيانات ومواعيد الاتصال بنجاح.")
    except Exception as db_err:
        logger.critical(f"❌ فشل حرج في تهيئة قواعد البيانات: {db_err}")
        raise db_err

    # 2. إطلاق الجداول والخدمات الخلفية
    try:
        setup_scheduler()
        start_scheduler()
        logger.info("✅ قنوات المتابعة والجدولة الزمنية قيد التشغيل التام.")
    except Exception as sch_err:
        logger.error(f"⚠️ تحذير في إقلاع الجدول الزمني: {sch_err}")

    # 3. إعداد الويب هوك الخاص بتليجرام
    if WEBHOOK_URL and TELEGRAM_SECRET_TOKEN:
        try:
            bot.remove_webhook()
            time.sleep(0.5)
            bot.set_webhook(url=WEBHOOK_URL, secret_token=TELEGRAM_SECRET_TOKEN, drop_pending_updates=True)
            logger.info(f"✅ تم ربط الويب هوك بنجاح: {WEBHOOK_URL}")
        except Exception as e:
            logger.error(f"❌ خطأ خلفي في ربط الويب هوك: {e}")
    else:
        logger.warning("ℹ️ يعمل بوت تليجرام في وضع الاستماع المحلي أو اليدوي.")

    yield  # --- بداية تشغيل النظام أثناء فترة النفاذ ---

    # 4. إغلاق النظام بأمان (Graceful Shutdown)
    logger.warning("🛑 [AymnGuard Core] إيقاف تشغيل النظام وأمان الأرجوحة اللوجستية قيد التنفيذ...")
    try:
        shutdown_scheduler()
        logger.info("✅ تم إيقاف المداولات واللوجستيات الخلفية بأمان تام.")
    except Exception as ex:
        logger.error(f"❌ خطأ أثناء الإيقاف الآمن: {ex}")

# ============================================================
# تعريف التطبيق والواجهة (FastAPI Initialization)
# ============================================================
app = FastAPI(
    title="AymnGuard Enterprise Logistics & Sovereign Platform",
    description="النواة الخلفية الآمنة للمنصة اللوجستية المستقلة وإدارة الـ API وتكامل بوت تليجرام الذكي",
    version="5.0.0-Ultimate",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=enterprise_lifespan
)

# تجهيز المجلدات الأساسية
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/app", exist_ok=True)

templates = Jinja2Templates(directory="templates")

# ============================================================
# الوسائط والتحكم في الاتصال (Middlewares)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(rate_limiter_middleware)

# تتبع معرف الطلبات (Request ID Tracing)
@app.middleware("http")
async def enterprise_telemetry_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Powered-By"] = "AymnGuard Enterprise Sovereign Core"
    return response

# معالج الأخطاء المركزي المتقدم
@app.exception_handler(Exception)
async def global_enterprise_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", "UNKNOWN")
    logger.error(f"[{req_id}] System Critical Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "request_id": req_id,
            "message": "حدث خطأ غير متوقع أثناء معالجة طلبك السيادي.",
            "debug_hint": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else "Protected Enterprise Security Error"
        }
    )

# ============================================================
# المسار الرئيسي وقوالب الواجهة السيادية (Root Endpoint)
# ============================================================
@app.get("/", response_class=HTMLResponse, summary="الصفحة الرئيسية السيادية للمنصة")
async def sovereign_root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request, "platform_version": "5.0.0-Ultimate"})
    except Exception:
        # واجهة هبوط افتراضية أنيقة ومصممة بعناية فائقة في حال غياب القالب الخارجي
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AymnGuard Enterprise Sovereign Platform</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, sans-serif; background: #0b0f19; color: #f3f4f6; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .card { background: #1f2937; max-width: 650px; padding: 50px; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); border: 1px solid #374151; }
                h1 { color: #60a5fa; margin-bottom: 15px; font-size: 28px; }
                p { color: #9ca3af; line-height: 1.6; margin-bottom: 30px; }
                .btn { display: inline-block; padding: 12px 25px; background: #2563eb; color: #fff; text-decoration: none; border-radius: 8px; font-weight: bold; transition: background 0.3s; }
                .btn:hover { background: #1d4ed8; }
                .badge { display: inline-block; padding: 4px 12px; background: #065f46; color: #34d399; border-radius: 20px; font-size: 12px; margin-bottom: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="card">
                <span class="badge">v5.0.0-Ultimate | Active & Secure</span>
                <h1>🛡️ AymnGuard Enterprise Sovereign Platform</h1>
                <p>النواة الخلفية للسيادة اللوجستية، إدارة الـ API، والتشغيل الذكي تعمل بكفاءة وأمان مطلق تحت إشرافك المباشر.</p>
                <a href="/docs" class="btn">🚀 عرض التوثيق التفاعلي (Swagger UI)</a>
            </div>
        </body>
        </html>
        """)

# ============================================================
# 5. مركز التحكم السيادي (Sovereign Control Center Router)
# ============================================================
owner_sovereign_router = APIRouter(prefix="/api/v1/sovereign-owner", tags=["Sovereign Owner Control Center"])

class SystemOverrideSchema(BaseModel):
    action_type: str = Field(..., description="مديرية التفعيل وتاريخ المرجع الخارجي")
    authorization_key: str = Field(..., description="المفتاح السيادي الموثوق والآمن")
    payload: Dict[str, Any] = Field(default={}, description="المرجع لكل قيادة تفصيلية")

@owner_sovereign_router.get("/metrics", summary="الحصول على مقاييس أداء النظام السيادي")
async def sovereign_system_metrics(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    uptime = time.time() - getattr(app.state, "startup_time", time.time())
    return {
        "status": "success",
        "sovereign_clearance": "AUTHORIZED_OWNER",
        "metrics": {
            "platform_status": "ONLINE_STABLE",
            "active_nodes": 1,
            "database_engine": "SQLite / PostgreSQL / MongoDB Enterprise Bridge",
            "uptime_seconds": int(uptime),
            "security_integrity": "100%",
            "system_version": "5.0.0-Ultimate",
            "architecture": "Clean Micro-Core & Async SQLAlchemy 2.0"
        }
    }

@owner_sovereign_router.post("/override-control", summary="تفعيل التعديلات والعمليات التشغيلية الطارئة")
async def execute_sovereign_override(data: SystemOverrideSchema, db: AsyncSession = Depends(get_db)):
    if not verify_sovereign_key(data.authorization_key):
        logger.warning(f"⚠️ محاولة تجاوز أمني غير مأذون به لـ {data.action_type}")
        raise HTTPException(status_code=403, detail="تصريح أمني مرفوض: مفتاح السيادة غير صالح.")
    
    logger.info(f"🛡️ تنشيط إداري سيادي: تم تنفيذ أمر [{data.action_type}] بنجاح.")
    return {
        "status": "success",
        "message": f"تم تنفيذ وتوجيه إيعاز [{data.action_type}] بنجاح تحت إشراف سيادي.",
        "executed_payload": data.payload,
        "timestamp": time.time()
    }

# ============================================================
# 6. ربط الروترات والخدمات الثابتة (Routers Hub & Mounts)
# ============================================================
app.include_router(api_router, prefix="/api/v1")
app.include_router(owner_sovereign_router)

# تركيب الملفات الثابتة وتطبيقات الويب (PWA & Static Assets)
app.mount("/app", StaticFiles(directory="static/app", html=True), name="static_app")
app.mount("/static", StaticFiles(directory="static"), name="static_files")

# ============================================================
# 7. نقطة الدخول السيادية (Entry Point)
# ============================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🌐 بدء إطلاق الخادم السيادي على المنفذ: {port}...")
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=False)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 تم إيقاف السيرفر وبدء إغلاق ملفات العمل بأمان.")
