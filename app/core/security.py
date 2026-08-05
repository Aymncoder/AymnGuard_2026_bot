# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Security & Cryptography Core
نواة الأمان السيادي - تشفير البيانات، إدارة الهوية، وإصدار التصاريح (JWT)
=============================================================================
"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from passlib.context import CryptContext
from jose import jwt, JWTError

# استدعاء مركز الإعدادات الذي بنيناه مسبقاً
from .config import settings

# تهيئة محرك التشفير (Bcrypt) - المعيار الذهبي في تشفير كلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================================================================
# 1. هندسة تشفير كلمات المرور (Password Hashing)
# =========================================================================

def get_password_hash(password: str) -> str:
    """
    تشفير كلمة المرور في اتجاه واحد (One-way Hash).
    حتى لو تم اختراق قاعدة البيانات، ستكون كلمات المرور عبارة عن طلاسم غير قابلة للقراءة.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    مقارنة كلمة المرور المدخلة مع النسخة المشفرة في قاعدة البيانات بأمان.
    """
    return pwd_context.verify(plain_password, hashed_password)

# =========================================================================
# 2. هندسة التوكن والمصادقة (JWT Tokens Generation)
# =========================================================================

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    إصدار تصريح دخول (Token) مشفر ومؤقت.
    subject: عادة يكون مُعرف المستخدم (User ID) أو اسمه.
    expires_delta: فترة صلاحية التصريح قبل أن يتم تدميره تلقائياً.
    """
    # تحديد وقت انتهاء الصلاحية
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # استخدام القيمة الافتراضية من مدير الإعدادات (أسبوع واحد)
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # بناء هيكل البيانات الذي سيتم تشفيره (Payload)
    # نستخدم 'exp' للوقت، و 'sub' للهوية (معايير JWT العالمية)
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # استخراج المفتاح السري بأمان من كائن SecretStr
    secret = settings.SECRET_KEY.get_secret_value()
    
    # توقيع التوكن وإصداره
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)
    
    return encoded_jwt
