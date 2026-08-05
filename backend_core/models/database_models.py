# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Database Models & Subscriptions
نماذج قاعدة البيانات لحفظ بيانات المشتركين، الباقات، وحالة التراخيص
=============================================================================
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserModel(Base):
    """
    جدول المشتركين والمستخدمين في النظام السيادي.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    is_vip = Column(Boolean, default=False)
    subscription_tier = Column(String, default="free") # free, bot_only, transfer_tool, vip_all
    subscription_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TransactionModel(Base):
    """
    جدول تتبع المدفوعات، الكوبونات، والمعاملات المالية.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    service_type = Column(String, nullable=False)
    coupon_used = Column(String, nullable=True)
    status = Column(String, default="completed") # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
