from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Float, DateTime
from sqlalchemy.sql import func
from .engine import Base

# --- قطاع أمن المجتمعات ---

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    reputation_score = Column(Integer, default=100) # رصيد السمعة، ينقص مع المخالفات
    is_blacklisted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(BigInteger, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    security_level = Column(String, default="strict") # مستويات: low, medium, strict
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- قطاع ذكاء الأسواق ---

class MarketSignal(Base):
    __tablename__ = 'market_signals'
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False) # مثل BTCUSDT
    rsi_value = Column(Float, nullable=True)
    ema_value = Column(Float, nullable=True)
    signal_type = Column(String, nullable=False) # BUY, SELL, HOLD
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
