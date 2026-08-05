# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Async Database Engine (v5.0 Unified)
محرك إدارة جلسات قاعدة البيانات غير المتزامنة وإنشاء الجداول تلقائياً
=============================================================================
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# استيراد النماذج الأساسية لجداول النظام السيادي
try:
    from backend_core.models.database_models import Base
except ImportError:
    try:
        from models.database_models import Base
    except ImportError:
        from .models.database_models import Base

load_dotenv()

# مسار قاعدة البيانات السيادية (يدعم SQLite المحلي أو خوادم PostgreSQL السحابية)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aymnguard_enterprise.db")

# إنشاء المحرك غير المتزامن (Async Engine) مع دعم التوافقية لـ SQLite
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# منشئ الجلسات غير المتزامن (Async Session Maker)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    """
    إنشاء وتوليد الجداول تلقائياً عند الإقلاع الأول للنظام السيادي.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """
    مُزود ومولد جلسات الاتصال غير المتزامن (Dependency) 
    لاستخدامه في مسارات FastAPI لضمان فتح الجلسات، الحفظ، التراجع عند الخطأ، والإغلاق بأمان تام.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
