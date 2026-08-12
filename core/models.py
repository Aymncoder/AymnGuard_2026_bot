# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.1.0 : Sovereign Database Models (Cloud ORM)
==============================================================================
مخطط الهياكل والجداول المركزية لإمبراطورية AymnGuard:
تعريف جداول المستخدمين، التراخيص، البوتات الديناميكية، وسجلات التدقيق الأمني.
تم تحسين أنواع البيانات (BigInteger) وتوحيد التسميات لبيئة السحابة المدفوعة.
==============================================================================
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ==============================================================================
# 1. جدول المستخدمين (Sovereign Users)
# ==============================================================================
class SovereignUser(Base):
    __tablename__ = 'sovereign_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # استخدام BigInteger ضروري جداً لمعرفات تليجرام لمنع الانهيار
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=True, index=True)
    role = Column(String(50), default="subscriber")  # owner, admin, subscriber
    is_active = Column(Boolean, default=True)
    # الاعتماد على توقيت السيرفر السحابي لضمان الدقة
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # علاقة ربط مع التراخيص
    licenses = relationship("LicenseKey", back_populates="owner", cascade="all, delete-orphan")


# ==============================================================================
# 2. جدول التراخيص (License Keys)
# ==============================================================================
class LicenseKey(Base):
    __tablename__ = 'license_keys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    tier = Column(String(50), default="Premium")  # Premium, Enterprise
    expiry_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_used = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('sovereign_users.id'), nullable=True)

    # علاقة عكسية مع جدول المستخدمين
    owner = relationship("SovereignUser", back_populates="licenses")


# ==============================================================================
# 3. جدول البوتات والميكروسيرفسات الديناميكية (Bot Instances)
# ==============================================================================
class BotInstance(Base):
    __tablename__ = 'bot_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    module_type = Column(String(100), nullable=False)
    config = Column(JSON, default={})
    is_enabled = Column(Boolean, default=False)
    last_run = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ==============================================================================
# 4. جدول سجلات التدقيق الأمني (Sovereign Audit Logs)
# ==============================================================================
class SovereignAuditLog(Base):
    __tablename__ = 'sovereign_audit_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=True, index=True)
    action = Column(String(255), nullable=False)
    status = Column(String(50), default="Success")  # Success, Failed, Alert
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(String, nullable=True)
