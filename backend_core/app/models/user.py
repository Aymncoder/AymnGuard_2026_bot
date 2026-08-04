import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.database import Base

class UserRole(str, enum.Enum):
    """تصنيف الأدوار والصلاحيات الهيكلية للمنصات اللوجستية والمؤسسية المتقدمة"""
    ADMIN = "admin"
    LOGISTICS_MANAGER = "logistics_manager"
    OPERATOR = "operator"
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"

    # المعرف الفريد العالمي (UUIDv4) لضمان التوافق مع أنظمة قواعد البيانات الموزعة وسلاسل الإمداد المعقدة
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True, 
        nullable=False
    )
    
    # الهوية الرقمية والتعريفية للمستخدم (مدمجة من البنية الكلاسيكية والمستقبلية)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True, nullable=True)
    
    # نموذج التحكم بالوصول القائم على الأدوار (RBAC) لفرق العمل والعمليات اللوجستية
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), 
        default=UserRole.CLIENT, 
        nullable=False,
        index=True
    )
    
    # حالات الحساب والتحقق الأمني والمصادقة المتقدمة
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # حماية المعاملات الحساسة عبر نظام المصادقة الثنائية (MFA)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # سجلات التتبع الأمني واللوجستي والمقاييس التشغيلية
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True) # يدعم صيغ نطاق عناوين IPv4 و IPv6 معاً
    
    # مسار التدقيق الزمني وإدارة الحذف الناعم (Soft Delete) للحفاظ على نزاهة السجلات اللوجستية والتاريخية
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<EnterpriseLogisticsUser(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}', active={self.is_active})>"

