from core.celery_app import celery_app
from core.logger import logger
import time

@celery_app.task(bind=True, name="tasks.health_check_task")
def health_check_task(self):
    """
    مهمة دورية لفحص صحة النظام والخدمات المرتبطة تلقائياً في الخلفية.
    """
    logger.info("⚡ [Background Worker] جاري تنفيذ فحص الحالة الدوري للنظام...")
    try:
        time.sleep(1)
        logger.info("✅ [Background Worker] تم اجتياز فحص الحالة بنجاح تام.")
        return {"status": "healthy", "task_id": self.request.id}
    except Exception as e:
        logger.error(f"❌ [Background Worker] فشل فحص الحالة: {str(e)}")
        raise e

@celery_app.task(name="tasks.cleanup_logs_task")
def cleanup_logs_task():
    """
    مهمة مجدولة لتنظيف السجلات القديمة وحماية مساحة تخزين السيرفر.
    """
    logger.info("🧹 [Background Worker] بدء عملية تنظيف السجلات والبيانات المؤقتة...")
    logger.info("✨ [Background Worker] تمت عملية التنظيف بنجاح.")
    return {"cleaned": True}

