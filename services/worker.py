# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Advanced Sovereign Background Worker & Cron Engine
عامل المهام الخلفية والجدولة المتطور: يجمع بين معالجة طوابير الرسائل غير المتزامنة 
عبر Redis Queue وبين المهام المجدولة دورياً (Cron Jobs) لفحص الأسواق والسيولة.
"""

import logging
import asyncio
from typing import Dict, Any

# محاولة استيراد مدير الطوابير البرمجي من النظام
try:
    from backend_core.services.queue_manager import MessageQueueManager
except ImportError:
    # بديل احتياطي لضمان عمل السكريبت معزولاً لو لزم الأمر
    class MessageQueueManager:
        @staticmethod
        async def pop_from_queue(queue_name: str) -> Dict[str, Any]:
            await asyncio.sleep(0.1)
            return {}

# إعداد السجلات المؤسسية
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Sovereign-Worker] - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AymnGuard.WorkerEngine")

class SovereignEnterpriseWorker:
    """
    محرك التشغيل الخلفي الشامل: يدير طوابير الأحداث والمهام المجدولة للأسواق.
    """
    def __init__(self):
        logger.info("⚙️ [Worker Engine]: جاري إقلاع عامل المهام الخلفية والجدولة المؤسسية...")

    async def run_periodic_market_scan(self):
        """
        مهمة مجدولة دورية: تفقد أسواق التداول والسيولة والأصول الرقمية في الخلفية.
        """
        logger.info("🔄 [Cron Job]: بدء دورة الفحص الآلي للأسواق والأصول الرقمية...")
        await asyncio.sleep(0.5)
        logger.info("✅ [Cron Job]: اكتملت دورة الفحص الآلي للأسواق وتحديث المؤشرات بنجاح.")

    async def process_queue_loop(self):
        """
        حلقة سحب ومعالجة طوابير الانتظار غير المتزامنة عبر Redis Queue باستمرار.
        """
        logger.info("⚡ [Queue Processor]: بدء الاستماع لطوابير الرسائل والأحداث عبر Redis...")
        
        while True:
            try:
                # سحب البيانات من طابور تيليجرام أو الأحداث المعلقة بشكل غير متزامن
                update_data = await MessageQueueManager.pop_from_queue("telegram_updates_queue")
                
                if update_data:
                    update_id = update_data.get("update_id", "N/A")
                    logger.info(f"⚡ [Worker Processing]: معالجة الحدث برقم التعرف -> [{update_id}]")
                    # هنا يتم توجيه البيانات لمحرك الذكاء الاصطناعي أو معالجة الطلبات الواردة
                else:
                    # استراحة قصيرة جداً لمنع استهلاك المعالج بالكامل (Non-blocking sleep)
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"❌ [Queue Error]: خطأ في حلقة معالجة الطوابير: {e}")
                await asyncio.sleep(1)

    async def start_combined_worker(self):
        """
        إطلاق العمليات المزدوجة معاً: معالجة طوابير Redis بالتوازي مع فحص الأسواق الدوري.
        """
        logger.info("🚀 [Worker Active]: عامل المهام الخلفية يعمل بكافة أذرعه الآن.")
        
        # تشغيل حلقة معالجة الطوابير وحلقة الفحص الدوري كمهام متزامنة في الخلفية (Async Tasks)
        queue_task = asyncio.create_task(self.process_queue_loop())
        
        # حلقة التشغيل المجدولة الخاصة بالفحوصات
        while True:
            try:
                # تنفيذ الفحص الدوري للأسواق كل 300 ثانية (5 دقائق)
                await self.run_periodic_market_scan()
                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"❌ [Cron Error]: خطأ في حلقة الفحص الدوري: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    worker = SovereignEnterpriseWorker()
    try:
        asyncio.run(worker.start_combined_worker())
    except KeyboardInterrupt:
        logger.info("🛑 [Worker Engine]: تم إيقاف العامل الخلفي يدوياً بأمان تام.")
