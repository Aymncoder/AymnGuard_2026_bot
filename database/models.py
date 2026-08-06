# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v11.0.0 : Ultimate Sovereign Database Models Master
==============================================================================
النسخة الماسية المدمجة والنهائية لكافة نماذج وجداول قاعدة البيانات المؤسسية:
1. TelegramLogModel: توثيق رسائل وأحداث تيليجرام الواردة.
2. UserAuthModel: إدارة اشتراكات المستخدمين وصلاحيات الـ VIP.
3. SovereignUser: إدارة المستخدمين السياديين، الصلاحيات والأدوار (Operator, Admin, Sovereign).
4. TradingTransaction: بوابات وتداولات السوق والأصول الرقمية والمالية.
5. SovereignAuditLog / SecurityAuditLog: سجلات الأمان، تدقيق العمليات والعقود الذكية غير القابلة للتلاعب.
"""

from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, Float, Boolean

# تعريف الفئة الأساسية الموحدة لجميع نماذج المنظومة السيادية
Base = declarative_base()

class TelegramLogModel(Base):
    """جدول تسجيل وتوثيق رسائل وأحداث تيليجرام الواردة والأزرار التفاعلية."""
    __tablename__ = "telegram_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    update_id: Mapped[int] = mapped_column(Integer, index=True)
    chat_id: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), default="message")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class UserAuthModel(Base):
    """جدول إدارة الاشتراكات وصلاحيات المستخدمين السيادية وتفعيل الـ VIP."""
    __tablename__ = "user_subscriptions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    is_vip: Mapped[int] = mapped_column(Integer, default=0)
    subscription_type: Mapped[str] = mapped_column(String(50), default="Standard")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SovereignUser(Base):
    """جدول مستخدمي النظام السيادي عبر تيليجرام وإدارة الصلاحيات والأدوار الإمبريالية."""
    __tablename__ = "sovereign_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="operator")  # operator, admin, sovereign
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TradingTransaction(Base):
    """جدول بوابات التداول والعمليات المالية الرقمية والتحليل الفني والصفقات."""
    __tablename__ = "trading_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True, nullable=False)  # مثل BTCUSDT
    side: Mapped[str] = mapped_column(String(10), nullable=False)  # buy, sell
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    execution_price: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")  # success, failed, pending
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SovereignAuditLog(Base):
    """سجلات التدقيق الأمني والعقود والعمليات السيادية غير القابلة للتلاعب (Immutable Audit Trails)."""
    __tablename__ = "sovereign_audit_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    action: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SecurityAuditLog(Base):
    """جدول سجلات الأمان المتقدمة، فحص الثغرات وتقييم مخاطر العقود والعمليات."""
    __tablename__ = "security_audit_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    target_contract: Mapped[str] = mapped_column(String(255), nullable=False)
    audit_result: Mapped[str] = mapped_column(Text, nullable=True)
    risk_score: Mapped[str] = mapped_column(String(20), default="SAFE")  # SAFE, WARNING, CRITICAL
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
