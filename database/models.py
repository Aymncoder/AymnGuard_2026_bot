# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Database Models & Schema Definitions
تعريف الجداول والنماذج الأساسية لقاعدة البيانات السيادية (SQLAlchemy DeclarativeBase).
"""

import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean

class Base(DeclarativeBase):
    """
    الفئة الأساسية (Declarative Base) الموحدة لجميع جداول ونماذج الإمبراطورية.
    """
    pass

class SovereignUser(Base):
    """
    جدول مستخدمي النظام السيادي عبر تيليجرام.
    """
    __tablename__ = "sovereign_users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class SovereignAuditLog(Base):
    """
    جدول سجلات الأمان والعمليات السيادية لتدقيق العمليات.
    """
    __tablename__ = "sovereign_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True, nullable=False)
    action = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
