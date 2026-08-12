# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Imperial Enterprise Gateway (Cloud Production Ready)
==============================================================================
البوابة المؤسسية السيادية الشاملة: هندسة الحسابات المتعددة، نقل الأعضاء، 
واجهات الأعمال، مؤشرات التداول، والاتصالات اللحظية عبر WebSockets.
تم التأمين وتفعيل CORS ليتوافق مع السيرفرات السحابية وتطبيقات الهاتف.
==============================================================================
"""

from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

# إعداد سجلات البوابة
logger = logging.getLogger("AymnGuard.Gateway")

# --- استيراد النواة والمحركات الإمبراطورية الموسعة والشاملة ---
from core.license_manager import SovereignLicenseManager
from core.session_manager import SovereignSessionManager
from bots.protection.bot_engine import SovereignProtectionEngine
from bots.creative.creative_engine import SovereignCreativeStudio
from bots.search.search_engine import SovereignSearchEngine
from modules.telegram.transfer_engine import MemberTransferEngine
from modules.telegram.business_engine import TelegramBusinessEngine
from modules.trading.indicators_engine import TradingIndicatorEngine

app = FastAPI(
    title="AymnGuard Imperial Enterprise Gateway",
    version="6.0.1",
    description="البوابة المركزية السحابية لمنظومة AymnGuard"
)

# --- إعدادات جدار الحماية للاتصالات السحابية (CORS Middleware) ---
# هذا الإعداد ضروري جداً لكي يتمكن تطبيق Flutter من الاتصال بالسيرفر السحابي
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكن تقييدها لاحقاً بعناوين IP محددة لمزيد من الأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- إدارة الاتصالات النشطة للمراقبة اللحظية (WebSockets) ---
active_connections: List[WebSocket] = []

@app.websocket("/api/v1/ws/monitor/{license_key}")
async def websocket_monitor(websocket: WebSocket, license_key: str):
    """قناة مراقبة لحظية لكل إجراء في النظام السيادي"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[System Echo]: {data}")
    except WebSocketDisconnect:
        logger.info(f"[WS]: انقطع الاتصال بشكل طبيعي للمفتاح {license_key}")
    except Exception as e:
        logger.error(f"[WS]: خطأ غير متوقع في الاتصال اللحظي: {str(e)}")
    finally:
        if websocket in active_connections:
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
    feature_type: str
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
    asset_type: str = "logo"
    aspect_ratio: str = "1:1"

class EnterpriseSearchRequest(BaseModel):
    license_key: str
    query: str
    scope: str = "all"


# --- مسارات البوابة المركزية الإمبراطورية المؤسسية ---

@app.post("/api/v1/sessions/register", summary="تهيئة وعزل جلسة جديدة")
async def api_register_session(data: SessionRegistrationRequest):
    try:
        return await SovereignSessionManager.initialize_session(
            data.license_key, data.session_name, data.api_id, data.api_hash, data.phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل تهيئة الجلسة: {str(e)}")

@app.post("/api/v1/telegram/transfer", summary="تشغيل محرك نقل الأعضاء")
async def api_member_transfer(data: MemberTransferRequest):
    try:
        return await MemberTransferEngine.execute_transfer(
            data.license_key, data.session_name, data.source_chat, data.target_chat, data.batch_size, data.filter_active_users
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل محرك النقل: {str(e)}")

@app.post("/api/v1/telegram/business", summary="تفعيل واجهات الأعمال")
async def api_telegram_business(data: TelegramBusinessRequest):
    try:
        return await TelegramBusinessEngine.configure_feature(
            data.license_key, data.session_name, data.feature_type, data.config_payload
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل تكوين الأعمال: {str(e)}")

@app.post("/api/v1/trading/indicators", summary="حساب مؤشرات التداول")
async def api_trading_indicators(data: TradingIndicatorRequest):
    try:
        return await TradingIndicatorEngine.compute_indicators(
            data.license_key, data.session_name, data.symbol, data.timeframe, data.indicators
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل محرك التداول: {str(e)}")

@app.post("/api/v1/license/link", summary="إدارة وربط المفتاح السيادي")
async def api_link_license(data: dict):
    try:
        return await SovereignLicenseManager.verify_and_link_user(
            data.get("license_key"), data.get("chat_id")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل التحقق من الترخيص: {str(e)}")

@app.post("/api/v1/protection/activate", summary="تفعيل دروع الحماية")
async def api_activate_protection(data: ProtectionSlotRequest):
    try:
        return await SovereignProtectionEngine.activate_protection(
            data.license_key, data.channel_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل تفعيل الحماية: {str(e)}")

@app.post("/api/v1/creative/generate", summary="توليد الهويات والتصاميم")
async def api_generate_asset(data: CreativeAssetRequest):
    try:
        return await SovereignCreativeStudio.generate_asset_request(
            data.license_key, data.prompt, data.asset_type, data.aspect_ratio
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل الاستوديو الإبداعي: {str(e)}")

@app.post("/api/v1/search/intelligence", summary="البحث الاستخباراتي الشامل")
async def api_enterprise_search(data: EnterpriseSearchRequest):
    try:
        return await SovereignSearchEngine.execute_enterprise_search(
            data.license_key, data.query, data.scope
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"فشل محرك البحث: {str(e)}")

@app.get("/health", summary="فحص نبض النظام السحابي")
async def health_check():
    return {
        "status": "online",
        "system": "AymnGuard Imperial Enterprise Core v6.0.1",
        "architecture": "Cloud-Native, Isolated Multi-Session, Real-time WebSockets",
        "network": "CORS Enabled for Remote Clients"
    }
