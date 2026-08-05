# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Security Dependencies
حارس البوابة ونقاط التفتيش المركزية - التحقق من الـ JWT وتأمين مسارات API
=============================================================================
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

# استيراد إعدادات النواة وقاعدة البيانات
from backend_core.core.config import settings
from backend_core.db.session import get_db_session  # صمام الأمان المعزول للبيانات
from backend_core.models.user import User
from backend_core.crud.user import user_crud

# تحديد مسار جلب التوكن (OAuth2)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login" # مسار تسجيل الدخول الذي سنقوم ببنائه لاحقاً
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    نقطة تفتيش سيادية: تقوم بفك تشفير الـ JWT، التحقق من الهوية،
    والتأكد من أن الكيان موجود ومفعل داخل قاعدة البيانات.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="فشل التحقق من بيانات المصادقة أو انتهاء صلاحية التصريح.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # استخراج المفتاح السري وخوارزمية التشفير من الإعدادات المركزية
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(
            token, secret_key, algorithms=[settings.ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # البحث عن المستخدم في قاعدة البيانات عبر طبقة الـ CRUD المعزولة
    user = await user_crud.get_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
        
    # التحقق الاستباقي: هل المستخدم محظور أو غير مفعل؟
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عفواً، هذا الكيان السيادي معطل أو موقوف عن العمل."
        )
        
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    نقطة تفتيش عليا: تضمن أن المستخدم الحالي ليس فقط مسجلاً، 
    بل يمتلك صلاحيات (Superuser / Admin) لتنفيذ العمليات الخطرة والحرجة.
    """
    if getattr(current_user, "role", "user") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="صلاحيات غير كافية. هذا الإجراء مخصص للمديرين السياديين فقط."
        )
    return current_user
