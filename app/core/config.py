# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Configuration Manager
مركز الإعدادات السيادي - كبسلة وتأمين متغيرات البيئة والمصادقة
=============================================================================
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, AnyHttpUrl

class Settings(BaseSettings):
    # 1. إعدادات المنصة الأساسية (Core Platform Settings)
    PROJECT_NAME: str = "AymnGuard Enterprise"
    VERSION: str = "5.0.0"
    ENVIRONMENT: str = "development" # يمكن أن تكون production
    DEBUG_MODE: bool = False
    
    # 2. إعدادات قواعد البيانات (Database & Storage)
    # نستخدم بروتوكولات قوية لضمان الاتصال
    POSTGRES_URI: Optional[str] = None
    REDIS_URI: Optional[str] = None
    
    # 3. إعدادات التشفير والهوية (Security & Cryptography)
    SECRET_KEY: SecretStr  # يتم استخدام SecretStr لمنع طباعة المفتاح في السجلات بالخطأ
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # أسبوع افتراضياً
    
    # 4. إعدادات الاتصال واللوجستيات (Telegram & Telemetry)
    TELEGRAM_BOT_TOKEN: Optional[SecretStr] = None
    TELEGRAM_API_ID: Optional[int] = None
    TELEGRAM_API_HASH: Optional[SecretStr] = None
    WEBHOOK_URL: Optional[AnyHttpUrl] = None

    # تهيئة الـ Pydantic لقراءة المتغيرات من ملف .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # تجاهل أي متغيرات في البيئة لا تهمنا
    )

# كائن مركزي يتم استدعاؤه في كل النظام
# بمجرد استدعائه، سيقوم بالتحقق من وجود المفاتيح الحساسة
settings = Settings()
