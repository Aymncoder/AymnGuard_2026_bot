# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Authentication & User Management Hub
محرك المصادقة، التسجيل، وإصدار التصاريح الأمنية (JWT & Users Core)
=============================================================================
"""

import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

# 🛡️ تصحيح المسارات المعمارية لتوحيد الجذور داخل backend_core
from backend_core.db.session import get_db_session
from backend_core.models.user import User
from backend_core.schemas.user_schema import UserCreateSchema, UserResponseSchema, UserListResponseSchema
from backend_core.core.security import verify_password, get_password_hash, create_access_token
from backend_core.core.config import settings
from backend_core.crud.user import user_crud

router = APIRouter(prefix="/auth", tags=["Sovereign Authentication & Users"])
logger = logging.getLogger("AymnGuardAuthEngine")

@router.post(
    "/register", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="تسجيل مستخدم سيادي جديد في المنصة"
)
async def register_user(
    user_data: UserCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    تسجيل مستخدم جديد مع التحقق الاستباقي وتشفير بيانات الاعتماد بمعايير الأمان المؤسسي.
    """
    try:
        query = select(User).where(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
        result = await db.execute(query)
        existing_user = result.scalars().first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="تحذير أمني: اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً في النظام."
            )

        # تطبيق التشفير السيادي الآمن
        secured_password = get_password_hash(user_data.password)

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            role=user_data.role,
            is_active=user_data.is_active,
            is_verified=user_data.is_verified,
            hashed_password=secured_password
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"✨ [Auth Engine]: تم تسجيل الكيان السيادي بنجاح: {new_user.username} (ID: {new_user.id})")
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.critical(f"❌ [Auth Engine Error]: فشل تسجيل المستخدم - التفاصيل: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطأ داخلي حرج أثناء معالجة التسجيل السيادي. تم التراجع عن العملية."
        )


@router.post("/login", summary="إصدار التوكن السيادي (تسجيل الدخول)")
async def login_access_token(
    db: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """
    التحقق من بيانات الاعتماد وإصدار مفتاح وصول مؤقت (JWT Access Token).
    """
    user = await user_crud.get_by_username(db, username=form_data.username)
    if not user:
        user = await user_crud.get_by_email(db, email=form_data.username)
        
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة."
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذا الكيان السيادي معطل ولا يملك صلاحية الوصول."
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "status": "Authorized",
        "sovereign_node": settings.PROJECT_NAME
    }


@router.get(
    "/users", 
    response_model=UserListResponseSchema, 
    summary="استعراض قائمة المستخدمين والكيانات النشطة"
)
async def list_users(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db_session)
):
    """
    استرجاع قائمة المستخدمين مع تقسيم الصفحات (Pagination) وحماية الذاكرة.
    """
    try:
        offset = (page - 1) * page_size
        query = select(User).offset(offset).limit(page_size)
        result = await db.execute(query)
        users = result.scalars().all()
        
        count_query = select(func.count()).select_from(User)
        total_count = await db.scalar(count_query)

        return {
            "status": "success",
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "users": users
        }
    except Exception as e:
        logger.error(f"❌ [Database Read Error]: خطأ في جلب قائمة الكيانات - التفاصيل: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="فشل استرداد البيانات من النواة المركزية."
        )
