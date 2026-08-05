import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from core.agents.security_agent import CommunitySecurityAgent

# تهيئة السجلات المؤسسية
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Telegram_Gateway")

# استدعاء الوكيل الأمني المركزي
security_agent = CommunitySecurityAgent()

class SovereignTelegramGateway:
    """
    بوابة الاتصال السيادية: مسؤولة عن إدارة تدفق البيانات من وإلى شبكة تيليجرام.
    مصممة لتحمل الضغط العالي وتوجيه الأحداث بذكاء إلى الوكلاء المختصين.
    """
    def __init__(self, api_id: int, api_hash: str, bot_token: str):
        self.app = Client(
            "AymnGuard_Enterprise",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            in_memory=True # تقليل استهلاك الإدخال والإخراج (I/O) لسرعة استجابة استثنائية
        )
        self._register_routes()

    def _register_routes(self):
        """ربط الأحداث الخارجية بالخوارزميات الداخلية"""
        
        @self.app.on_message(filters.new_chat_members)
        async def on_new_member(client: Client, message: Message):
            for user in message.new_chat_members:
                logger.info(f"🛡️ تم رصد دخول جديد: {user.first_name} (ID: {user.id})")
                # توجيه الحدث فوراً إلى الوكيل الأمني للتحليل واتخاذ القرار
                await security_agent.analyze_user_behavior(
                    telegram_id=user.id, 
                    username=user.username or "Unknown"
                )

        @self.app.on_message(filters.group & filters.text)
        async def on_group_message(client: Client, message: Message):
            # هنا يمكننا لاحقاً إضافة فحص الرسائل المزعجة (Spam) أو الكلمات المحظورة
            pass

    def open_gates(self):
        """إطلاق البوابة وربطها بشبكة تيليجرام العالمية"""
        logger.info("🚀 جاري فتح بوابات تيليجرام السيادية...")
        self.app.run()

# ملاحظة: سيتم تشغيل البوابة من خلال ملف main.py لاحقاً
