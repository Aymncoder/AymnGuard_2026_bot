# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Telegram Bot Engine (v5.0 Ultimate Protected)
محرك بوت تيليجرام المتكامل مع درع الحماية الشامل، الأذكار، ورسالة الترحيب السيادية
=============================================================================
"""

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from dotenv import load_dotenv

# استيراد محركات الحماية والخدمات السيادية بأمان تام
try:
    from backend_core.services.queue_manager import MessageQueueManager
    from backend_core.services.telegram_business import TelegramBusinessManager
    from backend_core.services.group_protection_engine import GroupProtectionEngine
    from backend_core.bot.owner_panel import get_owner_main_keyboard, OWNER_ID
    from backend_core.bot.subscriber_panel import get_subscriber_main_keyboard
    from backend_core.database import AsyncSessionLocal
    from backend_core.services.subscription_service import SubscriptionService
except ImportError:
    try:
        from services.queue_manager import MessageQueueManager
        from services.telegram_business import TelegramBusinessManager
        from services.group_protection_engine import GroupProtectionEngine
        from owner_panel import get_owner_main_keyboard, OWNER_ID
        from subscriber_panel import get_subscriber_main_keyboard
        from database import AsyncSessionLocal
        from services.subscription_service import SubscriptionService
    except ImportError:
        from services.queue_manager import MessageQueueManager
        from services.telegram_business import TelegramBusinessManager
        from services.group_protection_engine import GroupProtectionEngine
        from .owner_panel import get_owner_main_keyboard, OWNER_ID
        from .subscriber_panel import get_subscriber_main_keyboard
        from database import AsyncSessionLocal
        from services.subscription_service import SubscriptionService

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AymnGuardBotEngine")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mattress-before-exec-artwork.trycloudflare.com/app/index.html")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ [Configuration Error]: لم يتم العثور على TELEGRAM_BOT_TOKEN في البيئة السيادية.")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# قائمة الأذكار اللحظية المباركة
ADHAKAR_LIST = [
    "✨ *سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ*",
    "🌿 *لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ*",
    "💎 *أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لَا إِلَهَ إِلَّا هو الْحَيُّ الْقَيُّومُ وَأَتُوبُ إِلَيْهِ*",
    "🌸 *اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ*",
    "🛡️ *حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ، نِعْمَ الْمَوْلَى وَنِعْمَ النَّصِيرُ*"
]

@dp.message(Command("start"))
async def command_start_handler(message: types.Message):
    """
    معالجة أمر البدء، تقديم رسالة الترحيب السيادية، تسجيل المشترك بالقاعدة الدائمة، وعرض لوحة التحكم.
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    first_name = message.from_user.first_name or "القائد السيادي"
    
    logger.info(f"🛡️ [Bot Event]: استقبال أمر /start من المشترك {user_id} (@{username})")
    
    # 1. تسجيل المشترك في القاعدة الدائمة
    try:
        async with AsyncSessionLocal() as session:
            await SubscriptionService.get_or_create_user(session, user_id, username, first_name)
    except Exception as db_err:
        logger.error(f"❌ [Database Sync Error]: فشل تسجيل المستخدم في القاعدة الدائمة - التفاصيل: {str(db_err)}")

    # 2. رسالة الترحيب السيادية الشاملة
    welcome_text = (
        f"🛡️ **مرحباً بك، {first_name} في منصة AymnGuard Enterprise v5.0 السيادية** 🚀\n\n"
        "**فكرة وعمل التطبيق السيادي والبوت:**\n"
        "• **درع الحماية المطلق:** حماية المجموعات والقنوات من التجميد، التهكير، وبروتوكولات التجسس مع إخفاء إشعارات الانضمام والمغادرة والبلاغات الكيدية.\n"
        "• **استيعاب بلا حدود:** تهيئة القنوات والمجموعات لاستقبال ملايين الأعضاء بأعلى أداء سرعة وكفاءة.\n"
        "• **استوديو الذكاء الاصطناعي (4K):** تصميم وتوليد الشعارات، القوالب، والأصول البصرية بدقة مذهلة.\n"
        "• **محرك البحث والوسائط الشامل:** البحث في الويب ويوتيوب وشبكات التواصل ومشاهدة الفيديوهات مباشرة من داخل التطبيق دون مغادرته.\n"
        "• **تليجرام الأعمال:** إدارة متكاملة ومؤتمتة لرسائل وحسابات الأعمال السيادية.\n\n"
        "النظام يعمل بأحدث تقنيات الذكاء الاصطناعي والحوسبة الآمنة. اختر الخدمة المطلوبة من القائمة أدناه:"
    )

    keyboard = get_subscriber_main_keyboard()
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode="Markdown")

# 🔒 تفعيل درع الحماية الشامل لجميع رسائل المجموعات والقنوات (حذف الإشعارات والروابط الخبيثة)
@dp.message()
async def global_group_protection_middleware(message: types.Message):
    """
    مُستقبل مركزي لفحص وتأمين رسائل المجموعات والقنوات لحظياً.
    """
    if message.chat.type in ["group", "supergroup", "channel"]:
        # 1. إخفاء رسائل الخدمة (انضمام، مغادرة، تثبيت)
        is_sanitized = await GroupProtectionEngine.sanitize_service_messages(message, bot)
        if is_sanitized:
            return

        # 2. منع البلاغات الهجومية والروابط الخبيثة
        is_blocked = await GroupProtectionEngine.intercept_malicious_payloads(message)
        if is_blocked:
            return

    # السماح بباقي الرسائل العادية بالمرور الطبيعي
    pass

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
    keyboard = get_subscriber_main_keyboard()
    await message.answer("🛡️ **القائمة الرئيسية السيادية للمشترك:**", reply_markup=keyboard, parse_mode="Markdown")

# معالجات تليجرام الأعمال
@dp.business_connection()
async def business_connection_handler(business_connection: types.BusinessConnection):
    await TelegramBusinessManager.handle_business_connection(business_connection)

@dp.business_message()
async def business_message_handler(message: types.Message):
    await TelegramBusinessManager.handle_business_message(message)

async def main():
    logger.info("🚀 [Bot Launch]: إطلاق محرك بوت تيليجرام السيادي مع درع الحماية الشامل والميزات المتقدمة (v5.0)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 [Bot Shutdown]: تم إيقاف محرك البوت يدوياً بأمان تام.")
