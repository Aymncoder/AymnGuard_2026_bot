# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Telegram Bot Engine (v5.0 Ultimate Unified Core)
محرك بوت تيليجرام المتكامل: تليجرام الأعمال، طوابير Redis، لوحة المالك، ومشتركين المنصة
=============================================================================
"""

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# 🛡️ [حماية المسارات المتقدمة]: استيراد كافة خدمات النواة ولوحات التحكم دون أي تداخل أو تكرار
try:
    from backend_core.services.queue_manager import MessageQueueManager
    from backend_core.services.telegram_business import TelegramBusinessManager
    from backend_core.bot.owner_panel import get_owner_main_keyboard, OWNER_ID
    from backend_core.bot.subscriber_panel import get_subscriber_main_keyboard
except ImportError:
    try:
        from services.queue_manager import MessageQueueManager
        from services.telegram_business import TelegramBusinessManager
        from owner_panel import get_owner_main_keyboard, OWNER_ID
        from subscriber_panel import get_subscriber_main_keyboard
    except ImportError:
        from ..services.queue_manager import MessageQueueManager
        from ..services.telegram_business import TelegramBusinessManager
        from .owner_panel import get_owner_main_keyboard, OWNER_ID
        from .subscriber_panel import get_subscriber_main_keyboard

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AymnGuardBotEngine")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mattress-before-exec-artwork.trycloudflare.com/app/index.html")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ [Configuration Error]: لم يتم العثور على TELEGRAM_BOT_TOKEN في البيئة السيادية.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: types.Message):
    """
    معالجة أمر البدء للمشتركين وعرض اللوحة السيادية المتكاملة مع الأزرار التفاعلية والخدمات.
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    logger.info(f"🛡️ [Bot Event]: استقبال أمر /start من المشترك {user_id} (@{username})")
    
    # دفع الحدث لطوابير Redis للاستجابة الخلفية غير المتزامنة
    await MessageQueueManager.push_to_queue("telegram_updates_queue", {
        "update_id": message.message_id,
        "chat_id": message.chat.id,
        "user_id": user_id,
        "username": username,
        "text": message.text
    })

    keyboard = get_subscriber_main_keyboard()

    await message.answer(
        "🛡️ **مرحباً بك في منصة AymnGuard Enterprise v5.0 السيادية**\n\n"
        "النظام يعمل بأقصى معايير الأمان، الذكاء الاصطناعي، والحوسبة الفائقة. اختر الخدمة التي تود إدارتها من القائمة أدناه:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(Command("panel"))
async def owner_control_panel_handler(message: types.Message):
    """
    نقطة الدخول للوحة التحكم السيادية الخاصة بالمالك حصرياً (Owner Control Panel).
    """
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ عذراً، هذه اللوحة مخصصة لمالك النظام السيادي فقط.")
        return

    keyboard = get_owner_main_keyboard()
    await message.answer(
        "🛡️ **مرحباً بك في غرفة القيادة والسيطرة السيادية (Owner Control Panel)**\n\n"
        "جميع الأنظمة، الطوابير، ومحركات الذكاء الاصطناعي تعمل بكفاءة مطلقة. اختر العملية المطلوبة:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(lambda msg: msg.text == "🔙 القائمة الرئيسية")
async def return_to_main_menu(message: types.Message):
    """
    العودة الفورية للقائمة الرئيسية السيادية للمشترك.
    """
    keyboard = get_subscriber_main_keyboard()
    await message.answer("🛡️ **القائمة الرئيسية السيادية للمشترك:**", reply_markup=keyboard, parse_mode="Markdown")

# 💼 معالجات تليجرام الأعمال المتقدمة (Telegram Business Handlers)
@dp.business_connection()
async def business_connection_handler(business_connection: types.BusinessConnection):
    """
    مُستقبل حدث اتصال حساب تليجرام التجاري بالبوت وتوجيهه عبر الطوابير.
    """
    await TelegramBusinessManager.handle_business_connection(business_connection)

@dp.business_message()
async def business_message_handler(message: types.Message):
    """
    مُستقبل رسائل الحسابات التجارية لتنفيذ المعالجة الآلية والذكية.
    """
    await TelegramBusinessManager.handle_business_message(message)

async def main():
    """
    إقلاع محرك البوت والخدمات السيادية بكفاءة فائقة.
    """
    logger.info("🚀 [Bot Launch]: جاري إطلاق محرك بوت تيليجرام السيادي المتكامل (v5.0)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 [Bot Shutdown]: تم إيقاف محرك البوت يدوياً بأمان تام.")
