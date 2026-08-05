# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Telegram Bot Engine
محرك بوت تيليجرام الأساسي لاستقبال الأحداث ودفعها للطوابير الخلفية
=============================================================================
"""

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from backend_core.services.queue_manager import MessageQueueManager

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AymnGuardBotEngine")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ [Configuration Error]: لم يتم العثور على TELEGRAM_BOT_TOKEN في البيئة السيادية.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: types.Message):
    """
    معالجة أمر البدء (/start) وربط المستخدم بالخدمات والواجهة المصغرة.
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    logger.info(f"🛡️ [Bot Event]: تم استقبال أمر /start من المستخدم {user_id} (@{username})")
    
    # دفع الحدث لطوابير Redis للاستجابة الفورية عبر العامل الخلفي (Worker)
    await MessageQueueManager.push_to_queue("telegram_updates_queue", {
        "update_id": message.message_id,
        "chat_id": message.chat.id,
        "user_id": user_id,
        "username": username,
        "text": message.text
    })

    await message.answer(
        "🛡️ **مرحباً بك في AymnGuard Enterprise v5.0**\n\n"
        "النظام السيادي الموثق يعمل بكفاءة تامة. يمكنك الوصول إلى التطبيق المصغّر (Mini App) عبر الأزرار المخصصة.",
        parse_mode="Markdown"
    )

async def main():
    """
    إقلاع بوت تيليجرام بصيغة Polling أو الاستعداد لاستقبال التحديثات.
    """
    logger.info("🚀 [Bot Launch]: جاري إطلاق محرك بوت تيليجرام السيادي...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 [Bot Shutdown]: تم إيقاف البوت يدوياً بأمان تام.")
