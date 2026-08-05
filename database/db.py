# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Ultimate Sovereign Database Engine & Connection Manager
النسخة الماسية المطورة كلياً: معالجة أقفال SQLite، إدارة تجمعات الاتصالات (Connection Pooling)،
الإغلاق النظيف (Graceful Shutdown)، وآليات إعادة المحاولة التلقائية المتقدمة.
"""

import os
import sys
import time
import logging
import asyncio
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import event

# --- حقن مسارات الجذر لضمان عمل الاستيرادات في أي بيئة تشغيل ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- استيراد آمن ومحصن لنموذج القاعدة (Base Model) ---
try:
    from .models import Base
except ImportError:
    try:
        from database.models import Base
    except ImportError:
        from models import Base

# إعداد السجلات المؤسسية
logger = logging.getLogger("AymnGuard.DatabaseEngine")
logger.setLevel(logging.INFO)

# قراءة رابط قاعدة البيانات مع دعم SQLite افتراضياً
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///aymnguard_enterprise.db")
is_sqlite = "sqlite" in DATABASE_URL

# إعدادات المحرك المتقدمة
engine_kwargs = {
    "echo": False,
    "future": True,
}

if not is_sqlite:
    engine_kwargs.update({
        "pool_size": 40,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_timeout": 30
    })
else:
    # تحسينات جذرية لبيئات SQLite لمنع أخطاء القفل وضمان الدعم المتزامن
    engine_kwargs.update({
        "connect_args": {
            "check_same_thread": False,
            "timeout": 30.0  # الانتظار حتى 30 ثانية قبل إطلاق خطأ القفل
        }
    })

# إنشاء محرك الاتصال غير المتزامن المتقدم
async_engine = create_async_engine(DATABASE_URL, **engine_kwargs)

# تفعيل مراقبة أحداث الاتصال في بيئات الإنتاج الكبرى
if not is_sqlite:
    @event.listens_for(async_engine.sync_engine, "connect")
    def receive_connect(dbapi_connection, connection_record):
        logger.debug("🔗 [DB Pool]: تم إرساء اتصال جديد بقاعدة البيانات بنجاح تام.")

# مصنع الجلسات غير المتزامنة المؤسسي
SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db(max_retries: int = 5, delay: float = 2.0) -> None:
    """
    إنشاء وتجهيز كافة جداول قاعدة البيانات آلياً مع نظام إعادة المحاولة التلقائي (Exponential Backoff).
    """
    for attempt in range(1, max_retries + 1):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("🗄️ [Database Engine]: تم إنشاء وتجهيز كافة جداول قاعدة البيانات السيادية بنجاح مطلق.")
            return
        except Exception as e:
            logger.warning(f"⚠️ [Database Warning]: المحاولة {attempt}/{max_retries} فشلت في الاتصال بقاعدة البيانات: {e}")
            if attempt == max_retries:
                logger.error("❌ [Database Critical]: فشل استنفاد محاولات الاتصال بقاعدة البيانات.", exc_info=True)
                raise
            await asyncio.sleep(delay * attempt)

async def close_db() -> None:
    """
    ميزة مؤسسية للإغلاق النظيف (Graceful Shutdown): تفريغ حوض الاتصالات وإغلاق المحرك بأمان عند إيقاف النظام.
    """
    try:
        await async_engine.dispose()
        logger.info("🔌 [Database Engine]: تم إغلاق محرك قاعدة البيانات وتفريغ التجمعات بنجاح نظيف.")
    except Exception as e:
        logger.error(f"❌ [Shutdown Error]: خطأ أثناء إغلاق محرك قاعدة البيانات: {e}")

async def check_database_health() -> dict:
    """
    فحص نبض وسلامة الاتصال بقاعدة البيانات لحظياً (Health Check Probe) مع قياس زمن الاستجابة (Latency).
    """
    start_time = time.time()
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        latency_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"🟢 [Database Health]: اتصال مستقر | زمن الاستجابة: {latency_ms}ms")
        return {"status": "healthy", "latency_ms": latency_ms, "engine": "AsyncIO SQLAlchemy"}
    except Exception as e:
        logger.error(f"🔴 [Database Health Alert]: فشل فحص سلامة قاعدة البيانات: {e}")
        return {"status": "unhealthy", "error": str(e)}

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    مولد جلسات قاعدة البيانات المؤسسي (Dependency Injection) للاستخدام الآمن داخل مسارات FastAPI.
    يضمن معالجة المعاملات بدقة ميكروسكوبية وإجراء التراجع الفوري (Rollback) عند حدوث أي استثناء.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ [Session Transaction Error]: استثناء في المعاملة، تم التراجع بنجاح: {e}")
            raise
        finally:
            await session.close()
