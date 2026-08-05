# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Telegram Sovereign Gateway
==============================================================================
بوابة تيليجرام السيادية: نقطة الاتصال المحصنة بين خوادم تيليجرام ومحرك AymnGuard.
"""

import logging
import asyncio
import sys
import os
from typing import Optional
from services.sovereign_agents import guardian_agent

# إضافة المسار الجذري (Root) لكي تتمكن الخدمة من قراءة الملفات الرئيسية
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyrogram import Client, filters
from pyrogram.types import Message

# استدعاء الأعضاء الحيوية من المسار الرئيسي (بدون backend_core)
from task_broker import broker
from context_vault import ContextVault
from services.sovereign_agents import guardian_agent  # <== أضف هذا السطر هنا

# إعداد مسجل الأحداث الخاص بطبقة الاتصال
logger = logging.getLogger("AymnGuard.TelegramGateway")

class TelegramGateway:
    """
    مدير اتصال تيليجرام بنمط (Singleton).
    """
    def __init__(self, bot_token: str, api_id: int, api_hash: str):
        self.app = Client(
            "AymnGuard_Sovereign_Session",
            bot_token=bot_token,
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True 
        )
        self._register_routes()
        
    def _register_routes(self) -> None:
        @self.app.on_message(filters.command("start") & filters.private)
        async def sovereign_start_command(client: Client, message: Message):
            user_id = str(message.from_user.id)
            logger.info(f"🛡️ [Telegram Gateway]: Secure /start signal received from {user_id}")
            
            await ContextVault.store_context(user_id, {"last_command": "/start", "platform": "telegram"})
            
            await message.reply_text(
                "**AymnGuard Enterprise v5.0** 🛡️\n\n"
                "تم تفعيل البروتوكولات السيادية بنجاح."
            )

        @self.app.on_message(filters.text & filters.private & ~filters.command("start"))
        async def ai_agent_dispatcher(client: Client, message: Message):
            user_id = str(message.from_user.id)
            payload_text = message.text
            
            logger.debug(f"📥 [Telegram Gateway]: Payload received from {user_id}. Dispatching...")

            async def send_typing_action(chat_id: int):
                # استدعاء حالة الكتابة مباشرة باستخدام raw API لتجنب استيراد enums
                await client.send_chat_action(chat_id, "typing")
                
            await broker.submit_task(send_typing_action, message.chat.id)

                # لاحظ المسافات هنا
        async def cognitive_task(uid: str, text: str, msg_obj: Message):
            try:
                ai_result = await guardian_agent.analyze_and_document(uid, text)
                response_text = f"⚙️ [المحرك العصبي]:\n\n{ai_result}"
                await msg_obj.reply_text(response_text)
            except Exception as e:
                logger.error(f"❌ [Telegram Gateway]: Agent failure for {uid} -> {e}")
                await msg_obj.reply_text("⚠️ تعذر إتمام بروتوكول التحليل السيادي.")

        # 🔥 الحل هنا: يجب أن يكون هذا السطر تحته مباشرة بنفس عدد المسافات بالضبط
        await broker.submit_task(cognitive_task, user_id, payload_text, message)


        # إرسال المهمة لوسيط المهام (Task Broker)
        await broker.submit_task(cognitive_task, user_id, payload_text, message)


    async def boot_gateway(self) -> None:
        logger.info("🚀 [Telegram Gateway]: Initiating secure connection to Telegram...")
        await self.app.start()
        logger.info("✅ [Telegram Gateway]: Online and listening.")
        
    async def shutdown_gateway(self) -> None:
        logger.info("🛑 [Telegram Gateway]: Terminating connection securely...")
        await self.app.stop()
