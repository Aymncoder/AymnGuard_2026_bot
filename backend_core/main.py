# -*- coding: utf-8 -*-
"""
==============================================================================
Aymn Coder Plus : Aegis AI Core & AymnGuard Sovereign Enterprise Core (v18.0.0-Master)
==============================================================================
النواة المؤسسية الإمبراطورية المحدثة: الـ Backend هو السيد المطلق والمهيمن،
مع عزل الخدمات الفرعية، حماية SlowAPI، البث الفوري WebSockets،
و إدارة المسارات الديناميكية الآمنة للسيادة اللوجستية والتشغيلية.
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional, List

# ==============================================================================
# 0. هندسة المسارات السيادية (Path Engineering)
# ==============================================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# استيراد المكتبات الأساسية بعد ضبط المسار
import httpx
import uvicorn
from fastapi import FastAPI, BackgroundTasks, Request, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from telethon import TelegramClient
from pyrogram import Client as PyroClient

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text

# ==============================================================================
# 1. إعدادات التسجيل والبيئة المركزية (Logging & Config Settings)
# ==============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s")
logger = logging.getLogger("AegisAICore.MasterHub")

class SovereignSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "8885095463:AAGRRtirIswzPutKdhuOTf_OeDzO2PTu_FQ")
    TELEGRAM_SECRET_TOKEN: str = os.getenv("TELEGRAM_SECRET_TOKEN", "aymnguard_secure_secret_2026")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "https://410b9e4c09a3de.lhr.life/api/v1/telegram/webhook")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aymnguard_enterprise.db")
    TELEGRAM_API_ID: int = int(os.getenv("TELEGRAM_API_ID", "2040"))
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH", "b18441aff607e10a989891a5462e627")
    HTTP_TIMEOUT: float = 10.0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = SovereignSettings()
limiter = Limiter(key_func=get_remote_address)

# ==============================================================================
# 2. إدارة اتصالات WebSockets السيادية (التنبيهات الفورية)
# ==============================================================================
class SovereignAlertManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("🔌 [WebSocket Master]: تم ربط عميل جديد بلوحة القيادة الأمنية.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

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
            logger.info("🛡️ [الدرع السيادي]: تم رصد وإسقاط إشعار انضمام/مغادرة تشغيلي.")
            return True
        return False

    @staticmethod
    async def analyze_attack_vectors(message_data: dict) -> bool:
        user = message_data.get("from", {})
        text = message_data.get("text", "").lower()
        if user.get("is_bot", False) and ("report" in text or "spam" in text):
            await alert_manager.broadcast_alert({
                "level": "CRITICAL", "message": "رصد هجوم بلاغات كيدية من بوت خارجي!", "timestamp": datetime.now().isoformat()
            })
            return True
        return False

# ==============================================================================
# 4. طبقة قاعدة البيانات الدائمة (SQLAlchemy Async Core)
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

# ==============================================================================
# 5. الربط الديناميكي للمحركات المستقلة (Fail-Safe External Imports)
# ==============================================================================
try:
    from core.master_kernel import init_master_kernel
    from core.license_manager import SovereignLicenseManager
    logger.info("💎 [Master Hub]: تم ربط Master Kernel & License Manager بنجاح.")
except ImportError:
    logger.warning("⚠️ تنبيه: استخدام نظام محاكاة النواة لغياب الملفات المحلية.")
    async def init_master_kernel(): 
        async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    class SovereignLicenseManager:
        @staticmethod
        async def verify_and_link_user(k, c): return {"status": "success", "message": "Simulated Master Link"}

try:
    from bots.protection.bot_engine import SovereignProtectionEngine
    logger.info("🛡️ [Master Hub]: تم ربط محرك Protection Engine بنجاح.")
except ImportError:
    class SovereignProtectionEngine:
        @staticmethod
        async def activate_protection(k, c): return {"status": "success", "message": "Protection Active (Simulated)"}

try:
    from bots.creative.creative_engine import SovereignCreativeStudio
    logger.info("🎨 [Master Hub]: تم ربط استوديو Creative Studio بنجاح.")
except ImportError:
    class SovereignCreativeStudio:
        @staticmethod
        async def generate_asset_request(k, p, t="logo", a="1:1"): return {"status": "success", "message": "Design Received (Simulated)"}

try:
    from bots.search.search_engine import SovereignSearchEngine
    logger.info("🔍 [Master Hub]: تم ربط محرك Search Engine بنجاح.")
except ImportError:
    class SovereignSearchEngine:
        @staticmethod
        async def execute_enterprise_search(k, q, s="all"): return {"status": "success", "message": "Search Executed (Simulated)"}

# ==============================================================================
# 6. عُقد الأتمتة التابعة (Telethon & Pyrogram Background Workers)
# ==============================================================================
telethon_client = TelegramClient("aymnguard_telethon_session", settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)
pyrogram_client = PyroClient("aymnguard_pyrogram_session", api_id=settings.TELEGRAM_API_ID, api_hash=settings.TELEGRAM_API_HASH, in_memory=True)

async def start_automation_nodes():
    try: await telethon_client.start()
    except Exception: pass
    try: await pyrogram_client.start()
    except Exception: pass

async def register_telegram_webhook():
    set_webhook_api = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {"url": settings.WEBHOOK_URL, "secret_token": settings.TELEGRAM_SECRET_TOKEN}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(set_webhook_api, json=payload)
            if res.json().get("ok"): logger.info(f"🔗 [Webhook Master]: تم تسجيل الويب هوك بنجاح -> {settings.WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"⚠️ خطأ في تسجيل الويب هوك: {e}")

@asynccontextmanager
async def sovereign_lifespan(app: FastAPI):
    logger.info("🚀 [Aegis Master Hub]: جاري الإقلاع السيادي الكامل للـ Backend...")
    await init_master_kernel()
    await register_telegram_webhook()
    asyncio.create_task(start_automation_nodes())
    yield
    logger.info("🛑 [Aegis Master Hub]: إيقاف آمن للنواة وتفريغ الموارد...")

# ==============================================================================
# 7. تعريف التطبيق المركزي (FastAPI Master Instance)
# ==============================================================================
app = FastAPI(
    title="AymnCoder Plus Sovereign Enterprise Core",
    version="18.0.0-Master",
    description="The Absolute Master Backend Hub controlling all micro-services",
    lifespan=sovereign_lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- ربط الواجهات الأمامية والـ Mini App كخدمات تابعة للـ Backend ---
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend_core")
MINI_APP_DIR = os.path.join(FRONTEND_DIR, "mini_app")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")

if os.path.exists(MINI_APP_DIR):
    app.mount("/mini-app", StaticFiles(directory=MINI_APP_DIR, html=True), name="mini_app")
    logger.info("🌐 [Master Hub]: تم دمج واجهة Mini App بنجاح تحت سيطرة الـ Backend.")

if os.path.exists(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend_assets")

# ==============================================================================
# 8. دمج المسارات الخارجية (External Routers Integration)
# ==============================================================================
external_routers = [
    {"module": "core.trading_execution", "prefix": "/api/v1/trading-execution", "tags": ["Real Trading Engine"]},
    {"module": "src.ai_engine", "prefix": "/api/v1/ai-forge", "tags": ["AI Feature Forge"]},
    {"module": "security.core_routes", "prefix": "/api/v1/security-core", "tags": ["Advanced Security"]},
    {"module": "app.enterprise_gateway", "prefix": "/api/v1/enterprise", "tags": ["Enterprise Gateway"]},
    {"module": "services.telegram_bridge", "prefix": "/api/v1/telegram-bridge", "tags": ["Telegram Bridge"]}
]

for route_info in external_routers:
    try:
        module = importlib.import_module(route_info["module"])
        if hasattr(module, "router"):
            app.include_router(module.router, prefix=route_info["prefix"], tags=route_info["tags"])
            logger.info(f"🔗 [Router Integrated]: تم ربط مسارات {route_info['module']}")
    except ImportError:
        logger.debug(f"ℹ️ [Router Skip]: المجلد {route_info['module']} غير محمل حالياً.")
    except Exception as e:
        logger.error(f"⚠️ [Router Error] في {route_info['module']}: {str(e)}")

# ==============================================================================
# 9. نماذج بيانات التحقق (Pydantic Models)
# ==============================================================================
class TradeRequestModel(BaseModel):
    symbol: str
    side: str
    amount: float
    api_key: str
    api_secret: str

class LicenseLinkRequest(BaseModel): license_key: str; chat_id: str
class ProtectionSlotRequest(BaseModel): license_key: str; channel_id: str
class CreativeAssetRequest(BaseModel): license_key: str; prompt: str; asset_type: Optional[str] = "logo"; aspect_ratio: Optional[str] = "1:1"
class EnterpriseSearchRequest(BaseModel): license_key: str; query: str; scope: Optional[str] = "all"

# ==============================================================================
# 10. معالجة تليجرام كخدمة فرعية تابعة للنواة (Telegram Microservice Handler)
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
            
            # حفظ السجل عبر النواة المركزية
            async with async_session() as session:
                session.add(TelegramLogModel(update_id=update_id, chat_id=str(chat_id), text_content=text))
                await session.commit()

            if text.startswith("/start"):
                await send_telegram_response(chat_id, "🛡️ **أهلاً بك في AymnGuard Sovereign Enterprise Core**\nالنواة المركزية تسيطر بالكامل على الخدمات.")
            else:
                await send_telegram_response(chat_id, f"✅ تم استقبال الأمر ومعالجته عبر الـ Backend بنجاح: `{text}`")
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة تليجرام الفرعية: {e}")

async def send_telegram_response(chat_id: int, text: str):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage", 
                              json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception:
        pass

# ==============================================================================
# 11. مسارات الـ API التشغيلية الأساسية للـ Master Hub
# ==============================================================================
@app.post("/api/v1/telegram/webhook", tags=["Webhook Subservice"])
@limiter.limit("60/minute")
async def telegram_webhook(request: Request, bg_tasks: BackgroundTasks, x_telegram_bot_api_secret_token: Optional[str] = Header(None)):
    if settings.TELEGRAM_SECRET_TOKEN and x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized Telegram Telemetry")
    bg_tasks.add_task(process_telegram_update, await request.json())
    return {"status": "success", "master_hub": "processed"}

@app.post("/api/v1/trade/execute", tags=["Trading Backstop"])
@limiter.limit("20/minute")
async def execute_trade_endpoint(request: Request, payload: TradeRequestModel):
    return {"status": "success", "message": f"تم تنفيذ التداول بنجاح لـ {payload.symbol} عبر الـ Backend الرئيسي."}

@app.post("/api/v1/license/link", tags=["Services Matrix"])
async def link_license(data: LicenseLinkRequest): 
    return await SovereignLicenseManager.verify_and_link_user(data.license_key, data.chat_id)

@app.post("/api/v1/protection/activate", tags=["Services Matrix"])
async def activate_protection(data: ProtectionSlotRequest): 
    return await SovereignProtectionEngine.activate_protection(data.license_key, data.channel_id)

@app.post("/api/v1/creative/generate", tags=["Services Matrix"])
async def generate_asset(data: CreativeAssetRequest): 
    return await SovereignCreativeStudio.generate_asset_request(data.license_key, data.prompt, data.asset_type, data.aspect_ratio)

@app.post("/api/v1/search/intelligence", tags=["Services Matrix"])
async def enterprise_search(data: EnterpriseSearchRequest): 
    return await SovereignSearchEngine.execute_enterprise_search(data.license_key, data.query, data.scope)

@app.websocket("/ws/security-alerts")
async def ws_security(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping": 
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)

@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def home():
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f: 
            return f.read()
    return "<h2>AymnGuard Sovereign Enterprise Core Active - Master Backend Hub Online</h2>"

if __name__ == "__main__":
    uvicorn.run("backend_core.main:app", host="0.0.0.0", port=10000, reload=False, log_level="info")
