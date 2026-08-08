# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# --- جدول المستخدمين ---
class SovereignUser(Base):
    __tablename__ = 'sovereign_users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, default="subscriber") # owner, admin, subscriber
    is_active = Column(Boolean, default=True)

# --- جدول التراخيص (نظام الاشتراكات) ---
class LicenseKey(Base):
    __tablename__ = 'license_keys'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False) # المفتاح المشفر
    tier = Column(String) # Premium, Enterprise
    expiry_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_used = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('sovereign_users.id'))

# --- جدول البوتات والميكروسيرفسات (الديناميكي) ---
class BotInstance(Base):
    __tablename__ = 'bot_instances'
    id = Column(Integer, primary_key=True)
    name = Column(String) # مثال: "النقل الذكي"
    module_type = Column(String) # مثال: "transfer_bot"
    config = Column(JSON) # حفظ الإعدادات بصيغة JSON المرنة (للتوسيع المستقبلي)
    is_enabled = Column(Boolean, default=False)
    last_run = Column(DateTime, default=datetime.datetime.utcnow)

# --- جدول السجلات (للتحقيق الأمني والتحليل) ---
class SystemLog(Base):
    __tablename__ = 'system_logs'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    status = Column(String) # Success, Failed, Alert
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String)
