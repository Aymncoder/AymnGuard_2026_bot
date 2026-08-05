# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Telegram Business & Premium Features Engine
محرك إدارة تليجرام الأعمال والميزات المتقدمة والربط السيادي بالخدمات
=============================================================================
"""

import logging
import json
from aiogram import types
from backend_core.services.queue_manager import MessageQueueManager

logger = logging.getLogger("AymnGuardBusinessEngine")

class TelegramBusinessManager:
    """
    مدير أعمال تليجرام لمعالجة اتصالات الحسابات التجارية، الرسائل، والتحديثات المتقدمة.
    """

    @staticmethod
    async def handle_business_connection(connection: types.BusinessConnection):
        """
        معالجة حالة اتصال أو إلغاء اتصال حساب تجاري (Business Connection) بالبوت.
        """
        try:
            connection_id = connection.id
            user_id = connection.user.id
            is_enabled = connection.is_enabled
            
            logger.info(f"💼 [Telegram Business]: تحديث اتصال تجاري - المستخدم: {user_id}, الحالة: {'مفعل' | 'معطل'}, المعرف: {connection_id}")
            
            # دفع الحدث لطوابير Redis للاستجابة الفورية والمعالجة الخلفية
            await MessageQueueManager.push_to_queue("telegram_business_queue", {
                "event_type": "business_connection",
                "connection_id": connection_id,
                "user_id": user_id,
                "is_enabled": is_enabled,
                "date": connection.date
            })
            return True
        except Exception as e:
            logger.error(f"❌ [Business Connection Error]: فشل معالجة الاتصال التجاري - التفاصيل: {str(e)}")
            return False

    @staticmethod
    async def handle_business_message(message: types.Message):
        """
        معالجة الرسائل الواردة نيابة عن الحساب التجاري (Business Messages).
        """
        try:
            business_connection_id = message.business_connection_id
            user_id = message.from_user.id if message.from_user else "N/A"
            text = message.text or "[محتوى غير نصي/وسائط]"
            
            logger.info(f"💬 [Business Message]: استقبال رسالة تجارية عبر المعرف {business_connection_id} من المستخدم {user_id}")
            
            # إرسال الرسالة إلى طوابير النظام لتحليلها عبر الذكاء الاصطناعي أو الرد التلقائي
            await MessageQueueManager.push_to_queue("telegram_business_messages_queue", {
                "event_type": "business_message",
                "business_connection_id": business_connection_id,
                "user_id": user_id,
                "text": text,
                "message_id": message.message_id
            })
            return True
        except Exception as e:
            logger.error(f"❌ [Business Message Error]: فشل معالجة الرسالة التجارية - التفاصيل: {str(e)}")
            return False
