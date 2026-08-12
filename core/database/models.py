# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Sovereign Database Models (Cloud ORM)
==============================================================================
تعريف جداول المستخدمين، المجموعات، وإشارات السوق باستخدام SQLAlchemy ORM.
تم تصحيح الأخطاء النحوية وتحسين أنواع البيانات لتتوافق مع بيئة السيرفرات السحابية.
==============================================================================
"""

from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Float, DateTime
from sqlalchemy.sql import func
from .engine import Base

# ==============================================================================
# 1. قطاع أمن المجتمعات (User Model)
# ==============================================================================
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, nullable=True)
    reputation_score = Column(Integer, default=100)  # رصيد السمعة، ينقص مع المخالفات
    is_blacklisted = Column(Boolean, default=False)
    # تصحيح الخطأ النحوي: استبدال علامة الناقص (-) بعلامة المساواة (=)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# 2. قطاع إدارة المجموعات (Group Model)
# ==============================================================================
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(BigInteger, unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    security_level = Column(String(50), default='strict')  # low, medium, strict
    # تصحيح الخطأ النحوي: استبدال علامة الناقص (-) بعلامة المساواة (=)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==============================================================================
# 3. قطاع ذكاء الأسواق (Market Signal Model)
# ==============================================================================
class MarketSignal(Base):
    __tablename__ = 'market_signals'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), index=True, nullable=False)  # مثل BTCUSDT
    rsi_value = Column(Float, nullable=True)
    ema_value = Column(Float, nullable=True)
    signal_type = Column(String(50), nullable=False)  # BUY, SELL, HOLD
    # تصحيح الخطأ النحوي: استبدال علامة الناقص (-) بعلامة المساواة (=)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
