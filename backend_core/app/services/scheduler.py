import logging
import time
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED

# إعداد نظام التسجيل والتليمتري المؤسسي
logger = logging.getLogger("AymnGuardCore.EnterpriseScheduler")

# إنشاء جدول الخلفية المؤسسي متوافق مع معايير التوقيت العالمي الموحد (UTC)
scheduler = BackgroundScheduler(timezone=timezone.utc)

def background_health_audit_job() -> None:
    """مهمة خلفية دورية مؤمنة لفحص سلامة الذاكرة وموارد النظام السيادي"""
    try:
        current_utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        logger.info(f"🛡️ [Enterprise Telemetry] فحص سلامة النظام الخلفي الدوري نشط في: {current_utc_time}")
    except Exception as e:
        logger.error(f"❌ خطأ أثناء تنفيذ فحص السلامة الدوري: {e}")

def _job_listener(event) -> None:
    """مراقب أحداث المهام لتسجيل الأخطاء أو المهام الفائتة فور حدوثها"""
    if event.exception:
        logger.error(f"⚠️ فشلت المهمة المجدولة [{event.job_id}]: {event.exception}")
    else:
        logger.debug(f"✨ تمت جدولة وتنفيد المهمة [{event.job_id}] بنجاح.")

def setup_scheduler() -> None:
    """إعداد وتهيئة المهام الخلفية وربطها بالمستمعات ونظام التوقيت العالمي"""
    try:
        # إضافة مستمع الأحداث لتتبع دقة التشغيل
        scheduler.add_listener(_job_listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)

        # إضافة مهمة دورية تعمل بانتظام كل 10 دقائق بتوقيت UTC
        scheduler.add_job(
            background_health_audit_job,
            trigger=IntervalTrigger(minutes=10, timezone=timezone.utc),
            id="enterprise_health_audit_utc",
            name="AymnGuard Enterprise Health Audit (UTC)",
            replace_existing=True,
            misfire_grace_time=60
        )
        logger.info("⚙️ تم إعداد وتهيئة جدول المهام الخلفية المؤسسية (UTC) بنجاح تام وخلو كامل من التحذيرات.")
    except Exception as e:
        logger.critical(f"❌ خطأ حرج أثناء إعداد الجدول الزمني المؤسسي: {e}")
        raise

def start_scheduler() -> None:
    """إقلاع وتشغيل خادم الجدولة الخلفي بأمان ودون تعارض"""
    try:
        if not scheduler.running:
            scheduler.start()
            logger.info("▶️ تم إقلاع وتشغيل محرك الجدولة والمهام الخلفية بنجاح مؤسسي مطلق.")
        else:
            logger.warning("⚠️ محرك الجدولة يعمل مسبقاً بالفعل.")
    except Exception as e:
        logger.error(f"❌ فشل إقلاع محرك الجدولة: {e}")
        raise

def shutdown_scheduler() -> None:
    """إيقاف الجدول الزمني وتفريغ الموارد بأمان تام (Graceful Shutdown)"""
    try:
        if scheduler.running:
            scheduler.shutdown(wait=False)
            logger.info("🛑 تم إيقاف الجدول الزمني والمهام الخلفية بأمان تام وحفظ استقرار الموارد.")
        else:
            logger.info("ℹ️ محرك الجدولة لم يكن قيد التشغيل أثناء أمر الإغلاق.")
    except Exception as e:
        logger.error(f"❌ خطأ أثناء إيقاف محرك الجدولة: {e}")
