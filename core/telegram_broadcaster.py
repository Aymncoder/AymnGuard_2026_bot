# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.1.0 : Sovereign Broadcast Engine (Cloud Optimized)
==============================================================================
محرك البث السيادي: المسؤول عن إرسال الردود والتقارير المالية والرسائل
بشكل غير متزامن (Asynchronous) من خوادم تيليجرام إلى المستخدمين.
تم تحسين استهلاك الـ TCP Sockets للعمل بكفاءة فائقة على السيرفرات السحابية.
==============================================================================
"""

import os
import logging
import asyncio
import aiohttp
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
        logger.info("[Broadcast Engine]: تم تسليح محرك البث السيادي وهو جاهز للاتصال بشبكة تيليجرام.")

    async def send_message(self, chat_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> bool:
        """
        إرسال رسالة نصية (مع دعم HTML والأزرار التفاعلية إن وجدت) بشكل لامتزامن وآمن تماماً.
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
        
        # فتح جلسة اتصال واحدة لتوفير الموارد أثناء المحاولات المتكررة (Optimized TCP Pooling)
        try:
            async with aiohttp.ClientSession() as session:
                for attempt in range(1, max_retries + 1):
                    try:
                        # وضع مهلة زمنية (Timeout=10s) لمنع الخادم من التعليق
                        async with session.post(url, json=payload, timeout=10.0) as response:
                            if response.status == 200:
                                logger.info(f"[Broadcast Success]: تم إرسال الرد السيادي للعميل [{chat_id}] بنجاح.")
                                return True
                            else:
                                error_text = await response.text()
                                logger.warning(f"[Broadcast Warning]: فشل الإرسال للعميل [{chat_id}] (محاولة {attempt}/{max_retries}) - السبب: {error_text}")
                                
                                # إذا كان الخطأ بسبب تجاوز الحد (FloodWait)، ننتظر قليلاً
                                if response.status == 429:
                                    await asyncio.sleep(3)
                                else:
                                    await asyncio.sleep(1)
                    except asyncio.TimeoutError:
                        logger.warning(f"[Broadcast Timeout]: انقضت مهلة الاتصال أثناء إرسال الرسالة لـ [{chat_id}] (محاولة {attempt})")
                        await asyncio.sleep(1.5)
                    except Exception as e:
                        logger.error(f"[Broadcast Exception]: انهيار في محرك الإرسال أثناء مخاطبة العميل [{chat_id}] -> {e}")
                        await asyncio.sleep(1)
                        
        except Exception as core_error:
            logger.error(f"[Broadcast Fatal]: فشل في تهيئة جلسة الاتصال الأساسية: {core_error}")

        logger.error(f"[Broadcast Failure]: تعذر إرسال الرسالة للعميل [{chat_id}] بعد استنفاد كافة المحاولات.")
        return False
