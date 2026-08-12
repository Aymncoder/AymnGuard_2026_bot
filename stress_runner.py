# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Sovereign Stress & Load Testing Suite
==============================================================================
محاكي الضغط والتحمل السيادي (في المسار الرئيسي):
يقوم بإرسال مئات الطلبات المتزامنة (Concurrent Requests) إلى العقل المدبر 
`MasterSovereignOrchestrator` لقياس سرعة الاستجابة (Latency)، واختبار كفاءة التحمل.
"""

import asyncio
import time
import logging
from core.master_orchestrator import MasterSovereignOrchestrator

# إعداد السجلات الخاصة باختبارات التحمل
logging.basicConfig(level=logging.INFO, format="%(asctime)s ⚡ [Stress-Runner] %(levelname)s: %(message)s")
logger = logging.getLogger("AymnGuard.StressRunner")

async def simulate_single_user_request(orchestrator: MasterSovereignOrchestrator, user_id: int, message: str):
    """محاكاة طلب مستخدم مفترض لقياس الزمن وزرع الضغط."""
    start_time = time.time()
    try:
        username = f"StressUser_{user_id}"
        response = await orchestrator.orchestrate_user_request(
            telegram_id=str(100000 + user_id),
            username=username,
            message_text=message
        )
        duration = time.time() - start_time
        return {"success": True, "duration": duration, "status": response.get("status")}
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"❌ فشل الطلب للمستخدم {user_id}: {e}")
        return {"success": False, "duration": duration, "error": str(e)}

async def run_stress_test(total_requests: int = 100, concurrency_limit: int = 20):
    """
    تنفيذ هجوم ضغط واختبار تحلّل الأداء:
    - total_requests: إجمالي عدد الطلبات الوهمية.
    - concurrency_limit: عدد الطلبات التي تُنفذ في نفس اللحظة (متزامنة).
    """
    logger.info(f"🚀 [Stress Test Initiated]: بدء محاكاة ضغط بـ {total_requests} طلب (التزامن: {concurrency_limit})...")
    
    orchestrator = MasterSovereignOrchestrator()
    sample_messages = [
        "/start",
        "ذكاء: افحص كفاءة النظام",
        "/analyze BTCUSDT",
        "/audit 0x71C3...CustomToken",
        "القائمة الرئيسيه",
        "menu_admin_panel"
    ]
    
    semaphore = asyncio.Semaphore(concurrency_limit)
    
    async def bounded_task(idx: int):
        async with semaphore:
            msg = sample_messages[idx % len(sample_messages)]
            return await simulate_single_user_request(orchestrator, idx, msg)

    start_total_time = time.time()
    
    # تنفيذ المهام بالتزامن الموجه
    tasks = [bounded_task(i) for i in range(total_requests)]
    results = await asyncio.gather(*tasks)
    
    total_duration = time.time() - start_total_time
    
    # تحليل النتائج واستخراج مؤشرات الأداء
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    avg_latency = sum(r["duration"] for r in successful) / len(successful) if successful else 0.0
    
    logger.info("==================================================")
    logger.info("📊 [Stress Test Report - تقرير اختبار التحمل الأداء]:")
    logger.info(f"🔹 إجمالي الطلبات المُنفذة: {total_requests}")
    logger.info(f"✅ الطلبات الناجحة: {len(successful)}")
    logger.info(f"❌ الطلبات الفاشلة: {len(failed)}")
    logger.info(f"⏱️ الوقت الإجمالي للاختبار: {round(total_duration, 4)} ثانية")
    logger.info(f"⚡ متوسط زمن الاستجابة (Latency): {round(avg_latency * 1000, 2)} ميلي ثانية")
    logger.info("==================================================")

if __name__ == "__main__":
    asyncio.run(run_stress_test(total_requests=100, concurrency_limit=20))
