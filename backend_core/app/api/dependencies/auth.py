# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise - Authentication Dependencies & Security Guards (Cloud)
==============================================================================
حواضن ومحددات المصادقة والتحقق من الهوية عبر JWT للبيئة السحابية.
تم تطهيره بالكامل من الرموز التعبيرية وتأمين معالجة الأخطاء.
==============================================================================
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from backend_core.core.config import settings
from backend_core.db.session import get_db_session
from backend_core.models.user import User
from backend_core.crud.user import user_crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    التحقق من الهوية بنقطة التفتيش السحابية: فك تشفير التوكن والتأكد من وجود الكيان داخل قاعدة البيانات.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="فشل التحقق من بيانات المصادقة أو انقطاع صلاحية التوكن.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # معالجة آمنة لسر المفتاح سواء كان SecretStr أو String عادي
        secret_key = settings.SECRET_KEY
        if hasattr(secret_key, "get_secret_value"):
            secret_key = secret_key.get_secret_value()

        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # التأكد من صحة تحويل معرف المستخدم إلى رقم صحيح دون انهيار
        try:
            parsed_user_id = int(user_id)
        except (ValueError, TypeError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # البحث عن المستخدم عبر الـ CRUD المعتمد
    user = await user_crud.get_by_id(db, user_id=parsed_user_id)
    if user is None:
        raise credentials_exception

    # التحقق الاستباقي من حالة الكيان وحظره إدارياً
    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="عذراً، هذا الكيان محظر أو موقوف إدارياً."
        )

    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    لتأمين العمليات والمسارات الحرجة (Superuser Guard) للبيئة السحابية والمالك السيادي.
    """
    user_role = getattr(current_user, "role", "subscriber")
    if user_role not in ["admin", "owner", "sovereign_owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="صلاحيات سيادية غير كافية لتنفيذ هذا الإجراء."
        )
    return current_user
