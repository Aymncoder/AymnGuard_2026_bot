# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base

# استخدام SQLite للمرحلة الحالية، وسهولة التحويل لـ PostgreSQL لاحقاً
DATABASE_URL = "sqlite:///./sovereign_empire.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # بناء الجداول تلقائياً عند أول تشغيل
    Base.metadata.create_all(bind=engine)
