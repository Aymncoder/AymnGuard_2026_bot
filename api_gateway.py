# gateway/api_gateway.py
from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- استيراد النواة والمحركات الإمبراطورية الموسعة والشاملة ---
from core.license_manager import SovereignLicenseManager
from core.session_manager import SovereignSessionManager  # إدارة الجلسات والحسابات المعزولة
from bots.protection.bot_engine import SovereignProtectionEngine
from bots.creative.creative_engine import SovereignCreativeStudio
from bots.search.search_engine import SovereignSearchEngine
from modules.telegram.transfer_engine import MemberTransferEngine # محرك نقل الأعضاء
from modules.telegram.business_engine import TelegramBusinessEngine # واجهات تيليجرام الأعمال والمميز
from modules.trading.indicators_engine import TradingIndicatorEngine # مؤشرات التداول الفنية

app = FastAPI(
    title="AymnGuard Imperial Enterprise Gateway",
    version="6.0.0",
    description="البوابة المؤسسية السيادية الشاملة - هندسة الحسابات المتعددة، نقل الأعضاء، واجهات الأعمال، مؤشرات التداول، والاتصالات اللحظية عبر WebSockets"
)

# --- إدارة الاتصالات النشطة للمراقبة اللحظية (WebSockets) ---
active_connections: List[WebSocket] = []

@app.websocket("/api/v1/ws/monitor/{license_key}")
async def websocket_monitor(websocket: WebSocket, license_key: str):
    """قناة مراقبة لحظية (Real-time Feedback) لكل إجراء في النظام السيادي."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Sovereign Core Operational: Echoing -> {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# --- نماذج بيانات المؤسسة (Pydantic Schemas) ---

class SessionRegistrationRequest(BaseModel):
    license_key: str
    session_name: str
    api_id: int
    api_hash: str
    phone_number: str

class MemberTransferRequest(BaseModel):
    license_key: str
    session_name: str
    source_chat: str
    target_chat: str
    batch_size: int = 50
    filter_active_users: bool = True

class TelegramBusinessRequest(BaseModel):
    license_key: str
    session_name: str
    feature_type: str  # auto_reply, greeting_bot, premium_broadcast, quick_replies
    config_payload: Dict[str, Any]

class TradingIndicatorRequest(BaseModel):
    license_key: str
    session_name: str
    symbol: str
    timeframe: str
    indicators: List[str] = ["RSI", "EMA", "ParabolicSAR", "MACD"]

class ProtectionSlotRequest(BaseModel):
    license_key: str
    channel_id: str

class CreativeAssetRequest(BaseModel):
    license_key: str
    prompt: str
    asset_type: Optional[str] = "logo"
    aspect_ratio: Optional[str] = "1:1"

class EnterpriseSearchRequest(BaseModel):
    license_key: str
    query: str
    scope: Optional[str] = "all"


# --- مسارات البوابة المركزية الإمبراطورية المؤسسية ---

@app.post("/api/v1/sessions/register", summary="إدمان وعزل جلسة/حساب جديد ضمن المنظومة السيادية")
async def api_register_session(data: SessionRegistrationRequest):
    """تهيئة وإضافة جلسة تليجرام جديدة مع عزل صلاحيات البوتات والأدوات التابعة لها."""
    result = await SovereignSessionManager.initialize_session(
        data.license_key, data.session_name, data.api_id, data.api_hash, data.phone_number
    )
    return result

@app.post("/api/v1/telegram/transfer", summary="تشغيل محرك نقل الأعضاء والكسح الآلي المتقدم")
async def api_member_transfer(data: MemberTransferRequest):
    """إدارة عمليات نقل الأعضاء بين المجموعات عبر الجلسة المحددة بأعلى معايير الحماية والتجاوز."""
    result = await MemberTransferEngine.execute_transfer(
        data.license_key, data.session_name, data.source_chat, data.target_chat, data.batch_size, data.filter_active_users
    )
    return result

@app.post("/api/v1/telegram/business", summary="تفعيل واجهات تيليجرام الأعمال والمميز لكل حساب")
async def api_telegram_business(data: TelegramBusinessRequest):
    """التحكم الكامل بخطوط إنتاج تيليجرام الأعمال، الردود التلقائية، وخدمات الحسابات المميزة."""
    result = await TelegramBusinessEngine.configure_feature(
        data.license_key, data.session_name, data.feature_type, data.config_payload
    )
    return result

@app.post("/api/v1/trading/indicators", summary="حساب مؤشرات التداول الفنية والتحليل المرتبط بالحساب")
async def api_trading_indicators(data: TradingIndicatorRequest):
    """تنفيذ الحسابات الرياضية للمؤشرات (RSI, EMA, SAR) لدعم استراتيجيات التداول الآلي واليدوي."""
    result = await TradingIndicatorEngine.compute_indicators(
        data.license_key, data.session_name, data.symbol, data.timeframe, data.indicators
    )
    return result

@app.post("/api/v1/license/link", summary="إدارة استعادة المفتاح السيادي بربط الحساب بملف تليجرام جديد")
async def api_link_license(data: dict):
    result = await SovereignLicenseManager.verify_and_link_user(data.get("license_key"), data.get("chat_id"))
    return result

@app.post("/api/v1/protection/activate", summary="تفعيل دروع الحماية وإدارة الثغرات الديناميكية")
async def api_activate_protection(data: ProtectionSlotRequest):
    result = await SovereignProtectionEngine.activate_protection(data.license_key, data.channel_id)
    return result

@app.post("/api/v1/creative/generate", summary="توليد الهويات والتصاميم عبر استوديو الذكاء الاصطناعي")
async def api_generate_asset(data: CreativeAssetRequest):
    result = await SovereignCreativeStudio.generate_asset_request(
        data.license_key, data.prompt, data.asset_type, data.aspect_ratio
    )
    return result

@app.post("/api/v1/search/intelligence", summary="البحث الاستخباراتي الشامل وربط شبكات البيانات المؤسسية")
async def api_enterprise_search(data: EnterpriseSearchRequest):
    result = await SovereignSearchEngine.execute_enterprise_search(
        data.license_key, data.query, data.scope
    )
    return result

@app.get("/health", summary="فحص نبض النظام السيادي والمؤسسي الشامل")
async def health_check():
    return {
        "status": "online",
        "system": "AymnGuard Imperial Enterprise Core v6.0",
        "architecture": "Isolated Multi-Session, Real-time WebSockets & Modular Sovereign Engine"
    }
