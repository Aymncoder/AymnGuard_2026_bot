# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Asynchronous Database Engine
إدارة جلسات الاتصال بقاعدة البيانات بصيغة غير متزامنة (Async SQLAlchemy Session)
=============================================================================
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# استدعاء رابط قاعدة البيانات الموحد
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aymnguard_enterprise.db")

# إنشاء المحرك غير المتزامن (Async Engine)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# منشئ الجلسات غير المتزامن
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """
    مُزود الجلسات (Dependency) لاستخدامه في مسارات FastAPI لضمان فتح وإغلاق الجلسات بأمان.
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
