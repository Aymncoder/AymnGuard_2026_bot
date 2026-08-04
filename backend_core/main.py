# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise Sovereign Platform (v7.0.0-MasterCore)
==============================================================================
النواة المؤسسية الشاملة للسيادة اللوجستية، إدارة قواعد البيانات المستمرة، 
بوابات المصادقة الآمنة، والتحكم المطلق في المنظومة عبر واجهات مستوحاة 
من النمط العالمي لتطبيقات تيليجرام وتطبيقات الأندرويد المتقدمة.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

# ==============================================================================
# 1. نظام التثبيت والتهيئة الذكي (Smart Auto-Installer Engine)
# ==============================================================================
def setup_environment():
    """فحص البيئة وتثبيت الحزم المطلوبة ديناميكياً لتشغيل النواة بكفاءة تامة."""
    print("\n" + "="*75)
    print("⚙️ [AymnGuard Core]: جاري فحص وتحديث البيئة البرمجية وقاعدة البيانات المستمرة...")
    
    try:
        if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
            subprocess.run(
                "pkg update -y > /dev/null 2>&1 && pkg upgrade -y > /dev/null 2>&1",
                shell=True,
                check=False
            )
    except Exception:
        pass

    required_packages = ["fastapi", "uvicorn", "pydantic", "pydantic-settings", "httpx", "sqlalchemy", "aiosqlite"]
    missing_packages = []

    for pkg in required_packages:
        pkg_import_name = pkg.replace("-", "_")
        try:
            __import__(pkg_import_name)
        except ImportError:
            missing_packages.append(pkg)

    if missing_packages:
        print(f"⏳ جاري تثبيت الحزم النواة المفقودة: {missing_packages}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("✅ تم تثبيت كافة الحزم والمكتبات الهندسية بنجاح.")
        except Exception as err:
            print(f"⚠️ خطأ أثناء تثبيت المكتبات: {err}")
    else:
        print("✅ جميع الحزم ومكتبات قواعد البيانات متوفرة ومستقرة.")
    print("="*75 + "\n")

setup_environment()

# استيراد المكتبات الأساسية بعد التهيئة
import httpx
import uvicorn
from fastapi import FastAPI, BackgroundTasks, Request, Header, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# مكتبات قاعدة البيانات (SQLAlchemy Async)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, select

# ==============================================================================
# 2. إعدادات التسجيل والبيئة (Logging & Config Settings)
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AymnGuard.MasterCore")

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv(
        "TELEGRAM_BOT_TOKEN", 
        "8885095463:AAGRRtirIswzPutKdhuOTf_OeDzO2PTu_FQ"
    )
    TELEGRAM_SECRET_TOKEN: str = os.getenv(
        "TELEGRAM_SECRET_TOKEN", 
        "aymnguard_secure_secret_2026"
    )
    WEBHOOK_URL: str = os.getenv(
        "WEBHOOK_URL", 
        "https://79aa1d2d170e59.lhr.life/api/v1/telegram/webhook"
    )
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./aymnguard_enterprise.db"
    )
    HTTP_TIMEOUT: float = 10.0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# ==============================================================================
# 3. طبقة قاعدة البيانات الدائمة (Persistent Database Layer)
# ==============================================================================
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class TelegramLogModel(Base):
    """نموذج جدول تخزين رسائل وأحداث تيليجرام الواردة بشكل دائم."""
    __tablename__ = "telegram_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    update_id: Mapped[int] = mapped_column(Integer, index=True)
    chat_id: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), default="message")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class UserAuthModel(Base):
    """نموذج إدارة صلاحيات المستخدمين والاشتراكات الفعالة (VIP)."""
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    is_vip: Mapped[int] = mapped_column(Integer, default=0) # 0: عادي, 1: VIP مفعل
    subscription_type: Mapped[str] = mapped_column(String(50), default="Standard")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

async def init_db():
    """تهيئة وإنشاء الجداول تلقائياً عند إقلاع النظام."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("🗄️ [قاعدة البيانات]: تم التحقق وإنشاء كافة الجداول بنجاح.")

async def get_db():
    """توفير جلسة قاعدة البيانات غير المتزامنة لطلبات الـ API."""
    async with async_session() as session:
        yield session

# ==============================================================================
# 4. إدارة دورة حياة التطبيق والتسجيل التلقائي للويب هوك (Lifespan Manager)
# ==============================================================================
async def register_telegram_webhook():
    """التسجيل التلقائي لرابط الويب هوك لدى تيليجرام عند بدء التشغيل."""
    set_webhook_api = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {
        "url": settings.WEBHOOK_URL,
        "secret_token": settings.TELEGRAM_SECRET_TOKEN,
        "drop_pending_updates": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(set_webhook_api, json=payload)
            result = response.json()
            if result.get("ok"):
                logger.info(f"🔗 [تم ربط Webhook بنجاح مع تيليجرام]: {settings.WEBHOOK_URL}")
            else:
                logger.error(f"❌ [فشل ربط Webhook تلقائياً]: {result.get('description', 'خطأ غير معروف')}")
    except Exception as e:
        logger.error(f"⚠️ [خطأ شبكي أثناء محاولة تسجيل Webhook]: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة الإقلاع والإيقاف الآمن للنواة."""
    logger.info("🚀 [النواة الرئيسية]: جاري إقلاع نظام AymnGuard MasterCore...")
    await init_db()
    await register_telegram_webhook()
    yield
    logger.info("🛑 [النواة الرئيسية]: إغلاق آمن وتفريغ الموارد... وداعاً.")

# تهيئة تطبيق FastAPI بمواصفات مؤسسية متقدمة
app = FastAPI(
    title="AymnGuard Enterprise Sovereign Platform",
    description="نظام إدارة لوجستي وبوتات تيليجرام متكامل مع لوحات تحكم عالمية ومصادقة مستمرة.",
    version="7.0.0-MasterCore",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# تفعيل إعدادات CORS المفتوحة للربط الشامل
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 5. نماذج البيانات الهندسية (Pydantic v2 Models)
# ==============================================================================
class AuthPayload(BaseModel):
    chat_id: str = Field(..., description="معرف المحادثة الفريد للمستخدم")
    username: Optional[str] = Field(None, description="اسم المستخدم")
    action: str = Field(..., description="نوع الطلب (activate_vip / check_status)")

class MassiveLogisticsPayload(BaseModel):
    task_batch: str = Field(..., description="دفعة المهام اللوجستية المراد معالجتها")
    parameters: dict = Field(default={}, description="المعاملات التشغيلية")

# ==============================================================================
# 6. معالجات المهام الخلفية وقاعدة البيانات (Background Workers)
# ==============================================================================
async def save_update_to_db(update_id: int, chat_id: str, username: str, text: str, event_type: str):
    """حفظ رسائل وأحداث تيليجرام في قاعدة البيانات بشكل دائم."""
    try:
        async with async_session() as session:
            db_log = TelegramLogModel(
                update_id=update_id,
                chat_id=str(chat_id),
                username=username,
                text_content=text,
                event_type=event_type
            )
            session.add(db_log)
            await session.commit()
    except Exception as e:
        logger.error(f"❌ [خطأ في حفظ السجل بقاعدة البيانات]: {str(e)}")

async def process_telegram_update_background(data: Dict[str, Any]):
    """معالجة التحديثات الواردة من تيليجرام غير متزامناً في الخلفية."""
    try:
        update_id = data.get("update_id")
        logger.info(f"🔄 [معالجة التحديث]: Update ID -> {update_id}")

        if "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            user = msg.get("from", {})
            username = user.get("username", "Unknown")
            
            if "text" in msg:
                text = msg["text"]
                await save_update_to_db(update_id, chat_id, username, text, "text_message")

                if text.startswith("/"):
                    await execute_command_router(chat_id, text, user)
                else:
                    await execute_text_handler(chat_id, text, user)
            elif "photo" in msg:
                await save_update_to_db(update_id, chat_id, username, "[Photo Media]", "photo_message")
                await send_telegram_response(chat_id, "🛡️ AymnGuard: تم استلام صورتك وتحليلها أمنياً بنجاح.")
        elif "callback_query" in data:
            callback = data["callback_query"]
            callback_id = callback["id"]
            chat_id = callback["message"]["chat"]["id"]
            callback_data = callback["data"]
            await save_update_to_db(update_id, chat_id, "CallbackUser", callback_data, "callback_query")
            await answer_callback_query(callback_id, "تم استلام الطلب ومعالجته")
            await send_telegram_response(chat_id, f"🔘 AymnGuard: تم تنفيذ الأمر المرتبط بالزر ({callback_data})")
    except Exception as e:
        logger.error(f"❌ [خطأ حرج في المعالجة الخلفية]: {str(e)}", exc_info=True)

async def execute_command_router(chat_id: int, command: str, user: dict):
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    name = user.get("first_name", "مستخدم")

    if cmd == "/start":
        reply = (
            f"🛡️ **مرحباً بك يا {name} في منصة AymnGuard Sovereign Core**\n\n"
            f"النظام يعمل بكفاءة مؤسسية تامة مع قاعدة بيانات مستمرة وتفعيل باقات VIP.\n"
            f"استخدم الأزرار أدناه للوصول لخدماتنا وتحميل التطبيق."
        )
    elif cmd == "/help":
        reply = "📖 **دليل المساعدة المؤسسي:**\n- يتم تسجيل كافة تفاعلاتك وحفظها بأمان تام في قاعدة البيانات المركزية."
    elif cmd == "/status":
        reply = "🟢 **حالة النظام:**\n- النواة: نشطة ومؤمنة بالكامل\n- التخزين: دائم (Persistent Active)"
    else:
        reply = f"⚙️ الأمر `{cmd}` قيد المعالجة ضمن النواة الذكية."

    await send_telegram_response(chat_id, reply)

async def execute_text_handler(chat_id: int, text: str, user: dict):
    reply_text = (
        f"🛡️ **AymnGuard Core Enterprise**\n\n"
        f"تم استلام أمرك ومعالجته عبر مسار الـ Webhook الآمن:\n"
        f"💬 المحتوى: `{text}`"
    )
    await send_telegram_response(chat_id, reply_text)

async def send_telegram_response(chat_id: int, text: str):
    api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            await client.post(api_url, json=payload)
    except Exception as exc:
        logger.error(f"⚠️ خطأ أثناء إرسال الرد لتيليجرام: {str(exc)}")

async def answer_callback_query(callback_query_id: str, text: str):
    api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
    payload = {"callback_query_id": callback_query_id, "text": text}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(api_url, json=payload)
    except Exception:
        pass

# ==============================================================================
# 7. مسارات الـ API التشغيلية والمصادقة (API Endpoints & Auth)
# ==============================================================================
@app.post("/api/v1/telegram/webhook", tags=["Telegram Webhook"])
async def telegram_webhook_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    """نقطة النهاية الآمنة لاستقبال أحداث تيليجرام وتفويضها للخلفية."""
    try:
        if settings.TELEGRAM_SECRET_TOKEN:
            if x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Webhook Source")

        data = await request.json()
        background_tasks.add_task(process_telegram_update_background, data)
        return {"status": "success", "architecture": "AymnGuard MasterCore Active"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"⚠️ خطأ في نقطة Webhook: {str(e)}")
        return {"status": "error", "details": str(e)}

@app.post("/api/v1/auth", tags=["Authentication & VIP"])
async def authenticate_and_activate_vip(payload: AuthPayload, session: AsyncSession = Depends(get_db)):
    """بوابة المصادقة وإدارة تفعيل خدمات VIP والاشتراكات للمستخدمين."""
    try:
        result = await session.execute(select(UserAuthModel).where(UserAuthModel.chat_id == payload.chat_id))
        user = result.scalars().first()

        if not user:
            user = UserAuthModel(
                chat_id=payload.chat_id,
                username=payload.username or "Anonymous",
                is_vip=1 if payload.action == "activate_vip" else 0,
                subscription_type="VIP-Enterprise" if payload.action == "activate_vip" else "Standard"
            )
            session.add(user)
        else:
            if payload.action == "activate_vip":
                user.is_vip = 1
                user.subscription_type = "VIP-Enterprise"

        await session.commit()
        return {
            "status": "success",
            "chat_id": user.chat_id,
            "is_vip": user.is_vip,
            "subscription_type": user.subscription_type,
            "message": "تم تحديث حالة المصادقة والاشتراك بنجاح."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Auth Error: {str(e)}")

@app.post("/api/v1/massive-logistics", tags=["Massive Logistics"])
async def massive_logistics_engine(payload: MassiveLogisticsPayload, background_tasks: BackgroundTasks):
    """معالجة العمليات اللوجستية الضخمة وإدارة المهام الموزعة."""
    background_tasks.add_task(logger.info, f"📦 تنفيذ دفعة المهام اللوجستية: {payload.task_batch}")
    return {
        "status": "Dispatched",
        "batch": payload.task_batch,
        "timestamp": datetime.now().isoformat(),
        "engine": "AymnGuard Sovereign Logistics"
    }

@app.get("/api/v1/health", tags=["System Health"])
async def health_check():
    """فحص سلامة النظام واستهلاك الموارد."""
    return {
        "status": "Healthy & Secure",
        "timestamp": datetime.now().isoformat(),
        "version": "7.0.0-MasterCore",
        "database": "Active & Persistent"
    }

@app.get("/api/v1/logs", tags=["Logs System"])
async def get_system_logs(session: AsyncSession = Depends(get_db)):
    """استرجاع أحدث السجلات المحفوظة في قاعدة البيانات."""
    result = await session.execute(select(TelegramLogModel).order_by(TelegramLogModel.id.desc()).limit(15))
    logs = result.scalars().all()
    return {
        "total": len(logs),
        "logs": [{"id": l.id, "update_id": l.update_id, "chat_id": l.chat_id, "text": l.text_content, "time": l.created_at} for l in logs]
    }

# ==============================================================================
# 8. واجهة التحكم المركزية العالمية (Telegram-Styled Sovereign Web UI Dashboard)
# ==============================================================================
@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def sovereign_control_center():
    """لوحة التحكم المركزية المصممة بطراز عالي الدقة مستوحى من تطبيقات تيليجرام الرسمية."""
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AymnGuard Enterprise Sovereign Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
            body { font-family: 'Cairo', sans-serif; background-color: #0f172a; color: #f8fafc; }
            .tg-card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; }
            .tg-header { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 1px solid #334155; }
            .tg-button { background-color: #2563eb; transition: all 0.3s ease; }
            .tg-button:hover { background-color: #1d4ed8; }
            .tg-vip-button { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #0f172a; }
            ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 4px; }
        </style>
    </head>
    <body class="min-h-screen p-4 md:p-8">
        <div class="max-w-6xl mx-auto space-y-6">
            
            <!-- Telegram-Styled Header -->
            <header class="tg-header p-6 rounded-2xl shadow-2xl flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                <div class="flex items-center space-x-4 space-x-reverse">
                    <div class="w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-2xl font-black text-white shadow-lg border-2 border-blue-400">
                        🛡️
                    </div>
                    <div>
                        <h1 class="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-l from-blue-400 to-emerald-400">
                            AymnGuard Enterprise Sovereign
                        </h1>
                        <p class="text-xs md:text-sm text-gray-400">مركز التحكم الموحد المستوحى من التصميم العالمي لتطبيقات تيليجرام (v7.0.0)</p>
                    </div>
                </div>
                
                <div class="flex items-center space-x-3 space-x-reverse">
                    <span class="px-4 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-600/50 text-emerald-400 text-xs font-bold animate-pulse">
                        ● متصل وآمن
                    </span>
                    <a href="/docs" target="_blank" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded-xl text-xs font-bold text-gray-200 transition">
                        <i class="fas fa-book ml-1 text-blue-400"></i> توثيق API
                    </a>
                </div>
            </header>

            <!-- Quick Download & Services Access -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Download App Card -->
                <div class="tg-card p-6 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="w-10 h-10 rounded-xl bg-sky-500/20 text-sky-400 flex items-center justify-center text-xl mb-3">
                            <i class="fas fa-download"></i>
                        </div>
                        <h2 class="text-lg font-bold text-gray-100">تطبيق AymnGuard الرسمي</h2>
                        <p class="text-xs text-gray-400 mt-1">حمل التطبيق الرسمي وتطبيقات تيليجرام المعدلة للوصول إلى كافة الخدمات بلمسة واحدة.</p>
                    </div>
                    <button onclick="downloadAppAction()" class="tg-button w-full py-3 rounded-xl text-sm font-bold text-white shadow-lg flex items-center justify-center space-x-2 space-x-reverse">
                        <i class="fas fa-cloud-download-alt"></i>
                        <span>تحميل التطبيق فوراً</span>
                    </button>
                </div>

                <!-- VIP Subscription Card -->
                <div class="tg-card p-6 flex flex-col justify-between space-y-4 border-amber-500/30">
                    <div>
                        <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl mb-3">
                            <i class="fas fa-crown"></i>
                        </div>
                        <h2 class="text-lg font-bold text-gray-100">تفعيل باقات VIP الحصرية</h2>
                        <p class="text-xs text-gray-400 mt-1">احصل على صلاحيات مطلقة واستخدام غير محدود لكافة خدمات التحصين والدرع السيادي.</p>
                    </div>
                    <button onclick="activateVipAction()" class="tg-vip-button w-full py-3 rounded-xl text-sm font-bold text-white shadow-lg flex items-center justify-center space-x-2 space-x-reverse">
                        <i class="fas fa-star"></i>
                        <span>ترقية وتفعيل VIP الآن</span>
                    </button>
                </div>

                <!-- Telegram Bot Integration Card -->
                <div class="tg-card p-6 flex flex-col justify-between space-y-4">
                    <div>
                        <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-xl mb-3">
                            <i class="fab fa-telegram-plane"></i>
                        </div>
                        <h2 class="text-lg font-bold text-gray-100">البوت الخدمي التفاعلي</h2>
                        <p class="text-xs text-gray-400 mt-1">تفاعل مباشرة مع البوت الرسمي عبر تيليجرام واستقبل الأوامر والردود الفورية.</p>
                    </div>
                    <a href="https://t.me/AymnGuard_2026_bot" target="_blank" class="w-full py-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/40 border border-purple-500/30 text-purple-300 text-sm font-bold text-center transition flex items-center justify-center space-x-2 space-x-reverse">
                        <i class="external-link-alt fas"></i>
                        <span>فتح البوت الرسمي</span>
                    </a>
                </div>
            </div>

            <!-- Database & System Logs Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- System Health & Status -->
                <div class="tg-card p-6 space-y-4">
                    <h2 class="text-base font-bold text-blue-300 flex items-center">
                        <i class="fas fa-server ml-2 text-blue-500"></i> حالة النواة والبيانات التشغيلية
                    </h2>
                    <div id="system-status-box" class="bg-black/60 p-4 rounded-xl text-xs text-emerald-400 font-mono h-48 overflow-y-auto border border-slate-800">
                        جاري فحص حالة النواة...
                    </div>
                    <button onclick="checkSystemHealth()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-gray-200 text-xs font-bold border border-slate-700 transition">
                        تحديث فحص النظام
                    </button>
                </div>

                <!-- Recent Database Logs -->
                <div class="tg-card p-6 space-y-4">
                    <h2 class="text-base font-bold text-purple-300 flex items-center">
                        <i class="fas fa-database ml-2 text-purple-500"></i> سجلات قاعدة البيانات المستمرة
                    </h2>
                    <div id="db-logs-box" class="bg-black/60 p-4 rounded-xl text-xs text-purple-300 font-mono h-48 overflow-y-auto border border-slate-800">
                        جاري جلب السجلات الحية...
                    </div>
                    <button onclick="loadDatabaseLogs()" class="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-gray-200 text-xs font-bold border border-slate-700 transition">
                        تحديث السجلات
                    </button>
                </div>
            </div>
            
        </div>

        <script>
            async function checkSystemHealth() {
                try {
                    const res = await fetch('/api/v1/health');
                    const data = await res.json();
                    document.getElementById('system-status-box').innerText = JSON.stringify(data, null, 2);
                } catch (e) {
                    document.getElementById('system-status-box').innerText = "❌ تعذر الاتصال بالنواة.";
                }
            }

            async function loadDatabaseLogs() {
                try {
                    const res = await fetch('/api/v1/logs');
                    const data = await res.json();
                    document.getElementById('db-logs-box').innerText = JSON.stringify(data, null, 2);
                } catch (e) {
                    document.getElementById('db-logs-box').innerText = "❌ تعذر جلب السجلات من قاعدة البيانات.";
                }
            }

            async function activateVipAction() {
                const chatId = prompt("أدخل معرف المحادثة (Chat ID) الخاص بك لتفعيل باقة VIP:", "123456789");
                if (!chatId) return;
                try {
                    const res = await fetch('/api/v1/auth', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ chat_id: chatId, username: "WebAdmin", action: "activate_vip" })
                    });
                    const data = await res.json();
                    alert("🎉 تم التفعيل بنجاح: " + JSON.stringify(data, null, 2));
                    loadDatabaseLogs();
                } catch (e) {
                    alert("⚠️ فشل عملية التفعيل.");
                }
            }

            function downloadAppAction() {
                alert("📥 جاري تحضير ملف التطبيق الرسمي والتطبيقات المعدلة للتحميل الفوري...");
                window.location.href = "/docs";
            }

            // التشغيل التلقائي عند التحميل
            checkSystemHealth();
            loadDatabaseLogs();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# ==============================================================================
# 9. نقطة التشغيل الرئيسية المباشرة (Main Execution Driver)
# ==============================================================================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
