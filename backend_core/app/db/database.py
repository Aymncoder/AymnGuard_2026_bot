import os
import time
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# إعداد نظام التسجيل الخاص بقاعدة البيانات
logger = logging.getLogger("AymnGuardCore.Database")

# تحديد رابط قاعدة البيانات مع قيم افتراضية مؤسسية
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite+aiosqlite:///./aymnguard_enterprise.db"
)

# إعداد محرك الاتصال المؤسسي مع ميزات تدوير الجلسات وإدارة الذاكرة المؤقتة
engine_kwargs = {"echo": False, "future": True}
if "sqlite" in DATABASE_URL:
    # إعدادات خاصة لـ SQLite لتحسين التزامن
    engine_kwargs["connect_args"] = {"timeout": 30}
else:
    # إعدادات مخصصة لقواعد البيانات العلائقية الكبرى (PostgreSQL / MySQL)
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 1800,
        "pool_pre_ping": True
    })

engine = create_async_engine(DATABASE_URL, **engine_kwargs)

# مُنشئ الجلسات المؤسسي المتقدم
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

async def init_databases() -> None:
    """إتهام وتهيئة الجداول والهياكل الأساسية لقاعدة البيانات بآمان تام"""
    try:
        async with engine.begin() as conn:
            logger.info("⚙️ بدء عملية المزامنة وهندسة الجداول داخل قاعدة البيانات...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ تمت تهيئة كافة الجداول والهياكل بنجاح مؤسسي.")
    except SQLAlchemyError as e:
        logger.critical(f"❌ خطأ حرج أثناء تهيئة قاعدة البيانات: {e}")
        raise

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """مولد جلسات قاعدة البيانات مع تتبع الأداء وإدارة المعاملات التلقائية"""
    async with AsyncSessionLocal() as session:
        start_time = time.time()
        try:
            yield session
            await session.commit()
        except Exception as err:
            await session.rollback()
            logger.error(f"⚠️ حدث خطأ أثناء المعاملة البرمجية، تم التراجع (Rollback): {err}")
            raise
        finally:
            await session.close()
            duration = time.time() - start_time
            if duration > 1.0:  # تسجيل تنبيه إذا استغرق الاستعلام وقتاً طويلاً
                logger.warning(f"⏱️ تنبيه أداء: استغرقت الجلسة وقت طويل نسبياً ({duration:.4f}s)")

@asynccontextmanager
async def get_isolated_db_session() -> AsyncGenerator[AsyncSession, None]:
    """مدير سياق معزول (Context Manager) للعمليات الخلفية والمهام المجدولة خارج المسارات"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ خطأ في الجلسة المعزولة: {e}")
            raise
        finally:
            await session.close()
