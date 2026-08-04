"""
AymnGuard Enterprise Logistics Platform - Unified Base Model & Global Registry
هذا الملف يدمج القاعدة الأساسية المعمارية (Declarative Base) مع الحقول المشتركة العالمية
(مثل المعرف الفريد UUID وأختام التدقيق الزمني) والمحور المركزي لتجميع النماذج اللوجستية.
"""

import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import Uuid

class Base(AsyncAttrs, DeclarativeBase):
    """
    النموذج الجذري المؤسسي لجميع كيانات المنصة اللوجستية.
    يوفر تلقائياً معرفاً فريداً عالمياً (UUIDv4) وأزمنة التدقيق والمتابعة الدقيقة لكل جدول في النظام.
    """
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        index=True,
        nullable=False,
        comment="المعرف الفريد العالمي للكيان اللوجستي والمؤسسي"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
        comment="ختم الوقت لإنشاء السجل في النظام"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False,
        comment="ختم الوقت لآخر تحديث على السجل اللوجستي"
    )

# 1. استيراد نموذج المستخدمين وإدارة الصلاحيات (RBAC & Auth) لضمان تسجيله تحت القاعدة المركزية
from app.models.user import User

# 2. مساحات حجز النماذج اللوجستية المستقبلية (الأساطيل، المستودعات، والشحنات الضخمة)
# from app.models.fleet import FleetVehicle, Driver, VehicleTelemetry
# from app.models.warehouse import Warehouse, InventoryItem
# from app.models.shipment import Shipment, Waybill

# تصدير الكيانات المؤسسية لضمان قراءتها والاكتشاف التلقائي بواسطة Alembic
__all__ = [
    "Base",
    "User",
    # سيتم تفعيل النماذج اللوجستية تباعاً:
    # "FleetVehicle",
    # "Driver",
    # "Warehouse",
    # "InventoryItem",
    # "Shipment",
]

