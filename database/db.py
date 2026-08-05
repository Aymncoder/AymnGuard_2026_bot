# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Ultimate Sovereign Database Engine & Connection Manager
"""

import os
import sys
import logging

# إضافة الجذر الأساسي للمشروع إلى مسارات بايثون لضمان نجاح استيراد حزمة database
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
from database.models import Base
from .models import Base

# إعداد السجلات المؤسسية
logger = logging.getLogger("AymnGuard.DatabaseEngine")
logger.setLevel(logging.INFO)


# قراءة رابط قاعدة البيانات من المتغيرات البيئية مع دعم SQLite و PostgreSQL/MySQL افتراضياً
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///aymnguard_enterprise.db")

# تحديد إعدادات التجمع بناءً على نوع قاعدة البيانات لتجنب تعارضات SQLite ورفع الكفاءة لبيئات الإنتاج
is_sqlite = "sqlite" in DATABASE_URL

engine_kwargs = {
    "echo": False,
    "future": True,
}

if not is_sqlite:
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 3600
    })
else:
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False}
    })

# إنشاء محرك الاتصال غير المتزامن المتقدم (Advanced Async Engine)
async_engine = create_async_engine(DATABASE_URL, **engine_kwargs)

# مصنع الجلسات غير المتزامنة المؤسسي (Enterprise Async Session Maker)
SessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db() -> None:
    """
    إنشاء كافة الجداول والنماذج في قاعدة البيانات آلياً عند إقلاع النظام مع معالجة استباقية للأخطاء.
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("🗄️ [Database Engine]: تم إنشاء وتجهيز كافة جداول قاعدة البيانات السيادية بنجاح مطلق.")
    except Exception as e:
        logger.error(f"❌ [Database Error]: فشل حرج في تهيئة قاعدة البيانات: {e}", exc_info=True)
        raise

async def check_database_health() -> bool:
    """
    ميزة مؤسسية متقدمة: فحص نبض وسلامة الاتصال بقاعدة البيانات لحظياً (Health Check Probe).
    """
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        logger.info("🟢 [Database Health]: اتصال قاعدة البيانات مستقر ويعمل بكفاءة Zero-Lag.")
        return True
    except Exception as e:
        logger.error(f"🔴 [Database Health Alert]: فشل فحص سلامة قاعدة البيانات: {e}")
        return False

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    مولد جلسات قاعدة البيانات المؤسسي (Dependency Injection) للاستخدام الآمن داخل مسارات FastAPI وخلفيات العمل.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ [Session Transaction Error]: حدث استثناء أثناء إدارة المعاملة، تم التراجع (Rollback) بنجاح: {e}")
            raise
        finally:
            await session.close()
