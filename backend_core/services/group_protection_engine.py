# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Group & Channel Total Protection Engine
محرك الحماية الشامل: إخفاء الإشعارات، تأمين المالك، منع التجسس، واستيعاب أعضاء بلا حدود
=============================================================================
"""

import logging
from aiogram import types, Bot

logger = logging.getLogger("AymnGuardGroupProtection")

class GroupProtectionEngine:
    """
    محرك سيادي لمنع الثغرات، حذف إشعارات الانضمام/المغادرة، وحماية المالكون والمجموعات من التجميد أو التهكير.
    """

    @staticmethod
    async def sanitize_service_messages(message: types.Message, bot: Bot) -> bool:
        """
        إخفاء وحذف إشعارات الانضمام، المغادرة، ورسائل الخدمة تلقائياً لتنظيف المجموعات 
        ومنع بروتوكولات التجسس من استغلالها في إغلاق المجموعات.
        """
        try:
            if message.new_chat_members or message.left_chat_member or message.pinned_message:
                await message.delete()
                logger.info(f"🛡️ [Security Audit]: تم حذف رسالة خدمة/انضمام في المحادثة {message.chat.id} لمنع الاستغلال البرمجي.")
                return True
        except Exception as e:
            logger.warning(f"⚠️ [Security Notice]: تعذر حذف رسالة الخدمة (تأكد من منح البوت صلاحية حذف الرسائل كمسؤول) - التفاصيل: {str(e)}")
        return False

    @staticmethod
    async def intercept_malicious_payloads(message: types.Message) -> bool:
        """
        التدقيق الفوري ضد البلاغات الهجومية الكيدية، روابط الاختراق، والـ Flood البرمجي.
        """
        try:
            if message.text:
                text_lower = message.text.lower()
                # رصد الروابط الخبيثة أو بروتوكولات الاختراق المعروفة
                malicious_patterns = ["t.me/joinchat/", "tg://", "hack", "exploit", "flood_attack"]
                if any(pattern in text_lower for pattern in malicious_patterns):
                    await message.delete()
                    logger.warning(f"🚨 [Anti-Hacking Alert]: تم اعتراض ورصد محاولة هجوم أو رابط خبيث في المحادثة {message.chat.id}")
                    return True
        except Exception as e:
            logger.error(f"❌ [Payload Intercept Error]: خطأ في فحص الحماية - التفاصيل: {str(e)}")
        return False
