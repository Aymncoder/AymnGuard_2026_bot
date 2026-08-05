# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Telegram Bridge & Webhook Handler
جسر تيليجرام السيادي: استقبال التحديثات الحية (Webhooks) من تيليجرام، تمريرها 
إلى العقل المركزي (Master Orchestrator)، وإرسال الردود المشفرة والمؤمنة للعملاء لحظياً.
"""

import os
import logging
import httpx
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from core.master_orchestrator import MasterSovereignOrchestrator

logger = logging.getLogger("AymnGuard.TelegramBridge")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/telegram", tags=["Sovereign Telegram Bridge"])

# تهيئة العقل المركزي للإمبراطورية
orchestrator = MasterSovereignOrchestrator()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def send_telegram_message(chat_id: int, text: str) -> None:
    """
    إرسال الرد السيادي إلى مستخدم تيليجرام بشكل غير متزامن وآمن.
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_bot_token_here":
        logger.warning("⚠️ [Telegram Bridge]: لم يتم ضبط رمز البوت (TELEGRAM_BOT_TOKEN)، تعذر الإرسال الفعلي للخارج.")
        return

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
            if response.status_code == 200:
                logger.info(f"📤 [Telegram Bridge]: تم إرسال الرد بنجاح للعميل [Chat ID: {chat_id}]")
            else:
                logger.error(f"❌ [Telegram API Error]: فشل إرسال الرسالة: {response.text}")
        except Exception as e:
            logger.error(f"❌ [Network Error]: حدث خطأ أثناء الاتصال بخوادم تيليجرام: {e}")

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook_receiver(request: Request, db: AsyncSession = Depends(get_db)):
    """
    نقطة النهاية لاستقبال أحداث ومانح الرسائل (Webhooks) القادمة من تيليجرام.
    """
    try:
        data = await request.json()
        logger.info("📥 [Telegram Webhook]: تلقي تحديث جديد من شبكة تيليجرام.")

        # التحقق من وجود رسالة نصية داخل التحديث
        message = data.get("message") or data.get("edited_message")
        if not message:
            return {"status": "ignored", "reason": "no_message_found"}

        chat = message.get("chat", {})
        sender = message.get("from", {})
        
        telegram_id = chat.get("id")
        username = sender.get("username") or sender.get("first_name", "SovereignOperator")
        message_text = message.get("text", "")

        if not telegram_id or not message_text:
            return {"status": "ignored", "reason": "invalid_payload"}

        logger.info(f"👤 [Incoming User]: {username} (ID: {telegram_id}) -> {message_text}")

        # توجيه الطلب للعقل المركزي المعالج مع تمرير جلسة قاعدة البيانات
        response_payload = await orchestrator.orchestrate_user_request(
            telegram_id=telegram_id,
            username=username,
            message_text=message_text,
            db_session=db
        )

        # استخراج المحتوى المُعّد للرد
        reply_content = response_payload.get("content", "⚠️ النظام يعمل بكفاءة تامة.")

        # إرسال الرد الفعلي عبر بوت تيليجرام
        await send_telegram_message(chat_id=telegram_id, text=reply_content)

        return {"status": "success", "processed_by": "MasterSovereignOrchestrator"}

    except Exception as e:
        logger.error(f"❌ [Webhook Critical Error]: خطأ حرج في معالجة الـ Webhook: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}
