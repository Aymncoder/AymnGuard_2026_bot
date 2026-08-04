# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Database & Cache Engine (Async)
==============================================================================
النظام المؤسسي المتكامل لإدارة اتصالات قاعدة البيانات (PostgreSQL Async) 
وذاكرة التخزين المؤقت الموزعة (Redis Async) بأعلى أداء واستقرار لاستيعاب الآلاف.
"""

import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
import redis.asyncio as redis

logger = logging.getLogger("AegisAICore.EnterpriseDatabase")

# جلب إعدادات البيئة مع قيم افتراضية مرنة
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password@localhost:5432/aymnguard_enterprise"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ==============================================================================
# 1. إعداد محرك PostgreSQL غير المتزامن (Connection Pooling محسن للذكاء السيادي)
# ==============================================================================
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=40,          # عدد الاتصالات النشطة الافتراضية في الخلفية
    max_overflow=60,       # الاتصالات الإضافية المسموح بها أوقات الذروة الكبرى
    pool_timeout=30,       # مهلة الانتظار للاتصال المتاح (بالثواني)
    pool_recycle=1800,     # إعادة تدوير الاتصالات كل 30 دقيقة لمنع انقطاعها
    pool_pre_ping=True     # فحص صحة الاتصال تلقائياً قبل الاستخدام لمنع الأخطاء الميتة
)

# مصنع الجلسات غير المتزامنة (Async Session Maker)
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# القاعدة الأساسية لجميع نماذج الجداول (ORM Models Base)
Base = declarative_base()


# ==============================================================================
# 2. مدير ذاكرة التخزين المؤقت الموزعة (Redis Async Manager)
# ==============================================================================
class EnterpriseRedisManager:
    def __init__(self):
        self.client: redis.Redis | None = None

    async def connect(self):
        """الاتصال بذاكرة Redis بشكل غير متزامن وآمن."""
        try:
            self.client = redis.from_url(
                REDIS_URL, 
                encoding="utf-8", 
                decode_responses=True,
                socket_timeout=5.0,
                retry_on_timeout=True
            )
            await self.client.ping()
            logger.info("✅ [Redis Async Engine]: تم الاتصال بذاكرة التخزين المؤقت بنجاح وبكفاءة عالية.")
        except Exception as e:
            logger.warning(f"⚠️ [Redis Warning]: تعذر الاتصال بـ Redis (النظام يعمل بوضع الاحتياط): {str(e)}")
            self.client = None

    async def disconnect(self):
        """إغلاق اتصال Redis بأمان عند إيقاف النظام."""
        if self.client:
            await self.client.close()
            logger.info("🛑 [Redis Async Engine]: تم إغلاق اتصال Redis بأمان وتفريغ الذاكرة.")

redis_manager = EnterpriseRedisManager()


# ==============================================================================
# 3. إدارة دورة حياة قواعد البيانات والاتصالات (Lifespan Handlers)
# ==============================================================================
async def init_databases() -> None:
    """فحص واختبار صحة الاتصال بقاعدة البيانات و Redis عند إقلاع النواة."""
    # فحص اتصال PostgreSQL
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("🗄️ [PostgreSQL Async]: تم التحقق من سلامة الاتصال بقاعدة البيانات بنجاح.")
    except Exception as e:
        logger.critical(f"❌ [PostgreSQL Critical]: فشل الاتصال بقاعدة البيانات: {str(e)}")
        raise e
    
    # تفعيل اتصال Redis
    await redis_manager.connect()

async def close_databases() -> None:
    """إغلاق محركات الاتصال وتفريغ الموارد بأمان تام عند إيقاف الخادم."""
    try:
        await engine.dispose()
        logger.info("🛑 [PostgreSQL Async]: تم إغلاق محرك الاتصال بقاعدة البيانات بأمان.")
    except Exception as e:
        logger.error(f"⚠️ [PostgreSQL Error]: خطأ أثناء إغلاق المحرك: {str(e)}")
    
    await redis_manager.disconnect()


# ==============================================================================
# 4. مزوّد الجلسات الآمن لكل طلب (Async Session Dependency)
# ==============================================================================
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    مزوّد جلسات قاعدة البيانات غير المتزامنة لكل طلب API
    مع ضمان الحفظ التلقائي (Commit) أو التراجع الآمن (Rollback) عند حدوث أي خطأ،
    وإغلاق الجلسة نهائياً لمنع تسريب الذاكرة (Memory Leaks).
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"⚠️ [Database Session Error]: تم التراجع عن المعاملة بسبب خطأ: {str(e)}")
            raise e
        finally:
            await session.close()
