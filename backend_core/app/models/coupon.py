# models.py (إضافات الجداول الأخيرة)
from sqlalchemy import String, Integer, DateTime, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base  # افتراض أن Base معرفة في ملف database.py

class CouponModel(Base):
    __tablename__ = "smart_coupons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    discount_value: Mapped[float] = mapped_column(Float, default=0.0)
    target_service: Mapped[str] = mapped_column(String(50), default="all")
    max_uses: Mapped[int] = mapped_column(Integer, default=1)
    current_uses: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PaymentTransactionModel(Base):
    __tablename__ = "payment_transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tx_id: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    chat_id: Mapped[str] = mapped_column(String(50), index=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(20), default="USDT")
    target_service: Mapped[str] = mapped_column(String(50), default="tool")
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
