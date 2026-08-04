from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

class TimestampMixin:
    """مكسن التتبع الزمني المتقدم للعمليات اللوجستية والمؤسسية"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
        comment="تاريخ ووقت إنشاء السجل اللوجستي"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False,
        comment="تاريخ ووقت آخر تحديث للبيانات"
    )

class SoftDeleteMixin:
    """مكسن الحذف الناعم لضمان عدم ضياع السجلات المالية والتاريخية للعمليات اللوجستية"""
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False, 
        index=True,
        comment="مؤشر حالة الحذف الناعم للسجل"
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True,
        comment="وقت أرشفة السجل اللوجستي"
    )

