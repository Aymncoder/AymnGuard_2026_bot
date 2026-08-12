# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Ecosystem Automation (v18.1.0-Cloud Enterprise)
==============================================================================
محرك الأتمتة السيادي (نسخة التوافق المطلق مع Pyrogram والبيئة السحابية):
سحب البيانات، النشر الفيروسي، وإدارة الأرقام الافتراضية مع حماية صارمة ضد الحظر.
تم تطهيره بالكامل من الرموز التعبيرية لضمان الاستقرار المطلق في بيئة الإنتاج.
==============================================================================
"""

import os
import logging
import asyncio
import aiohttp
from typing import Dict, Any, List
from pyrogram import Client
from pyrogram.errors import FloodWait

logger = logging.getLogger("AymnGuard.AutomationEngine")
logger.setLevel(logging.INFO)

class EcosystemAutomationEngine:
    """محرك أتمتة الشبكات والتوسع الفيروسي السيادي"""

    def __init__(self):
        # 1. سحب المفاتيح بأمان من البيئة بدل كتابتها مكشوفة (أمان مؤسسي)
        self.api_id = int(os.getenv("TELEGRAM_API_ID", "6"))
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
        self.sms_api_key = os.getenv("VIRTUAL_NUMBER_API_KEY", "")
        self.sms_api_url = "https://api.sms-activate.org/stubs/handler_api.php"
        
        logger.info("[Automation Engine]: تمت تهيئة محرك الأتمتة السيادي بنجاح وبسرية تامة.")

    # =========================================================================
    # 1. وحدة الاستخراج والترحيل (Scraping & Migration) مع درع الحظر
    # =========================================================================
    async def scrape_active_users(self, client: Client, group_username: str, limit: int = 100) -> Dict[str, Any]:
        """سحب بيانات الأعضاء النشطين مع درع الحماية من الحظر (FloodWait)."""
        logger.info(f"[Data Scraping]: بدء سحب الأعضاء من {group_username}...")
        
        if not client.is_connected:
            return {"status": "error", "message": "الوكيل غير متصل بالشبكة، يرجى تمرير جلسة نشطة."}
            
        users_data = []
        try:
            # استخدام Pyrogram لجلب الأعضاء بشكل آمن ومتوافق مع باقي النظام
            async for member in client.get_chat_members(group_username, limit=limit):
                if member.user.is_bot or member.user.is_deleted:
                    continue
                    
                users_data.append({
                    "id": member.user.id,
                    "username": member.user.username,
                    "first_name": member.user.first_name
                })
                
                # درع التبريد: استراحة بسيطة كل 50 مستخدم لمنع الحظر السريع
                if len(users_data) % 50 == 0:
                    await asyncio.sleep(1)

            logger.info(f"[Data Scraping]: تم سحب {len(users_data)} عضو بنجاح.")
            return {"status": "success", "data": users_data}

        except FloodWait as e:
            logger.warning(f"[Scrape FloodWait]: حماية تيليجرام نشطة، يجب الانتظار {e.value} ثانية.")
            return {"status": "rate_limit", "wait_time": e.value, "partial_data": users_data}
        except Exception as e:
            logger.error(f"[Scrape Error]: فشل السحب من {group_username}: {e}")
            return {"status": "error", "message": str(e)}

    # =========================================================================
    # 2. البث الفيروسي وتوجيه الإعلانات (Mass Broadcasting)
    # =========================================================================
    async def broadcast_sovereign_announcement(self, client: Client, target_users: List[int], message: str) -> Dict[str, Any]:
        """النشر الفيروسي الآمن مع فترات راحة ديناميكية لتجنب حرق الرقم (Anti-Spam Shield)."""
        logger.info(f"[Mass Broadcast]: بدء النشر الفيروسي لـ {len(target_users)} مستخدم...")
        
        success_count = 0
        failed_count = 0
        
        for index, user_id in enumerate(target_users):
            try:
                await client.send_message(chat_id=user_id, text=message)
                success_count += 1
                
                # درع التبريد الديناميكي (Dynamic Cool-down) يحاكي السلوك البشري
                if index > 0 and index % 10 == 0:
                    logger.debug("[Broadcast]: تبريد الأنابيب لـ 5 ثواني لتجنب الحظر...")
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(0.8) # استراحة خفيفة بين كل رسالة وأخرى
                    
            except FloodWait as e:
                logger.warning(f"[Broadcast FloodWait]: إيقاف إجباري لـ {e.value} ثانية. جاري الانتظار...")
                await asyncio.sleep(e.value)
            except Exception as e:
                failed_count += 1
                logger.debug(f"[Broadcast Warning]: فشل الإرسال للمستخدم {user_id}: {e}")

        logger.info(f"[Broadcast Finished]: تم التسليم: {success_count} | فشل: {failed_count}")
        return {"status": "success", "sent": success_count, "failed": failed_count}
        
    # =========================================================================
    # 3. إدارة الأرقام الافتراضية (Virtual Numbers Integration)
    # =========================================================================
    async def request_virtual_number(self, country: str = "ru", service: str = "tg") -> Dict[str, Any]:
        """طلب رقم افتراضي عبر واجهة API بشكل غير متزامن تماماً (Async)."""
        if not self.sms_api_key:
            return {"status": "error", "message": "لم يتم إعداد مفتاح API للأرقام الافتراضية في بيئة النظام."}
            
        params = {
            "api_key": self.sms_api_key,
            "action": "getNumber",
            "service": service,
            "country": country
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.sms_api_url, params=params) as response:
                    text = await response.text()
                    if "ACCESS_NUMBER" in text:
                        _, req_id, phone = text.split(":")
                        return {"status": "success", "phone": phone, "req_id": req_id}
                    return {"status": "error", "message": text}
        except Exception as e:
            return {"status": "error", "message": f"حدث خطأ في الاتصال بمزود الأرقام: {str(e)}"}
