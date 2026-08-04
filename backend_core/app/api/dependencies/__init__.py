# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - API Dependencies & Security Engine
==============================================================================
مزوّدات التبعية المركزية (FastAPI Dependencies) للمصادقة السيادية،
التحقق من صلاحيات الوصول، وحقن جلسات قواعد البيانات لجميع مسارات الـ API.
"""

import os
import logging
from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

# استيراد مزوّد قاعدة البيانات غير المتزامن
from app.db.database import get_db

logger = logging.getLogger("AegisAICore.ApiDependencies")

# مفتاح التشفير السيادي وإعدادات التوثيق
SECRET_KEY = os.getenv("SECRET_KEY", "AymnGuard_Sovereign_Enterprise_Secret_Key_2026")
ALGORITHM = "HS256"

# مخطط المصادقة عبر ترويسة Bearer Token
security_scheme = HTTPBearer(auto_error=True)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    التحقق من صحة رمز المصادقة (JWT Token) واستخراج بيانات المستخدم السيادية
    مع معالجة استباقية لمحاولات التلاعب أو انتهاء الصلاحية.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="فشل المصادقة السيادية: رمز الدخول غير صالح أو منتهي الصلاحية.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if not user_id:
            logger.warning("⚠️ [Security Warning]: محاولة مصادقة برمز خاوٍ من معرف المستخدم (sub).")
            raise credentials_exception
            
    except JWTError as e:
        logger.error(f"❌ [JWT Decryption Error]: فشل فك تشفير الرمز: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.critical(f"❌ [Auth Critical Error]: خطأ غير متوقع أثناء التحقق من الهوية: {str(e)}")
        raise credentials_exception

    # إرجاع بيانات الجلسة والمستخدم الموثقة
    return {
        "user_id": user_id,
        "session_payload": payload
    }


async def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    التحقق من أن المستخدم الحالي يملك صلاحيات المشرف أو المالك السيادي (Sovereign Owner/Admin)
    لمنع أي وصول غير مصرح به للمسارات الحساسة واللوجستية الكبرى.
    """
    payload = current_user.get("session_payload", {})
    roles = payload.get("roles", [])
    
    # التحقق من الرتبة السيادية
    if "admin" not in roles and "sovereign" not in roles:
        logger.warning(f"🚨 [Security Breach Attempt]: محاولة وصول إداري غير مصرح بها من المستخدم: {current_user.get('user_id')}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="صلاحيات مرفوضة: هذا المسار مخصص للمالك السيادي والمشرفين فقط."
        )
        
    return current_user
