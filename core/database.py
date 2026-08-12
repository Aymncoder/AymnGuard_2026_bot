# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Database Core (v18.1.0-Cloud Enterprise)
==============================================================================
نواة قاعدة البيانات الإمبراطورية: اتصال غير متزامن (Async)، 
إدارة متقدمة للاتصالات، وحماية مطلقة من تجميد السيرفر (Non-blocking).
تم تطهيره بالكامل من الرموز التعبيرية لضمان الاستقرار المطلق في بيئة الإنتاج السحابية.
==============================================================================
"""

import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.models import Base

logger = logging.getLogger("SovereignDatabaseCore")
logger.setLevel(logging.INFO)

# 1. جلب الرابط ديناميكياً (جاهز للانتقال لـ PostgreSQL السحابي المدفوع بضغطة زر)
DATABASE_URL = os.getenv("CORE_DATABASE_URL", "sqlite+aiosqlite:///./sovereign_empire.db")

# 2. بناء المحرك غير المتزامن (Async Engine) مع تحسينات الأداء السحابي
engine_kwargs = {"echo": False, "future": True}

if "sqlite" in DATABASE_URL:
    # إعدادات خاصة لـ SQLite لتعمل بكفاءة مع اللاتزامن والضغط العالي
    engine_kwargs["connect_args"] = {"timeout": 30}
else:
    # إعدادات متقدمة لقواعد البيانات السحابية الضخمة (PostgreSQL / MySQL)
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 1800,
        "pool_pre_ping": True
    })

engine = create_async_engine(DATABASE_URL, **engine_kwargs)

# 3. صانع الجلسات اللامتزامن (Async Session Factory)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def init_db():
    """
    بناء الجداول تلقائياً بأسلوب غير متزامن (Async) لكي لا يجمد السيرفر عند الإقلاع.
    """
    try:
        async with engine.begin() as conn:
            logger.info("[DB Core]: جاري تهيئة وهندسة جداول قاعدة البيانات المركزية...")
            # استخدام run_sync لتشغيل أوامر البناء التقليدية داخل بيئة لامتزامنة
            await conn.run_sync(Base.metadata.create_all)
            logger.info("[DB Core]: تمت تهيئة كافة الجداول والهياكل بنجاح مؤسسي.")
    except Exception as e:
        logger.critical(f"[DB Core Error]: فشل حرج في بناء قاعدة البيانات: {e}")
        raise
