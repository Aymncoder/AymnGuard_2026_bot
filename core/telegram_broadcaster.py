# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Broadcast Engine
محرك البث السيادي: المسؤول عن إرسال الردود، التقارير المالية، والرسائل العصبية 
من العقل المركزي إلى المستخدمين عبر Telegram API بشكل غير متزامن (Asynchronous).
"""

import logging
import aiohttp
import os
from typing import Optional, Dict, Any

logger = logging.getLogger("AymnGuard.Broadcaster")

class SovereignBroadcaster:
    """
    محرك البث الفضائي (Broadcaster):
    يتعامل حصرياً مع إرسال البيانات (رسائل، أزرار تفاعلية، إشعارات) إلى شبكة تيليجرام.
    """
    def __init__(self):
        # يفضل سحب التوكن من بيئة التشغيل (.env) لأسباب أمنية
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
        logger.info("📡 [Broadcast Engine]: تم تسليح محرك البث السيادي وهو جاهز للاتصال بشبكة تيليجرام.")

    async def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        """
        إرسال رسالة نصية (مع دعم HTML) وقوائم أزرار تفاعلية (إن وجدت) إلى العميل.
        """
        url = self.base_url + "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            # استخدام aiohttp لضمان عدم توقف الخادم أثناء انتظار رد تيليجرام
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"✉️ [Broadcast Success]: تم إرسال الرد السيادي للعميل [{chat_id}] بنجاح.")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ [Broadcast Failed]: فشل الإرسال للعميل [{chat_id}]. السبب: {error_text}")
                        return False
        except Exception as e:
            logger.error(f"❌ [Broadcast Exception]: انهيار في محرك الإرسال أثناء مخاطبة العميل [{chat_id}]: {e}")
            return False
