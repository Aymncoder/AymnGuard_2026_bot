# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Sovereign Broadcast Engine
==============================================================================
محرك البث السيادي: المسؤول عن إرسال الردود التقارير المالية، والرسائل العصبيّة
(Asynchronous) بشكل غير متزامن من API Telegram إلى المستخدمين غير
المتصلين مع درع حماية متقدم وإعادة محاولة تلقائية.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any

# إعداد نظام السجلات السيادي
logger = logging.getLogger("AymnGuard.Broadcaster")
logger.setLevel(logging.INFO)

class SovereignBroadcaster:
    """
    محرك البث الفضائي (Broadcaster): 
    يتعامل حصرياً مع إرسال البيانات (رسائل، أزرار تفاعلية، إشعارات) إلى شبكة تيليجرام بأمان تام.
    """
    def __init__(self):
        # لأسباب أمنية (env)، يُجلَب التوكن من بيئة التشغيل مع قيمة افتراضية آمنة
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        logger.info("📡 [Broadcast Engine]: تم تسليح محرك البث السيادي وهو جاهز الاتصال بشبكة تيليجرام.")

    async def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        """
        إرسال رسالة نصية (مع دعم HTML مع الأزرار التفاعلية إن وجدت) بشكل لامتزامن وآمن تماماً.
        """
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        if reply_markup:
            payload["reply_markup"] = reply_markup

        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                # ضمان عدم توقف الخادم أثناء الاتصال ووضع مهلة زمنية (Timeout=10s)
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, timeout=10) as response:
                        if response.status == 200:
                            logger.info(f"📤 [Broadcast Success]: تم إرسال الرد السيادي للعميل [{chat_id}] بنجاح.")
                            return True
                        else:
                            error_text = await response.text()
                            logger.warning(f"⚠️ [Broadcast Warning]: فشل الإرسال للعميل [{chat_id}] (محاولة {attempt}/{max_retries}) - السبب: {error_text}")
                            
                            # إذا كان الخطأ بسبب تجاوز الحد (FloodWait)، ننتظر قليلاً
                            if response.status == 429:
                                await asyncio.sleep(3)
                            else:
                                await asyncio.sleep(1)
            except asyncio.TimeoutError:
                logger.warning(f"⚠️ [Broadcast Timeout]: انقضت مهلة الاتصال أثناء إرسال الرسالة لـ [{chat_id}] (محاولة {attempt})")
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f"❌ [Broadcast Exception]: الانهيار في محرك الإرسال أثناء مخاطبة العميل [{chat_id}] -> {e}")
                await asyncio.sleep(1)

        logger.error(f"❌ [Broadcast Failure]: تعذر إرسال الرسالة للعميل [{chat_id}] بعد استنفاد المحاولات.")
        return False
