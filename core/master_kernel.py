# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.1.0 : Master Kernel & Database Models
==============================================================================
النواة الرئيسية للإمبراطورية: تعريف جداول التراخيص الصارمة (ORM)،
إدارة الاتصالات غير المتزامنة (Async)، وضمان استقرار قواعد البيانات.
تم تصحيح أخطاء الاستيراد والروابط لتتطابق مع بيئة الإنتاج السحابية.
==============================================================================
"""

import os
import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Integer, String, DateTime, Boolean

logger = logging.getLogger("SovereignMasterKernel")
logger.setLevel(logging.INFO)

# 1. جلب رابط قاعدة البيانات مع دعم كامل للاتصال اللامتزامن (aiosqlite)
DATABASE_URL = os.getenv("CORE_DATABASE_URL", "sqlite+aiosqlite:///./aymnguard_empire.db")

# تصحيح مسار الاتصال ليتوافق مع معيار async sqlite
if DATABASE_URL.startswith("sqlite:///"):
    DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class MasterLicenseModel(Base):
    """النواة المركزية لإدارة المفاتيح والصلاحيات الموحدة للإمبراطورية"""
    __tablename__ = "master_licenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    license_key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    owner_chat_id: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # 1. صلاحيات أدوات النقل والتشغيل (Migration & Termux Tools)
    has_migration_tool: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 2. صلاحيات الحماية والتحكم بالمجموعات (نظام الخمس خانات)
    max_protection_slots: Mapped[int] = mapped_column(Integer, default=5)
    used_protection_slots: Mapped[int] = mapped_column(Integer, default=0)
    
    # 3. صلاحيات محل الأسواق والمؤشرات المالية (Trading & Technical Analysis Core)
    has_trading_analyzer: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 4. صلاحيات استوديو الإبداع والتصميم بالذكاء الاصطناعي
    has_creative_studio: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 5. اشتراك الصيانة والدعم التشغيلي المستمر
    maintenance_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

async def init_master_kernel():
    """
    بناء وإطلاق قاعدة بيانات المفاتيح والصلاحيات الشاملة بأسلوب لامتزامن وآمن تماماً.
    """
    try:
        async with engine.begin() as conn:
            logger.info("[Master Kernel]: جاري فحص وبناء جداول التراخيص السيادية...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("[Master Kernel]: تم إرساء قاعدة بيانات المفاتيح والصلاحيات الشاملة بنجاح [الدولة الإمبراطورية].")
    except Exception as e:
        logger.critical(f"[Master Kernel Critical Error]: فشل إقلاع النواة الرئيسية وقاعدة البيانات: {e}")
        raise
