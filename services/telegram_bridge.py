# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Sovereign Telegram Bridge (Unified Core)
==============================================================================
جسر تيليجرام السيادي المتكامل: يجمع بين استقبال التحديثات الحية (Webhooks)،
وتمريرها للعقل المركزي المعالج، وبناء واجهات المستخدم التفاعلية (UI)، 
وإرسال الردود والبث الجماعي عبر بوابة اتصال موحدة وعالية الأداء.
"""

import os
import logging
import httpx
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Request, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# ==============================================================================
# 0. استيراد النواة المركزية وقواعد البيانات (مع تأمين الاستثناءات)
# ==============================================================================
try:
    from database.db import get_db
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:
    # بديل طوارئ في حال عدم توفر مسار قاعدة البيانات لتجنب انهيار الجسر
    from typing import AsyncGenerator
    async def get_db() -> AsyncGenerator[None, None]: yield None
    AsyncSession = Any

try:
    from core.master_orchestrator import MasterSovereignOrchestrator
    orchestrator = MasterSovereignOrchestrator()
except ImportError:
    # بديل طوارئ يحاكي العقل المركزي
    class MockOrchestrator:
        async def orchestrate_user_request(self, telegram_id, username, message_text, db_session):
            return {"content": "⚠️ [وضع المحاكاة]: العقل المركزي قيد التحديث، الجسر يعمل بكفاءة."}
    orchestrator = MockOrchestrator()

# إعداد السجلات (Logging)
logger = logging.getLogger("AegisAICore.TelegramBridge")
logger.setLevel(logging.INFO)

# إعداد الموجه (Router)
router = APIRouter(prefix="/telegram", tags=["Sovereign Telegram Bridge"])

# إعدادات تيليجرام
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8885095463:AAGRRtirIswzPutKdhuOTf_OeDzO2PTu_FQ")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# ==============================================================================
# 1. نماذج بيانات الجسر (Pydantic Models)
# ==============================================================================
class BroadcastPayload(BaseModel):
    message: str
    target_chats: List[str]

class DirectMessagePayload(BaseModel):
    chat_id: str
    message: str
    show_menu: bool = False

# ==============================================================================
# 2. محرك واجهة تيليجرام (UI & Inline Keyboards Engine)
# ==============================================================================
class TelegramUIBuilder:
    """محرك هندسة وبناء واجهات وأزرار تيليجرام التفاعلية للمنصة السيادية"""
    
    @staticmethod
    def get_main_menu() -> Dict[str, Any]:
        """لوحة التحكم الرئيسية للمستخدم (Main Dashboard)"""
        return {
            "inline_keyboard": [
                [
                    {"text": "🛡️ تفعيل الدرع السيادي", "callback_data": "menu_protect"},
                    {"text": "🎨 استوديو الإبداع", "callback_data": "menu_creative"}
                ],
                [
                    {"text": "📈 التداول الآلي و CCXT", "callback_data": "menu_trade"},
                    {"text": "🔍 الاستخبارات والبحث", "callback_data": "menu_search"}
                ],
                [
                    {"text": "💳 إدارة المفتاح والهوية", "callback_data": "menu_license"}
                ],
                [
                    {"text": "🌐 فتح لوحة التحكم (Mini App)", "web_app": {"url": "https://79aa1d2d170e59.lhr.life/mini-app"}}
                ]
            ]
        }

# ==============================================================================
# 3. البوابة المركزية للإرسال (Telegram API Gateway)
# ==============================================================================
class TelegramGateway:
    """بوابة الاتصال المباشر والمشفر مع خوادم تيليجرام"""
    
    @staticmethod
    async def send_message(chat_id: str, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> None:
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
            logger.warning("⚠️ [Telegram Gateway]: لم يتم ضبط رمز البوت بشكل صحيح.")
            return

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
            
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
                if response.status_code == 200:
                    logger.info(f"📤 [Telegram Gateway]: تم إرسال الرد بنجاح للعميل [{chat_id}]")
                else:
                    logger.error(f"❌ [Telegram API Error]: فشل إرسال الرسالة: {response.text}")
        except Exception as e:
            logger.error(f"❌ [Network Error]: خطأ شبكي أثناء الاتصال بخوادم تيليجرام: {str(e)}")

# ==============================================================================
# 4. مسارات API الجسر (Webhooks & External Endpoints)
# ==============================================================================

@router.post("/webhook", status_code=status.HTTP_200_OK, summary="استقبال الأحداث الحية (Webhooks)")
async def telegram_webhook_receiver(request: Request, db: AsyncSession = Depends(get_db)):
    """
    القلب النابض للجسر: يستقبل رسائل المستخدمين، يرسلها للعقل المركزي، ويجلب الرد للعميل.
    """
    try:
        data = await request.json()
        
        # التصفية الأولية: استخراج الرسالة النصية فقط
        message = data.get("message") or data.get("edited_message")
        if not message:
            return {"status": "ignored", "reason": "no_message_found"}

        chat = message.get("chat", {})
        sender = message.get("from", {})
        
        telegram_id = str(chat.get("id"))
        username = sender.get("username") or sender.get("first_name", "SovereignOperator")
        message_text = message.get("text", "")

        if not telegram_id or not message_text:
            return {"status": "ignored", "reason": "invalid_payload"}

        logger.info(f"📥 [Incoming Payload]: {username} (ID: {telegram_id}) -> {message_text[:30]}...")

        # 1. توجيه الطلب للعقل المركزي (Master Orchestrator)
        response_payload = await orchestrator.orchestrate_user_request(
            telegram_id=telegram_id,
            username=username,
            message_text=message_text,
            db_session=db
        )

        # 2. استخراج الرد وتحديد ما إذا كان يحتاج إلى واجهة أزرار (Menu)
        reply_content = response_payload.get("content", "⚠️ النظام يعمل بكفاءة تامة تحت حماية النواة.")
        show_menu = response_payload.get("show_menu", False) # يمكن للعقل المركزي أن يقرر إظهار القائمة
        
        # إذا كانت الرسالة هي "/start"، نعرض القائمة تلقائياً
        markup = TelegramUIBuilder.get_main_menu() if show_menu or message_text.strip().lower() == "/start" else None

        # 3. إرسال الرد الفعلي عبر بوابة الاتصال
        await TelegramGateway.send_message(chat_id=telegram_id, text=reply_content, reply_markup=markup)

        return {"status": "success", "processed_by": "MasterSovereignOrchestrator"}

    except Exception as e:
        logger.error(f"❌ [Webhook Critical Error]: {str(e)}", exc_info=True)
        return {"status": "error", "detail": str(e)}

@router.post("/send", summary="إرسال رسالة مباشرة (من خادم لعميل)")
async def send_direct_message(payload: DirectMessagePayload):
    """يسمح لباقي وحدات النظام بإرسال رسائل أو واجهات (قوائم) للمستخدمين فوراً"""
    markup = TelegramUIBuilder.get_main_menu() if payload.show_menu else None
    await TelegramGateway.send_message(payload.chat_id, payload.message, markup)
    return {"status": "success", "message": "تم توجيه الرسالة عبر جسر تيليجرام بنجاح."}

@router.post("/broadcast", summary="بث إرسال سيادي شامل")
async def broadcast_message(payload: BroadcastPayload, bg_tasks: BackgroundTasks):
    """إرسال رسالة تحذيرية أو تحديث لعدة مستخدمين في نفس الوقت (Background Task)"""
    async def process_broadcast():
        for chat_id in payload.target_chats:
            await TelegramGateway.send_message(chat_id, f"📢 **تنبيه سيادي عام:**\n\n{payload.message}")
            
    bg_tasks.add_task(process_broadcast)
    return {"status": "success", "message": f"جاري بث الرسالة لـ {len(payload.target_chats)} مستخدم."}

@router.get("/status", summary="فحص نبض الجسر")
async def bridge_status():
    return {"status": "online", "module": "Sovereign Telegram Bridge Unified", "ready": True}
