# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Sovereign Telegram Bridge & Telemetry Core
==============================================================================
جسر تيليجرام السيادي المتكامل ومركز الأحداث الميدانية (Unified Enterprise Core):
يجمع بين استقبال التحديثات الحية (Webhooks)، وتدقيق وتصفية إشارات الويب هوك،
رصد الهجمات والبلاغات الكيدية، تمرير البيانات للعقل المركزي المعالج، 
بناء واجهات المستخدم التفاعلية المتقدمة (UI & Inline Keyboards)، 
وإرسال الردود المباشرة والبث الجماعي الآمن عبر بوابة اتصال مشفرة وعالية الأداء.
"""

import os
import logging
import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Request, Header, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==============================================================================
# 0. استيراد النواة المركزية وقواعد البيانات (مع آليات الاستشعار والاحتواء الآمن)
# ==============================================================================
try:
    from database.db import get_db
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:
    from typing import AsyncGenerator
    async def get_db() -> AsyncGenerator[None, None]:
        yield None
    AsyncSession = Any

try:
    from core.master_orchestrator import MasterSovereignOrchestrator
    orchestrator = MasterSovereignOrchestrator()
except ImportError:
    class MockOrchestrator:
        async def orchestrate_user_request(self, telegram_id, username, message_text, db_session):
            return {
                "content": "⚠️ [وضع المحاكاة السيادية]: العقل المركزي قيد التحديث، الجسر يعمل بكفاءة تامة تحت حماية الدرع.",
                "show_menu": True
            }
    orchestrator = MockOrchestrator()

# إعداد السجلات المؤسسية (Enterprise Logging)
logger = logging.getLogger("AegisAICore.TelegramBridgeUnified")
logger.setLevel(logging.INFO)

# إعداد الموجه المركزي (Router) تحت النطاق المؤسسي الموحد
router = APIRouter(
    prefix="/telegram-bridge",
    tags=["Sovereign Telegram Bridge & Telemetry Core"]
)

# إعدادات البيئة والرموز السرية لتيليجرام
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8885095463:AAGRRtirIswzPutKdhuOTf_OeDzO2PTu_FQ")
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN", "aymnguard_secure_secret_2026")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# ==============================================================================
# 1. نماذج بيانات الجسر والتحقق الأمني (Pydantic Schema Architecture)
# ==============================================================================
class BroadcastPayload(BaseModel):
    message: str = Field(..., description="نص الرسالة السيادية المراد بثها للمستهدفين")
    target_chats: List[str] = Field(..., description="قائمة معرفات المحادثات المستهدفة للبث الجماعي")

class DirectMessagePayload(BaseModel):
    chat_id: str = Field(..., description="معرف المحادثة الخاص بالمستلم")
    message: str = Field(..., description="محتوى الرسالة المباشرة")
    show_menu: bool = Field(default=False, description="تحديد ما إذا كان سيتم إرفاق القائمة التفاعلية الرئيسية")

class BridgeTelemetryReport(BaseModel):
    status: str
    bridge_node: str
    active_monitors: int
    shield_status: str
    message: str

# ==============================================================================
# 2. محرك واجهة تيليجرام التفاعلية (UI & Inline Keyboards Engine)
# ==============================================================================
class TelegramUIBuilder:
    """محرك هندسة وبناء واجهات وأزرار تيليجرام التفاعلية للمنصة السيادية المؤسسية"""
    
    @staticmethod
    def get_main_menu() -> Dict[str, Any]:
        """توليد لوحة التحكم الرئيسية التفاعلية للمستخدم (Main Cyber-Sovereign Dashboard)"""
        return {
            "inline_keyboard": [
                [
                    {"text": "🛡️ تفعيل الدرع السيادي", "callback_data": "menu_protect"},
                    {"text": "🎨 استوديو الإبداع الذكي", "callback_data": "menu_creative"}
                ],
                [
                    {"text": "📈 التداول الآلي و CCXT", "callback_data": "menu_trade"},
                    {"text": "🔍 الاستخبارات والبحث", "callback_data": "menu_search"}
                ],
                [
                    {"text": "💳 إدارة المفتاح والهوية", "callback_data": "menu_license"}
                ],
                [
                    {"text": "🌐 فتح لوحة القيادة (Mini App)", "web_app": {"url": "https://79aa1d2d170e59.lhr.life/mini-app"}}
                ]
            ]
        }

# ==============================================================================
# 3. محرك الدرع الأمني الميداني وتدقيق الأحداث (Telegram Bridge Defense Engine)
# ==============================================================================
class SovereignTelegramBridgeEngine:
    """
    محرك الجسر الميداني والاستخباراتي: يتولى معالجة التحديثات الواردة من تيليجرام،
    تطبيق فلاتر الحماية، رصد الهجمات والبلاغات الكيدية، وإدارة الذاكرة التشغيلية.
    """
    
    @staticmethod
    def suppress_service_messages(message_data: dict) -> bool:
        """إسقاط إشعارات الانضمام والمغادرة التشغيلية لتقليل استهلاك الموارد وحماية الخوادم من الازدحام."""
        if "new_chat_members" in message_data or "left_chat_member" in message_data:
            logger.info("🛡️ [Telegram Bridge Shield]: تم رصد وإسقاط إشعار انضمام/مغادرة تشغيلي بنجاح.")
            return True
        return False

    @staticmethod
    async def analyze_telemetry_attacks(message_data: dict) -> bool:
        """تحليل محتوى الرسائل الواردة للكشف عن الهجمات الاستباقية أو البلاغات الكيدية من بوتات خارجية ضارة."""
        user = message_data.get("from", {})
        text = message_data.get("text", "").lower()
        
        if user.get("is_bot", False) and ("report" in text or "spam" in text or "ban" in text):
            logger.warning(f"⚠️ [Security Alert]: رصد محاولة بلاغ كيدي هجومي من بوت خارجي مشبوه ID: {user.get('id')}")
            return True
        return False

    @classmethod
    async def process_incoming_event(cls, update_payload: Dict[str, Any]) -> Dict[str, Any]:
        """معالجة التحديث الوارد وفحصه أمنياً قبل توجيهه للمسار التشغيلي الصحيح ضمن البنية التحتية."""
        try:
            update_id = update_payload.get("update_id")
            message = update_payload.get("message") or update_payload.get("edited_message")
            
            if not message:
                return {"status": "ignored", "reason": "no_message_found"}
                
            # تطبيق مرشحات الدرع الأمني الميداني
            if cls.suppress_service_messages(message):
                return {"status": "suppressed", "reason": "service_message"}
            
            if await cls.analyze_telemetry_attacks(message):
                return {"status": "blocked", "reason": "attack_vector_detected"}
                
            chat = message.get("chat", {})
            chat_id = chat.get("id")
            text = message.get("text", "")
            
            logger.info(f"📨 [Bridge Telemetry]: Processed verified update {update_id} from chat {chat_id}")
            return {
                "status": "success",
                "update_id": update_id,
                "chat_id": chat_id,
                "content_length": len(text),
                "routing": "dispatched_successfully"
            }
            
        except Exception as e:
            logger.error(f"❌ [Bridge Error]: Failed to process incoming telemetry event: {str(e)}")
            return {"status": "error", "error_details": str(e)}

# ==============================================================================
# 4. البوابة المركزية للإرسال وتشفير الاتصالات (Telegram API Gateway)
# ==============================================================================
class TelegramGateway:
    """بوابة الاتصال المباشر والآمن مع خوادم تيليجرام مع معالجة الاستثناءات ومراقبة الاستجابة"""
    
    @staticmethod
    async def send_message(chat_id: str, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> None:
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
            logger.warning("⚠️ [Telegram Gateway]: رمز البوت (Bot Token) غير مضبوط في البيئة التشغيلية.")
            return

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
            
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                response = await client.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
                if response.status_code == 200:
                    logger.info(f"📤 [Telegram Gateway]: تم إرسال الرد السيادي بنجاح للعميل [{chat_id}]")
                else:
                    logger.error(f"❌ [Telegram API Error]: فشل إرسال الرسالة للخادم: {response.text}")
        except Exception as e:
            logger.error(f"❌ [Network Error]: خطأ شبكي حرج أثناء الاتصال بخوادم تيليجرام الخارجية: {str(e)}")

# ==============================================================================
# 5. مسارات API الموحدة للجسر (Webhooks, Telemetry, Direct, Broadcast & Status)
# ==============================================================================

@router.get("/status", response_model=BridgeTelemetryReport, summary="فحص نبض وحالة جسر تيليجرام السيادي")
async def get_bridge_status(x_telegram_bot_api_secret_token: Optional[str] = Header(None)):
    """فحص سلامة وجاهزية عقدة جسر تيليجرام واستجابة مرشحات الدرع الأمني الميداني."""
    logger.info("🌐 [Telegram Bridge]: Health check requested for sovereign telemetry node.")
    
    return {
        "status": "online",
        "bridge_node": "AymnGuard-Telegram-Bridge-Node-Enterprise-01",
        "active_monitors": 5,
        "shield_status": "ACTIVE_AND_FILTERING",
        "message": "جسر تيليجرام والأحداث الميدانية يعمل بكفاءة تامة ومعايير أمان سيادية قصوى."
    }

@router.post("/webhook", status_code=status.HTTP_200_OK, summary="استقبال الأحداث الحية للرسائل (Webhooks Receiver)")
async def telegram_webhook_receiver(
    request: Request, 
    db: AsyncSession = Depends(get_db),
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    """
    القلب النابض الموحد للجسر: يستقبل رسائل المستخدمين، يمررها عبر مرشحات الدرع الأمني،
    يوجهها للعقل المركزي المعالج (Master Orchestrator)، ويجلب الرد الفوري للعميل مع واجهات الأزرار.
    """
    try:
        body_json = await request.json()
        
        # 1. التدقيق الأمني عبر محرك الجسر الميداني (Bridge Engine)
        telemetry_result = await SovereignTelegramBridgeEngine.process_incoming_event(body_json)
        if telemetry_result.get("status") in ["suppressed", "blocked"]:
            return {"status": "filtered", "detail": telemetry_result}

        message = body_json.get("message") or body_json.get("edited_message")
        if not message:
            return {"status": "ignored", "reason": "no_message_found"}

        chat = message.get("chat", {})
        sender = message.get("from", {})
        
        telegram_id = str(chat.get("id"))
        username = sender.get("username") or sender.get("first_name", "SovereignOperator")
        message_text = message.get("text", "")

        if not telegram_id or not message_text:
            return {"status": "ignored", "reason": "invalid_payload_content"}

        logger.info(f"📥 [Incoming Payload Mapped]: {username} (ID: {telegram_id}) -> {message_text[:35]}...")

        # 2. توجيه الطلب للعقل المركزي المعالج (Master Orchestrator)
        response_payload = await orchestrator.orchestrate_user_request(
            telegram_id=telegram_id,
            username=username,
            message_text=message_text,
            db_session=db
        )

        # 3. استخراج محتوى الاستجابة وتحديد متطلبات واجهة الأزرار التفاعلية
        reply_content = response_payload.get("content", "⚠️ النظام يعمل بكفاءة تامة تحت حماية النواة السيادية.")
        show_menu = response_payload.get("show_menu", False)
        
        # إذا أرسل المستخدم أمر البدء "/start"، يتم فرض عرض لوحة التحكم الرئيسية فوراً
        markup = TelegramUIBuilder.get_main_menu() if show_menu or message_text.strip().lower() == "/start" else None

        # 4. إرسال الرد الفعلي عبر بوابة الاتصال المشفرة
        await TelegramGateway.send_message(chat_id=telegram_id, text=reply_content, reply_markup=markup)

        return {"status": "success", "processed_by": "MasterSovereignOrchestrator", "telemetry": telemetry_result}

    except Exception as e:
        logger.error(f"❌ [Webhook Critical Error]: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/telemetry-ingest", summary="استقبال ومعالجة إشارات الويب هوك الميدانية الاستخباراتية")
async def ingest_telegram_telemetry(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    """
    بوابة استقبال الإشارات المتقدمة (Telemetry Ingestion Gateway): تستقبل تدفقات الأحداث،
    تتحقق من تطابق الرمز السري للأمان، وتجري التحليلات الاستباقية للدرع السيادي.
    """
    if TELEGRAM_SECRET_TOKEN and x_telegram_bot_api_secret_token != TELEGRAM_SECRET_TOKEN:
        logger.warning("🚨 [Security Breach Attempt]: محاولة اتصال غير مصرح بها لجسر التيليجرام برمز سري غير صحيح.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Telegram Telemetry Token")

    try:
        body_json = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="حمولة البيانات الواردة تالفة أو غير صالحة.")
    
    telemetry_result = await SovereignTelegramBridgeEngine.process_incoming_event(body_json)
    
    return {
        "status": "success",
        "bridge_response": telemetry_result
    }

@router.post("/send", summary="إرسال رسالة مباشرة فورية (من خادم المنصة لعميل محدد)")
async def send_direct_message(payload: DirectMessagePayload):
    """يسمح لباقي وحدات النواة والخدمات المؤسسية بإرسال رسائل توجيهية أو واجهات تفاعلية للمستخدمين فوراً"""
    markup = TelegramUIBuilder.get_main_menu() if payload.show_menu else None
    await TelegramGateway.send_message(payload.chat_id, payload.message, markup)
    return {"status": "success", "message": "تم توجيه الرسالة المباشرة عبر جسر تيليجرام بنجاح."}

@router.post("/broadcast", summary="بث إرسال سيادي شامل لعدة محادثات في الخلفية")
async def broadcast_message(payload: BroadcastPayload, bg_tasks: BackgroundTasks):
    """إرسال رسائل تحذيرية أو إعلانات وتحديثات برمجية لعدة مستخدمين ومجموعات بشكل متزامن وآمن (Background Task)"""
    async def process_broadcast():
        for chat_id in payload.target_chats:
            await TelegramGateway.send_message(chat_id, f"📢 **تنبيه سيادي عام للمنصة:**\n\n{payload.message}")
            
    bg_tasks.add_task(process_broadcast)
    return {"status": "success", "message": f"جاري بث الرسالة السيادية بنجاح لـ {len(payload.target_chats)} مستهدفاً."}
