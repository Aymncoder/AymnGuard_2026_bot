# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Authentication Dependencies & Security Guards
حواضن ومحددات المصادقة والتحقق من الهوية (Security Dependencies)
=============================================================================
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

# استيراد إعدادات النواة وقاعدة البيانات ضمن نطاق backend_core الموحد
from backend_core.core.config import settings
from backend_core.db.session import get_db_session
from backend_core.models.user import User
from backend_core.crud.user import user_crud

# نقطة النهاية المخصصة لجلب التوكن عبر مسار المصادقة المركزي
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    نقطة تفتيش سيادية: فك تشفير الـ JWT، التحقق من الهوية،
    والتأكد من أن الكيان موجود ومفعل داخل قاعدة البيانات.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="فشل التحقق من بيانات المصادقة أو انقضاء صلاحية التوكن.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        secret_key = settings.SECRET_KEY.get_secret_value()
        payload = jwt.decode(
            token, secret_key, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # البحث عن المستخدم عبر طبقة الـ CRUD المعزولة
    user = await user_crud.get_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
        
    # التحقق الاستباقي من حالة الكيان
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عفواً، هذا الكيان السيادي معطل أو موقوف إدارياً."
        )
        
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    حارس الصلاحيات العليا (Superuser Guard) لتأمين العمليات والمسارات الحرجة.
    """
    if getattr(current_user, "role", "user") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="صلاحيات سيادية غير كافية لتنفيذ هذا الإجراء."
        )
    return current_user
