# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Asynchronous Background Worker
عامل المعالجة الخلفي غير المتزامن لمعالجة أحداث وتحديثات النظام بأداء فائق
=============================================================================
"""

import asyncio
import logging
from backend_core.services.queue_manager import MessageQueueManager

# تهيئة نظام الصندوق الأسود اللوجستي للرصد الحي
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AymnGuardWorkerEngine")

async def start_worker():
    """
    حلقة المعالجة الخلفية غير المتزامنة للاستمرار في سحب ومعالجة الرسائل من Redis Queue.
    """
    logger.info("🛡️ [Worker Engine]: بدأ تشغيل العامل الخلفي وهو يستمع لطوابير Redis بوضع غير متزامن...")
    
    while True:
        try:
            # ⚡ [تصحيح جذري]: استخدام await لانتظار استجابة دالة السحب غير المتزامنة
            update_data = await MessageQueueManager.pop_from_queue("telegram_updates_queue")

            if update_data:
                update_id = update_data.get("update_id", "N/A")
                logger.info(f"⚡ [Worker Processing]: جاري معالجة الحدث برقم التعرف ID: {update_id}")
                # هنا سيتم توجيه البيانات لمحرك الذكاء الاصطناعي أو معالجة الطلبات اللوجستية
            else:
                # استراحة قصيرة جداً (Non-blocking sleep) لمنع استنزاف المعالج عند خلو الطابور
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.critical(f"❌ [Worker Loop Error]: خطأ حرج في حلقة العامل الخلفي - التفاصيل: {str(e)}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    # تشغيل حلقة الأحداث غير المتزامنة لنواة العامل
    try:
        asyncio.run(start_worker())
    except KeyboardInterrupt:
        logger.info("🛑 [Worker Engine]: تم إيقاف العامل الخلفي يدوياً بأمان تام.")
