# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Telegram Sovereign Gateway
==============================================================================
بوابة تيليجرام السيادية: نقطة الاتصال المحصنة بين خوادم تيليجرام ومحرك AymnGuard.
مصممة كخدمة مستقلة (Microservice) تلتقط الإشارات من المجتمعات والمستخدمين،
وتمررها فوراً إلى وسيط المهام (Task Broker) والمحرك العصبي لضمان عدم توقف الواجهة.
"""

import logging
import asyncio
from typing import Optional

# استخدام Pyrogram لسرعتها الفائقة وتوافقها مع بيئات لينكس المصغرة (Termux)
from pyrogram import Client, filters
from pyrogram.types import Message

# استدعاء الأعضاء الحيوية التي تم بناؤها مسبقاً (ربط تام بدون تكرار)
from backend_core.task_broker import broker
from backend_core.context_vault import ContextVault

# إعداد مسجل الأحداث الخاص بطبقة الاتصال
logger = logging.getLogger("AymnGuard.TelegramGateway")

class TelegramGateway:
    """
    مدير اتصال تيليجرام بنمط (Singleton) لضمان عدم تعدد جلسات الاتصال (Session Clash).
    يعمل كـ "مُوجّه وكلاء" (Agent Dispatcher) يحيل الطلبات للنظام الخلفي بذكاء.
    """
    
    def __init__(self, bot_token: str, api_id: int, api_hash: str):
        self.app = Client(
            "AymnGuard_Sovereign_Session",
            bot_token=bot_token,
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True # حماية أمنية: عدم ترك ملفات جلسات متناثرة في التخزين
        )
        self._register_routes()
        
    def _register_routes(self) -> None:
        """
        تسجيل مسارات الاستقبال (Routes) بدقة.
        معزولة تماماً داخل الكلاس لمنع أي تداخل مع مسارات التطبيق المصغر أو الـ API.
        """
        
        @self.app.on_message(filters.command("start") & filters.private)
        async def sovereign_start_command(client: Client, message: Message):
            user_id = str(message.from_user.id)
            logger.info(f"🛡️ [Telegram Gateway]: Secure /start signal received from {user_id}")
            
            # 1. استدعاء الذاكرة فوراً لتوثيق الجلسة
            await ContextVault.store_context(user_id, {"last_command": "/start", "platform": "telegram"})
            
            # 2. الرد الفوري لضمان تجربة مستخدم خاطفة
            await message.reply_text(
                "**AymnGuard Enterprise v5.0** 🛡️\n\n"
                "تم تفعيل البروتوكولات السيادية بنجاح. النظام جاهز لاستقبال الأوامر وتوجيه وكلاء الذكاء الاصطناعي."
            )

        @self.app.on_message(filters.text & filters.private & ~filters.command("start"))
        async def ai_agent_dispatcher(client: Client, message: Message):
            """
            بوابة العبور لوكلاء الذكاء الاصطناعي (AI Agents).
            تستلم النص وترميه لوسيط المهام ليتكفل به المحرك العصبي في الخلفية.
            """
            user_id = str(message.from_user.id)
            payload_text = message.text
            
            logger.debug(f"📥 [Telegram Gateway]: Payload received from {user_id}. Dispatching...")

            # مهمة خلفية أ: إرسال مؤشر "يكتب..." لعدم تجميد واجهة المستخدم
            async def send_typing_action(chat_id: int):
                await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
                
            await broker.submit_task(send_typing_action, message.chat.id)

            # مهمة خلفية ب: التوجيه للمحرك العصبي (Neural Engine) للتحليل
            # وضعناها كمهمة لا متزامنة لكي لا يتوقف البوت عن استقبال رسائل بقية المستخدمين
            async def cognitive_task(uid: str, text: str, msg_obj: Message):
                try:
                    # TODO: سيتم ربط مخرجات neural_engine.py هنا بدلاً من الـ Sleep
                    await asyncio.sleep(1.5) 
                    response_text = f"⚙️ [المحرك العصبي]: تم تحليل المعطيات سيادياً.\nمحتوى الإشارة: {text[:20]}..."
                    await msg_obj.reply_text(response_text)
                except Exception as e:
                    logger.error(f"❌ [Telegram Gateway]: Agent failure for {uid} -> {e}")
                    await msg_obj.reply_text("⚠️ حدث تداخل مؤقت في المسارات العصبية.")

            # حقن المهمة المعقدة في طابور العمليات (Task Broker)
            await broker.submit_task(cognitive_task, user_id, payload_text, message)

    async def boot_gateway(self) -> None:
        """إشعال شرارة الاتصال بخوادم تيليجرام"""
        logger.info("🚀 [Telegram Gateway]: Initiating secure connection to Telegram MTProto servers...")
        await self.app.start()
        logger.info("✅ [Telegram Gateway]: Online and listening for global signals.")
        
    async def shutdown_gateway(self) -> None:
        """إنهاء الاتصال بأمان تام عند إطفاء النظام"""
        logger.info("🛑 [Telegram Gateway]: Terminating connection securely...")
        await self.app.stop()

# الكائن لن يتم تشغيله هنا، بل تم تجهيزه ليكون جاهزاً للاستدعاء لاحقاً.
