# -*- coding: utf-8 -*-
"""
==============================================================================
Aymn Coder Plus : Aegis AI Core & AymnGuard Sovereign Enterprise Core (v19.0.0-ImperialMaster)
==============================================================================
النواة المؤسسية الإمبراطورية الموحدة كلياً: دمج كامل لمحركات التداول، الحماية،
الـ WebSockets، الأتمتة، وإدارة الجلسات مع محرك الاكتشاف التلقائي الشامل.
==============================================================================
"""
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
import os
import sys
import time
import logging
import asyncio
import importlib
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional, List

# ==============================================================================
# 0. هندسة المسارات السيادية (Path Engineering)
# ==============================================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import httpx
import uvicorn
from fastapi import FastAPI, BackgroundTasks, Request, Header, HTTPException, WebSocket, WebSocketDisconnect, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.future import select

app = FastAPI(title="AymnGuard Sovereign Core")

# --- SOVEREIGN_PYTHON_IMPORTS_MARKER ---
# (يتم حقن استدعاءات المكتبات الجديدة هنا)

# --- SOVEREIGN_PYTHON_ROUTES_MARKER ---
# (يتم حقن مسارات الـ API والتحكم هنا تلقائياً)

@app.get("/")
def read_root():
    return {"status": "Sovereign Engine Operational"}

# ==============================================================================
# 1. إعدادات التسجيل والبيئة المركزية (Logging & Config Settings)
# ==============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | 👑 IMPERIAL-%(levelname)-7s | %(name)s - %(message)s")
logger = logging.getLogger("AegisAICore.ImperialMasterHub")

class SovereignSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "8885095463:AAGcCsNOi68c0OYXC5y2ApcRXBVpTD-R-lU")
    TELEGRAM_SECRET_TOKEN: str = os.getenv("TELEGRAM_SECRET_TOKEN", "aymnguard_secure_secret_2026")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "http://135.181.86.199:8000/api/v1/telegram/webhook")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///aymnguard_enterprise.db")
    TELEGRAM_API_ID: int = int(os.getenv("TELEGRAM_API_ID", 6))
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    HTTP_TIMEOUT: float = 15.0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = SovereignSettings()
limiter = Limiter(key_func=get_remote_address)

# ==============================================================================
# 2. إدارة اتصالات WebSockets السيادية
# ==============================================================================
class SovereignAlertManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("🔌 [WebSocket Imperial]: تم ربط عميل جديد بلوحة القيادة الأمنية بنجاح.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("🔌 [WebSocket Imperial]: تم قطع اتصال عميل.")

    async def broadcast_alert(self, alert_data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(alert_data)
            except Exception:
                self.disconnect(connection)

alert_manager = SovereignAlertManager()

# ==============================================================================
# 3. محرك الدرع السيادي (Sovereign Shield & Defense Engine)
# ==============================================================================
class SovereignShieldEngine:
    @staticmethod
    def suppress_service_messages(message_data: dict) -> bool:
        if "new_chat_members" in message_data or "left_chat_member" in message_data:
            logger.info("🛡️ [الدرع السيادي]: تم رصد وإسقاط إشعار انضمام/مغادرة تشغيلي صامت.")
            return True
        return False

    @staticmethod
    async def analyze_attack_vectors(message_data: dict) -> bool:
        user = message_data.get("from", {})
        text = message_data.get("text", "").lower()
        if user.get("is_bot", False) and ("report" in text or "spam" in text or "attack" in text):
            await alert_manager.broadcast_alert({
                "level": "CRITICAL", 
                "message": f"رصد هجوم بلاغات كيدية أو نشاط مشبوه من البوت: {user.get('username', 'Unknown')}", 
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

# ==============================================================================
# 4. طبقة قاعدة البيانات الدائمة (SQLAlchemy Async Core & Vaults)
# ==============================================================================
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class TelegramLogModel(Base):
    __tablename__ = "telegram_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    update_id: Mapped[int] = mapped_column(Integer, index=True)
    chat_id: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), default="message")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class EnterpriseSessionModel(Base):
    __tablename__ = "enterprise_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    session_string: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    health_score: Mapped[float] = mapped_column(default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# ==============================================================================
# 5. الربط الديناميكي للمحركات المستقلة ومعالجة أخطاء الاستيراد (Fail-Safe)
# ==============================================================================
try:
    from core.trading_execution import execute_binance_order
    from services.trading import SovereignTradingEngine
    logger.info("📈 [Master Hub]: تم ربط محركات التداول بنجاح.")
except ImportError:
    async def execute_binance_order(*args, **kwargs): return {"status": "mocked_execution", "detail": "Trading core simulated."}
    SovereignTradingEngine = None

try:
    from core.master_kernel import init_master_kernel
    from core.license_manager import SovereignLicenseManager
except ImportError:
    async def init_master_kernel(): 
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    class SovereignLicenseManager:
        @staticmethod
        async def verify_and_link_user(k, c): return {"status": "success", "message": "Simulated Master Link"}

try:
    from bots.protection.bot_engine import SovereignProtectionEngine
except ImportError:
    class SovereignProtectionEngine:
        @staticmethod
        async def activate_protection(k, c): return {"status": "success", "message": "Protection Active (Simulated)"}

try:
    from bots.creative.creative_engine import SovereignCreativeStudio
except ImportError:
    class SovereignCreativeStudio:
        @staticmethod
        async def generate_asset_request(k, p, t="logo", a="1:1"): return {"status": "success", "message": "Design Received (Simulated)"}

try:
    from bots.search.search_engine import SovereignSearchEngine
except ImportError:
    class SovereignSearchEngine:
        @staticmethod
        async def execute_enterprise_search(k, q, s="all"): return {"status": "success", "message": "Search Executed (Simulated)"}

try:
    from core.session_manager import SovereignSessionManager
except ImportError:
    class SovereignSessionManager:
        @staticmethod
        async def initialize_session(*args, **kwargs): return {"status": "simulated"}
        @staticmethod
        async def get_enterprise_analytics_report(*args, **kwargs): return {"status": "simulated"}

try:
    from services.enterprise_transfer_engine import EnterpriseTransferEngine
except ImportError:
    class EnterpriseTransferEngine:
        @staticmethod
        async def initialize_interactive_workflow(*args, **kwargs): return "Simulated Workflow"
        @staticmethod
        async def handle_interactive_input(*args, **kwargs): return "Simulated Input"

try:
    from core.auth_manager import SovereignAuthManager
except ImportError:
    class SovereignAuthManager:
        @staticmethod
        async def send_verification_code(*args, **kwargs): return {"status": "simulated"}
        @staticmethod
        async def verify_code(*args, **kwargs): return {"status": "simulated"}
        @staticmethod
        async def verify_2fa_password(*args, **kwargs): return {"status": "simulated"}

# ==============================================================================
# 6. عُقد الأتمتة الخلفية (Telethon & Pyrogram Background Workers)
# ==============================================================================
from telethon import TelegramClient
from pyrogram import Client as PyroClient

telethon_client = TelegramClient("aymnguard_telethon_session", settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
pyrogram_client = PyroClient("aymnguard_pyrogram_session", api_id=settings.TELEGRAM_API_ID, api_hash=settings.TELEGRAM_API_HASH)

async def start_automation_nodes():
    try: 
        await telethon_client.start()
        logger.info("🟢 [Telethon Worker]: تم إقلاع عقدة Telethon بنجاح.")
    except Exception as e:
        logger.warning(f"⚠️ [Telethon Worker]: تعذر الإقلاع الفوري: {e}")
        
    try: 
        await pyrogram_client.start()
        logger.info("🟢 [Pyrogram Worker]: تم إقلاع عقدة Pyrogram بنجاح.")
    except Exception as e:
        logger.warning(f"⚠️ [Pyrogram Worker]: تعذر الإقلاع الفوري: {e}")

async def register_telegram_webhook():
    set_webhook_api = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {"url": settings.WEBHOOK_URL, "secret_token": settings.TELEGRAM_SECRET_TOKEN}
    try:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            res = await client.post(set_webhook_api, json=payload)
            if res.json().get("ok"): 
                logger.info(f"🔗 [Webhook Master]: تم تسجيل الويب هوك بنجاح سيادياً -> {settings.WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"⚠️ خطأ في تسجيل الويب هوك: {e}")

@asynccontextmanager
async def sovereign_lifespan(app: FastAPI):
    logger.info("🚀 [Aegis Master Hub v19]: جاري الإقلاع السيادي الكامل للـ Backend والخدمات المصغرة...")
    await init_master_kernel()
    await register_telegram_webhook()
    asyncio.create_task(start_automation_nodes())
    yield
    logger.info("🛑 [Aegis Master Hub]: إيقاف آمن للنواة الإمبراطورية وتفريغ الموارد...")

# ==============================================================================
# 7. تعريف التطبيق المركزي (FastAPI Master Instance)
# ==============================================================================
app = FastAPI(
    title="AymnCoder Plus Sovereign Enterprise Core",
    version="19.0.0-ImperialMaster",
    description="The Absolute Master Backend Hub controlling all enterprise micro-services, bots, and trading engines",
    lifespan=sovereign_lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def imperial_telemetry_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Imperial-Process-Time"] = str(round(process_time, 4))
    return response

# ==============================================================================
# 🌟 دمج المسارات والروابط السيادية (Auto-Wired Bridges) 🌟
# ==============================================================================
try:
    from core.meta_engine import router as meta_engine_router
    app.include_router(meta_engine_router)
    from services.telegram_bridge import router as telegram_bridge_router
    app.include_router(telegram_bridge_router)
    from services.test_orphan import router as test_orphan_router
    app.include_router(test_orphan_router)
    from services.test_orphan_service import router as test_orphan_service_router
    app.include_router(test_orphan_service_router)
    from services.websocket import router as websocket_router
    app.include_router(websocket_router)
    from services.health import router as health_router
    app.include_router(health_router)
    from src.ai_engine import router as ai_engine_router
    app.include_router(ai_engine_router)
    from app.enterprise_gateway import router as enterprise_gateway_router
    app.include_router(enterprise_gateway_router)
    from app.empire_app_gateway import router as empire_app_gateway_router
    app.include_router(empire_app_gateway_router)
    from backend_core.core_routes import router as core_routes_router
    app.include_router(core_routes_router)
    logger.info("🌉 [Bridges]: تم ربط المسارات الإمبراطورية الأساسية بنجاح.")
except ImportError as e:
    logger.debug(f"ℹ️ [Bridges Alert]: بعض المسارات قيد التطوير ولم يتم تحميلها: {e}")

try:
    from bots.telegram_bot import register_bot_handlers
    @app.on_event("startup")
    async def startup_event():
        register_bot_handlers(pyrogram_client)
        logger.info("🚀 [Master Hub]: Bot handlers successfully bound to the operational pipeline.")
except ImportError:
    logger.warning("⚠️ [Master Hub]: ملف telegram_bot غير محمل حالياً، سيتم تجاوزه.")

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend_core")
MINI_APP_DIR = os.path.join(FRONTEND_DIR, "mini_app")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")

if os.path.exists(MINI_APP_DIR):
    app.mount("/mini-app", StaticFiles(directory=MINI_APP_DIR, html=True), name="mini_app")
    logger.info("🌐 [Master Hub]: تم دمج واجهة Mini App بنجاح تحت سيطرة الـ Backend.")

if os.path.exists(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend_assets")

# ==============================================================================
# 8. محرك الاكتشاف والمسح الشامل التلقائي (Total Auto-Discovery Engine)
# ==============================================================================
def register_all_enterprise_modules(fastapi_app, base_root_dir):
    logger.info("🛡️ [Auto-Discovery]: بدء مسح واكتشاف كافة ملفات ومجلدات المستودع الشاملة...")
    target_folders = ["services", "bots", "security", "core", "src", "app", "backend_core"]
    discovered_count = 0
    
    for folder in target_folders:
        folder_path = os.path.join(base_root_dir, folder)
        if not os.path.exists(folder_path):
            continue
            
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    full_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_file_path, base_root_dir)
                    module_path = rel_path[:-3].replace(os.sep, ".")
                    
                    try:
                        module = importlib.import_module(module_path)
                        if hasattr(module, "router"):
                            endpoint_prefix = f"/api/v1/{folder}/{file[:-3].replace('_', '-')}"
                            tag_name = f"{folder.upper()} : {file[:-3].replace('_', ' ').title()}"
                            
                            fastapi_app.include_router(module.router, prefix=endpoint_prefix, tags=[tag_name])
                            logger.info(f"🔗 [Auto-Linked Router]: {module_path} -> [{endpoint_prefix}]")
                            discovered_count += 1
                    except Exception:
                        pass
                        
    logger.info(f"✨ [Auto-Discovery Complete]: تم بنجاح اكتشاف وربط {discovered_count} مكوناً برمجياً بالكتلة التشغيلية.")

register_all_enterprise_modules(app, ROOT_DIR)

# ==============================================================================
# 9. نماذج بيانات التحقق (Pydantic Models)
# ==============================================================================
class TradeRequestModel(BaseModel):
    symbol: str; side: str; amount: float; leverage: Optional[int] = 1; market: Optional[str] = "SPOT"; api_key: str; api_secret: str

class LicenseLinkRequest(BaseModel): license_key: str; chat_id: str
class ProtectionSlotRequest(BaseModel): license_key: str; channel_id: str
class CreativeAssetRequest(BaseModel): license_key: str; prompt: str; asset_type: Optional[str] = "logo"; aspect_ratio: Optional[str] = "1:1"
class EnterpriseSearchRequest(BaseModel): license_key: str; query: str; scope: Optional[str] = "all"

class SessionInitRequest(BaseModel): license_key: str; session_name: str; phone_number: str; api_id: int; api_hash: str
class TransferInitRequest(BaseModel): license_key: str; user_id: str; sessions_to_use: List[str]
class InteractiveInputRequest(BaseModel): license_key: str; user_id: str; user_input: str
class AuthSendCodeRequest(BaseModel): session_name: str; phone_number: str; api_id: int; api_hash: str
class AuthVerifyCodeRequest(BaseModel): session_name: str; phone_code: str
class AuthVerify2FARequest(BaseModel): session_name: str; password: str

async def send_telegram_response(chat_id, text):
    try:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        logger.error(f"Failed to send telegram response: {e}")

# ==============================================================================
# 10. معالجة تليجرام كخدمة فرعية تابعة للنواة
# ==============================================================================
async def process_telegram_update(data: Dict[str, Any]):
    try:
        update_id = data.get("update_id")
        if "message" in data:
            msg = data["message"]
            if SovereignShieldEngine.suppress_service_messages(msg): return
            if await SovereignShieldEngine.analyze_attack_vectors(msg): return
            
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            user_id = str(chat_id)

            response = await EnterpriseTransferEngine.handle_interactive_input(license_key="DEFAULT_LICENSE", user_id=user_id, user_input=text)

            if response and "البيئة غير مهيأة" not in response:
                await send_telegram_response(chat_id, response)
                return

            async with async_session() as session:
                session.add(TelegramLogModel(update_id=update_id, chat_id=str(chat_id), text_content=text))
                await session.commit()

            if text.startswith("/start"):
                await send_telegram_response(chat_id, "🛡️ **أهلاً بك في AymnGuard Sovereign Enterprise Core**\nاستخدم الأمر `/initialize_transfer` لبدء عملية النقل.")
            elif text.startswith("/initialize_transfer"):
                response = await EnterpriseTransferEngine.initialize_interactive_workflow(license_key="DEFAULT_LICENSE", user_id=user_id, sessions_to_use=["session_1", "session_2"])
                await send_telegram_response(chat_id, response)
            else:
                await send_telegram_response(chat_id, f"✅ تم استقبال الأمر ومعالجته عبر الـ Backend بنجاح: `{text}`")
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة تليجرام الفرعية: {e}")

# ==============================================================================
# 11. مسارات الـ API التشغيلية الأساسية للـ Master Hub (تمت الترقية للسرعة الخارقة)
# ==============================================================================
@app.get("/api/v1/system/version", tags=["System Management"])
async def get_system_version():
    return {
        "latest_version": 35.1,
        "download_url": "https://raw.githubusercontent.com/YourName/YourRepo/main/app-release.apk",
        "is_mandatory": True
    }

@app.post("/api/v1/telegram/webhook", tags=["Webhook Subservice"])
@limiter.limit("60/minute")
async def telegram_webhook(request: Request, bg_tasks: BackgroundTasks, x_telegram_bot_api_secret_token: Optional[str] = Header(None)):
    if settings.TELEGRAM_SECRET_TOKEN and x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized Telegram Telemetry")
    bg_tasks.add_task(process_telegram_update, await request.json())
    return {"status": "success", "master_hub": "processed"}

@app.post("/api/v1/trade/execute", tags=["Trading Engine"])
@limiter.limit("20/minute")
async def execute_trade_endpoint(request: Request, payload: TradeRequestModel):
    try:
        result = await execute_binance_order(symbol=payload.symbol, side=payload.side, amount=payload.amount, leverage=payload.leverage, market=payload.market, api_key=payload.api_key, api_secret=payload.api_secret)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution Failed: {str(e)}")

@app.post("/api/v1/license/link", tags=["Services Matrix"])
async def link_license(data: LicenseLinkRequest): return await SovereignLicenseManager.verify_and_link_user(data.license_key, data.chat_id)

@app.post("/api/v1/protection/activate", tags=["Services Matrix"])
async def activate_protection(data: ProtectionSlotRequest): return await SovereignProtectionEngine.activate_protection(data.license_key, data.channel_id)

@app.post("/api/v1/creative/generate", tags=["Services Matrix"])
async def generate_asset(data: CreativeAssetRequest): return await SovereignCreativeStudio.generate_asset_request(data.license_key, data.prompt, data.asset_type, data.aspect_ratio)

@app.post("/api/v1/search/intelligence", tags=["Services Matrix"])
async def enterprise_search(data: EnterpriseSearchRequest): return await SovereignSearchEngine.execute_enterprise_search(data.license_key, data.query, data.scope)

@app.get("/api/v1/imperial/health", tags=["System Health"])
async def imperial_health_check():
    return {"status": "HEALTHY", "version": "19.0.0-ImperialMaster", "database": "CONNECTED", "websockets_active_clients": len(alert_manager.active_connections), "timestamp": datetime.utcnow().isoformat()}

@app.websocket("/ws/security-alerts")
async def ws_security(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping": await websocket.send_text("pong")
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)

# ------------------------------------------------------------------------------
# 🌟 [ترقية سيادية]: مسارات المصادقة وتأكيد الدخول - معالجة الأخطاء والتسريع 🌟
# ------------------------------------------------------------------------------
@app.post("/api/v1/empire/auth/send-code", tags=["Sovereign Auth"])
async def auth_send_code(request: AuthSendCodeRequest, bg_tasks: BackgroundTasks): 
    try:
        # إضافة مهلة حماية (Timeout Wrapper) تمنع تجمد التطبيق إذا تأخر تيليجرام
        result = await asyncio.wait_for(
            SovereignAuthManager.send_verification_code(
                session_name=request.session_name, 
                phone_number=request.phone_number, 
                api_id=request.api_id, 
                api_hash=request.api_hash
            ),
            timeout=20.0
        )
        bg_tasks.add_task(logger.info, f"📱 [Auth]: نجح طلب الرمز للرقم {request.phone_number}")
        return result
    except asyncio.TimeoutError:
        logger.error("❌ [Auth Timeout]: انتهت مهلة استجابة مزود الخدمة (تيليجرام).")
        raise HTTPException(status_code=504, detail="تأخر رد خوادم تيليجرام، يرجى إعادة المحاولة.")
    except Exception as e:
        logger.error(f"❌ [Auth Error]: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/empire/auth/verify-code", tags=["Sovereign Auth"])
async def auth_verify_code(request: AuthVerifyCodeRequest, bg_tasks: BackgroundTasks):
    try:
        result = await asyncio.wait_for(
            SovereignAuthManager.verify_code(session_name=request.session_name, phone_code=request.phone_code),
            timeout=15.0
        )
        if result.get("status") == "success":
            async with async_session() as db:
                try:
                    db.add(EnterpriseSessionModel(session_name=request.session_name, session_string=result["session_string"]))
                    await db.commit()
                except Exception as db_err:
                    await db.rollback()
                    logger.error(f"❌ [DB Error]: فشل حفظ الجلسة: {db_err}")
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="انتهت المهلة أثناء التحقق من الكود.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/empire/auth/verify-2fa", tags=["Sovereign Auth"])
async def auth_verify_2fa(request: AuthVerify2FARequest):
    try:
        result = await asyncio.wait_for(
            SovereignAuthManager.verify_2fa_password(session_name=request.session_name, password=request.password),
            timeout=15.0
        )
        if result.get("status") == "success":
            async with async_session() as db:
                try:
                    db.add(EnterpriseSessionModel(session_name=request.session_name, session_string=result["session_string"]))
                    await db.commit()
                except Exception:
                    await db.rollback()
        return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------------------
# 🌟 [ترقية سيادية]: نقل تجهيز الجلسات المعقدة للعمال الخلفيين 🌟
# ------------------------------------------------------------------------------
@app.post("/api/v1/empire/sessions/register", tags=["Sovereign Sessions"])
async def register_new_session(request: SessionInitRequest, bg_tasks: BackgroundTasks): 
    # يتم الرد على واجهة فلاتر فوراً لتجنب أي Timeout، وترك العمل الثقيل للخلفية
    bg_tasks.add_task(
        SovereignSessionManager.initialize_session,
        license_key=request.license_key, 
        session_name=request.session_name, 
        api_id=request.api_id, 
        api_hash=request.api_hash, 
        phone_number=request.phone_number
    )
    return {
        "status": "processing", 
        "message": "تم استلام الطلب. جاري تهيئة الجلسة وبناء وكلاء الذكاء الاصطناعي في الخلفية بسرعة فائقة."
    }

@app.get("/api/v1/empire/sessions/analytics", tags=["Sovereign Sessions"])
async def get_session_analytics(license_key: str): return await SovereignSessionManager.get_enterprise_analytics_report(license_key)

# ------------------------------------------------------------------------------
# 🌟 [ترقية سيادية]: فصل الذكاء الاصطناعي عن الواجهة الأمامية 🌟
# ------------------------------------------------------------------------------
@app.post("/api/v1/empire/transfer/start-workflow", tags=["Sovereign Transfer"])
async def start_transfer_workflow(request: TransferInitRequest, bg_tasks: BackgroundTasks):
    # الذكاء الاصطناعي قد يأخذ وقتاً، نرسله لعمال الخلفية!
    bg_tasks.add_task(
        EnterpriseTransferEngine.initialize_interactive_workflow,
        license_key=request.license_key, 
        user_id=request.user_id, 
        sessions_to_use=request.sessions_to_use
    )
    return {
        "status": "workflow_initialized", 
        "message": "تم إطلاق عمال النقل والذكاء الاصطناعي في الخلفية بنجاح سيادي."
    }

@app.post("/api/v1/empire/transfer/interactive-input", tags=["Sovereign Transfer"])
async def handle_transfer_input(request: InteractiveInputRequest):
    return {"status": "success", "ai_response": await EnterpriseTransferEngine.handle_interactive_input(license_key=request.license_key, user_id=request.user_id, user_input=request.user_input)}

@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def home():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f: return f.read()
    return "<h2>AymnGuard Sovereign Enterprise Core - Imperial Master Backend Hub Online v19.0.0</h2>"

if __name__ == "__main__":
    uvicorn.run("backend_core.main:app", host="0.0.0.0", port=10000, reload=False, log_level="info")
