# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Sovereign Database Models (ORM)
==============================================================================
مخطط الهياكل والجداول المركزية لإمبراطورية AymnGuard:
تعريف جداول المستخدمين، التراخيص، البوتات الديناميكية، وسجلات التدقيق الأمني.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ==============================================================================
# 1. جدول المستخدمين (Sovereign Users)
# ==============================================================================
class SovereignUser(Base):
    __tablename__ = 'sovereign_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, default="subscriber")  # owner, admin, subscriber
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # علاقة ربط مع التراخيص
    licenses = relationship("LicenseKey", back_populates="owner", cascade="all, delete-orphan")


# ==============================================================================
# 2. جدول التراخيص (License Keys)
# ==============================================================================
class LicenseKey(Base):
    __tablename__ = 'license_keys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False, index=True)  # المفتاح السيادي
    tier = Column(String, default="Premium")  # Premium, Enterprise
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
    name = Column(String, nullable=False)  # مثل: "التداول الذكي"
    module_type = Column(String, nullable=False)  # مثال: "transfer_bot"
    config = Column(JSON, default={})  # حفظ الإعدادات بصيغة JSON (التوسع المستقل)
    is_enabled = Column(Boolean, default=False)
    last_run = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# ==============================================================================
# 4. جدول السجلات (التدقيق الأمني والتشغيل)
# ==============================================================================
class SystemLog(Base):
    __tablename__ = 'system_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String, nullable=False)
    status = Column(String, default="Success")  # Success, Failed, Alert
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    details = Column(String, nullable=True)
