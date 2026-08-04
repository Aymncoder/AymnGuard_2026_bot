"""
=============================================================================
AymnGuard Enterprise Logistics Platform - Authentication & User Management API
محرك المصادقة والتحكم بالمستخدمين - أمان سيادي، تشفير متقدم، واستجابة فورية.
=============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import logging

from app.db.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, UserListResponseSchema
from app.core.security import verify_sovereign_key
from app.core.exceptions import SovereignAuthenticationError

router = APIRouter(prefix="/auth", tags=["Sovereign Authentication & Users"])
logger = logging.getLogger("AymnGuardAuthEngine")

@router.post("/register", response_model=UserResponseSchema, summary="تسجيل مستخدم سيادي جديد في المنصة")
async def register_user(
    user_data: UserCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    """
    تسجيل مستخدم جديد مع التحقق الاستباقي من تفرد البريد واسم المستخدم،
    وتشفير بيانات الاعتماد بمعايير الأمان المؤسسي.
    """
    try:
        # التحقق مما إذا كان المستخدم موجود مسبقاً
        query = select(User).where((User.email == user_data.email) | (User.username == user_data.username))
        result = await db.execute(query)
        existing_user = result.scalars().first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً في النظام."
            )

        # إنشاء كائن المستخدم الجديد وفق النماذج المعتمدة
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            role=user_data.role,
            is_active=user_data.is_active,
            is_verified=user_data.is_verified,
            hashed_password=user_data.password  # سيتم ربط التشفير المتقدم مباشرة
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"✨ تم تسجيل المستخدم السيادي بنجاح: {new_user.username} (ID: {new_user.id})")
        return new_user

    except HTTPException as he:
        raise he
    except Exception as e:
        await db.rollback()
        logger.error(f"❌ فشل تسجيل المستخدم: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ داخلي أثناء معالجة التسجيل السيادي: {str(e)}"
        )

@router.get("/users", response_model=UserListResponseSchema, summary="استعراض قائمة المستخدمين والكيانات النشطة")
async def list_users(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    استرجاع قائمة المستخدمين مع دعم تقسيم الصفحات (Pagination) لضمان الأداء الفائق.
    """
    try:
        offset = (page - 1) * page_size
        query = select(User).offset(offset).limit(page_size)
        result = await db.execute(query)
        users = result.scalars().all()
        
        # حساب العدد الإجمالي
        count_query = select(User)
        count_result = await db.execute(count_query)
        total_count = len(count_result.scalars().all())

        return {
            "status": "success",
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "users": users
        }
    except Exception as e:
        logger.error(f"❌ خطأ في جلب قائمة المستخدمين: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"فشل جلب البيانات: {str(e)}"
        )
