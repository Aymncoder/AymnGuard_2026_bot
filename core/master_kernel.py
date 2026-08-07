# core/master_kernel.py
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import String, Integer, DateTime, Boolean

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aymnguard_empire.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class MasterLicenseModel(Base):
    """النواة المركزية لإدارة المفاتيح السيادية والصلاحيات الموحدة للإمبراطورية"""
    __tablename__ = "master_licenses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    license_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    owner_chat_id: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # 1. صلاحيات أدوات النقل والتشغيل
    has_migration_tool: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 2. صلاحيات الحماية والتحكم بالمجموعات (نظام الخمس خانات)
    max_protection_slots: Mapped[int] = mapped_column(Integer, default=5)
    used_protection_slots: Mapped[int] = mapped_column(Integer, default=0)
    
    # 3. صلاحيات محلل الأسواق والمؤشرات المالية (Trading & Technical Analysis Core)
    has_trading_analyzer: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 4. صلاحيات استوديو الإبداع والتصميم بالذكاء الاصطناعي
    has_creative_studio: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # اشتراك الصيانة والدعم التشغيلي المستمر
    maintenance_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

async def init_master_kernel():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("💎 [النواة الإمبراطورية]: تم إرساء قاعدة بيانات المفاتيح وصلاحيات الخدمات الشاملة بنجاح.")
