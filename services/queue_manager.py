# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Asynchronous Message Queue Manager
محرك طوابير الرسائل غير المتزامن لإدارة الأحداث والمهام عبر Redis
=============================================================================
"""

import json
import os
import logging
from dotenv import load_dotenv
import redis.asyncio as aioredis  # ⚡ [ترقية معمارية]: استخدام العميل غير المتزامن لمنع حظر خيط التنفيذ

load_dotenv()

logger = logging.getLogger("AymnGuardQueueEngine")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# تهيئة عميل Redis غير المتزامن (Async Redis Client)
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class MessageQueueManager:
    """
    مدير طوابير الرسائل غير المتزامن لتحقيق أعلى أداء ومعالجة فورية للبيانات.
    """

    @staticmethod
    async def push_to_queue(queue_name: str, data: dict) -> bool:
        """
        إدراج بيانات جديدة في الطوابير بصيغة غير متزامنة (Non-blocking).
        """
        try:
            await redis_client.rpush(queue_name, json.dumps(data))
            return True
        except Exception as e:
            logger.critical(f"❌ [Queue Push Error]: فشل دفع البيانات للطابور {queue_name} - التفاصيل: {str(e)}")
            return False

    @staticmethod
    async def pop_from_queue(queue_name: str) -> dict | None:
        """
        سحب ومعالجة العنصر التالي من الطوابير بكفاءة عالية وبشكل غير متزامن.
        """
        try:
            item = await redis_client.lpop(queue_name)
            return json.loads(item) if item else None
        except Exception as e:
            logger.critical(f"❌ [Queue Pop Error]: فشل سحب البيانات من الطابور {queue_name} - التفاصيل: {str(e)}")
            return None
