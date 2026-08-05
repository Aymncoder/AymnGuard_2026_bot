# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Task Broker (Asynchronous Job Queue)
==============================================================================
وسيط المهام: العصب المسؤول عن تنفيذ العمليات الثقيلة والمعقدة في الخلفية 
(Background Tasks) دون تعطيل استجابة النظام الرئيسية أو تجميد الواجهات.
مصمم ليعمل باستقلالية تامة عن البوابة الرئيسية لمنع تداخل المسارات والاصطدام.
"""

import asyncio
import logging
from typing import Callable, Any, Coroutine, List, Tuple

# إعداد مسجل الأحداث لطبقة وسيط المهام
logger = logging.getLogger("AymnGuard.TaskBroker")

class TaskBroker:
    """
    مدير مهام غير متزامن (Asynchronous) بمعايير مؤسسية.
    يقوم بتنظيم الطوابير (Queues) وإدارة الأخطاء ذاتياً لضمان عدم انهيار النظام 
    حتى تحت الضغط العالي أو عند فشل إحدى المهام الفرعية.
    """
    
    def __init__(self):
        # طابور المهام في الذاكرة (معمارية قابلة للتوسع للربط بقواعد رسائل خارجية لاحقاً)
        self._queue: asyncio.Queue = asyncio.Queue()
        self._is_running: bool = False
        self._workers: List[asyncio.Task] = []

    async def submit_task(self, task_func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any) -> None:
        """
        حقن مهمة جديدة في طابور المعالجة بأمان تام وسرعة فائقة.
        """
        await self._queue.put((task_func, args, kwargs))
        logger.debug(f"📥 [Task Broker]: New background task submitted -> {task_func.__name__}")

    async def _worker(self, worker_id: int) -> None:
        """
        العامل (Worker) المستقل: يسحب المهام من الطابور وينفذها بصمت.
        معزول تماماً لمعالجة أخطائه ذاتياً دون التأثير على استقرار العمال الآخرين.
        """
        logger.info(f"👷 [Worker {worker_id}]: Ready and listening for tasks...")
        while self._is_running:
            try:
                task_data: Tuple[Callable, Tuple, dict] = await self._queue.get()
                task_func, args, kwargs = task_data
                
                logger.info(f"⚙️ [Worker {worker_id}]: Executing task -> {task_func.__name__}")
                
                # التنفيذ الفعلي للمهمة
                await task_func(*args, **kwargs)
                
                self._queue.task_done()
                logger.info(f"✅ [Worker {worker_id}]: Task completed successfully -> {task_func.__name__}")
                
            except asyncio.CancelledError:
                # استجابة طبيعية عند طلب إيقاف النظام
                break
            except Exception as e:
                # احتواء الخطأ داخلياً ومنع تسربه للطبقات العليا
                logger.error(f"❌ [Worker {worker_id}]: Critical failure in task -> {e}", exc_info=True)

    async def start_broker(self, worker_count: int = 3) -> None:
        """
        إشعال محرك وسيط المهام وتشغيل العمال في الخلفية.
        """
        if self._is_running:
            logger.warning("⚠️ [Task Broker]: Broker is already active and running!")
            return
            
        self._is_running = True
        logger.info(f"🚀 [Task Broker]: Initializing with {worker_count} independent sovereign workers.")
        
        for i in range(worker_count):
            worker_task = asyncio.create_task(self._worker(i))
            self._workers.append(worker_task)

    async def stop_broker(self) -> None:
        """
        الإيقاف السيادي الآمن: ينتظر اكتمال المهام الحالية ثم يغلق النظام بسلام.
        """
        self._is_running = False
        logger.info("🛑 [Task Broker]: Initiating graceful shutdown. Waiting for queue to empty...")
        
        if self._workers:
            # ننتظر حتى تكتمل جميع المهام المعلقة في الطابور
            await self._queue.join()  
            for worker in self._workers:
                worker.cancel()
            await asyncio.gather(*self._workers, return_exceptions=True)
            self._workers.clear()
            
        logger.info("💤 [Task Broker]: Shutdown complete. All systems offline cleanly.")

# نسخة مفردة (Singleton) لتُستخدم في كافة أنحاء النظام لمنع تكرار الكائنات والمسارات
broker = TaskBroker()
