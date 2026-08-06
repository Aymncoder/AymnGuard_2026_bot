# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Ultimate Sovereign Infrastructure & Connection Core
النسخة الماسية الفائقة والمدمجة كلياً: دمج النواة التحتية وهندسة تجمعات الاتصالات العالية الأداء 
مع نظام إعادة المحاولة الأسّي (Exponential Backoff)، الإغلاق النظيف (Graceful Shutdown)، 
ومسبار الفحص الحي الشامل بمعايير عمالقة التكنولوجيا العالمية.
"""

import os
import sys
import time
import logging
import asyncio
from typing import AsyncGenerator, Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import event

# --- حقن مسارات الجذر لضمان الاستقرار المطلق في مسارات التنفيذ وتجنب أي أخطاء استيراد ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- استيراد آمن ومحصن لنموذج القاعدة (Base Model) مع تغطية شاملة لجميع المسارات المحتملة ---
try:
    from .models import Base
except ImportError:
    try:
        from database.models import Base
    except ImportError:
        from models import Base

# إعداد السجلات المؤسسية والسيادية الموحدة
logger = logging.getLogger("AymnGuard.SovereignInfrastructureCore")
logger.setLevel(logging.INFO)

# قراءة رابط قاعدة البيانات مع توفير دعم SQLite افتراضي مدمج
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///aymnguard_enterprise.db")
is_sqlite = "sqlite" in DATABASE_URL

# إعدادات المحرك المتقدمة وعالية الأداء (Advanced Engine Parameters)
engine_kwargs: Dict[str, Any] = {
    "echo": False,
    "future": True,
}

if not is_sqlite:
    engine_kwargs.update({
        "pool_size": 50,         # استيعاب كثافة عالية جداً من الاتصالات المتزامنة لبيئات الإنتاج الضخمة
        "max_overflow": 25,      # مرونة فائقة لامتصاص أوقات الذروة المفاجئة والطلبات الضخمة
        "pool_pre_ping": True,   # فحص صحة الاتصال استباقياً لمنع تمرير استعلامات على قنوات تالفة
        "pool_recycle": 3600,    # تدوير الاتصالات دورياً كل ساعة لمنع تسريب الذاكرة والموارد
        "pool_timeout": 30       # مهلة الانتظار القصوى للحصول على اتصال متاح من الحوض
    })
else:
    # تحسينات جذرية مخصصة لبيئات SQLite لمنع أخطاء القفل وضمان الدعم المتزامن بسلاسة تامة
    engine_kwargs.update({
        "connect_args": {
            "check_same_thread": False,
            "timeout": 30.0  # الانتظار حتى 30 ثانية كحد أقصى قبل إطلاق خطأ قفل الجدول
        }
    })

# إنشاء محرك الاتصال غير المتزامن المتقدم والفائق (AsyncIO Sovereign Engine)
async_engine = create_async_engine(DATABASE_URL, **engine_kwargs)

# تفعيل مراقبة أحداث وتجمعات الاتصال في بيئات الإنتاج الكبرى (Enterprise Event Listeners)
if not is_sqlite:
    @event.listens_for(async_engine.sync_engine, "connect")
    def receive_connect(dbapi_connection, connection_record):
        logger.debug("🔗 [Sovereign Infrastructure Core]: تم إرساء اتصال جديد بقاعدة البيانات بكفاءة مطلقة.")

# مصنع الجلسات غير المتزامنة المؤسسي الموحد (Enterprise Async Session Maker)
SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db(max_retries: int = 5, delay: float = 2.0) -> None:
    """
    تهيئة البنية التحتية وإنشاء كافة الجداول السيادية آلياً مع تطبيق خوارزمية إعادة 
    المحاولة ذات التراجع الأسّي (Exponential Backoff Retry Mechanism) لاستيعاب أي تأخر في إقلاع الحاويات.
    """
    for attempt in range(1, max_retries + 1):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("🗄️ [Sovereign Infrastructure Core]: تم إنشاء وتجهيز الجداول السيادية بنجاح تام واستقرار 99.99%.")
            return
        except Exception as e:
            logger.warning(f"⚠️ [Infrastructure Warning]: المحاولة {attempt}/{max_retries} فشلت في الاتصال بالبنية التحتية: {e}")
            if attempt == max_retries:
                logger.error("❌ [Sovereign Infrastructure Critical]: فشل استنفاد كافة محاولات الاتصال بالبنية التحتية.", exc_info=True)
                raise
            # تطبيق تزايد أسي دقيق للفاصل الزمني لإعادة المحاولة لمنع إغراق الخادم
            backoff_delay = delay * (2 ** (attempt - 1))
            await asyncio.sleep(backoff_delay)

# محاذاة دالة التهيئة الاحتياطية لتتوافق مع المعيار المدمج
init_infrastructure = init_db

async def close_db() -> None:
    """
    ميزة مؤسسية متقدمة للإغلاق النظيف (Graceful Shutdown): تفريغ حوض الاتصالات 
    وإغلاق المحرك بأمان تام عند إيقاف تشغيل المنظومة لمنع أي تسريب للموارد.
    """
    try:
        await async_engine.dispose()
        logger.info("🔌 [Sovereign Infrastructure Core]: تم إغلاق محرك قاعدة البيانات وتفريغ التجمعات بنجاح نظيف.")
    except Exception as e:
        logger.error(f"❌ [Shutdown Error]: خطأ حرج أثناء إغلاق محرك قاعدة البيانات: {e}")

async def check_database_health() -> Dict[str, Any]:
    """
    مسبار الفحص الحي والمتقدم (Health Check & Latency Probe) لقياس نبض وسلامة 
    الاتصال بقاعدة البيانات لحظياً بدقة ميكروسكوبية لضمان الاستجابة الفورية (Zero-Lag).
    """
    start_time = time.time()
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"🟢 [Sovereign Infrastructure Health]: اتصال مستقر | زمن الاستجابة: {latency_ms}ms")
        return {
            "status": "healthy",
            "latency_ms": latency_ms,
            "engine": "AsyncIO SQLAlchemy Sovereign Core",
            "architecture": "Distributed Zero-Lag Ready"
        }
    except Exception as e:
        logger.error(f"🔴 [Sovereign Infrastructure Alert]: فشل فحص سلامة قاعدة البيانات: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "engine": "AsyncIO SQLAlchemy Sovereign Core"
        }

# محاذاة دالة فحص الصحة الاحتياطية لتتوافق مع المعيار المدمج
check_infrastructure_health = check_database_health

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    مولد جلسات قاعدة البيانات المؤسسي (Dependency Injection) للاستخدام الآمن داخل مسارات FastAPI وخلفيات العمل.
    يضمن إدارة المعاملات بدقة ميكروسكوبية وإجراء التراجع الفوري (Rollback) عند حدوث أي استثناء لتأمين سلامة البيانات.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ [Session Transaction Error]: استثناء في المعاملة، تم التراجع (Rollback) بأمان تام: {e}")
            raise
        finally:
            await session.close()

# محاذاة مولد الجلسات الاحتياطي لتتوافق مع المعيار المدمج
get_db_session = get_db
