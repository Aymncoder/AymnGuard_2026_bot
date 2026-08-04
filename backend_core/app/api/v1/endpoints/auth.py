# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise Logistics Platform - Authentication & User Management API
محرك المصادقة والتحكم بالمستخدمين - أمان سيادي، تشفير متقدم، واستجابة فورية.
=============================================================================
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func # تم الإضافة لحساب العدد بكفاءة عالية

# 🛡️ تصحيح التداخل: استخدام صمام الأمان المعزول الذي قمنا ببنائه مسبقاً
from app.api.dependencies.db_deps import get_db_session
from app.models.user import User
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema, UserListResponseSchema

# استيراد أدوات التشفير السيادي (يجب التأكد من وجود get_password_hash)
from app.core.security import verify_sovereign_key, get_password_hash 
from app.core.exceptions import SovereignAuthenticationError

router = APIRouter(prefix="/auth", tags=["Sovereign Authentication & Users"])
logger = logging.getLogger("AymnGuardAuthEngine")

@router.post(
    "/register", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED, # تعديل مؤسسي: الاستجابة الدقيقة للإنشاء
    summary="تسجيل مستخدم سيادي جديد في المنصة"
)
async def register_user(
    user_data: UserCreateSchema,
    db: AsyncSession = Depends(get_db_session) # تم ربط الاعتمادية المعزولة
):
    """
    تسجيل مستخدم جديد مع التحقق الاستباقي من تفرد البريد واسم المستخدم،
    وتشفير بيانات الاعتماد بمعايير الأمان المؤسسي الصارمة.
    """
    try:
        # التحقق الاستباقي (يمكن نقله لاحقاً إلى crud/user.py لضمان نظافة المعمارية)
        query = select(User).where(
            (User.email == user_data.email) | (User.username == user_data.username)
        )
        result = await db.execute(query)
        existing_user = result.scalars().first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, # تعديل مؤسسي: 409 أفضل من 400 للتضارب
                detail="تحذير أمني: اسم المستخدم أو البريد الإلكتروني مسجل مسبقاً في النظام."
            )

        # 🔒 تطبيق التشفير السيادي الحقيقي قبل الحفظ
        secured_password = get_password_hash(user_data.password)

        # إنشاء كائن المستخدم الجديد
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            role=user_data.role,
            is_active=user_data.is_active,
            is_verified=user_data.is_verified,
            hashed_password=secured_password # تم ربط التشفير بنجاح
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"✨ [Auth Engine]: تم تسجيل الكيان السيادي بنجاح: {new_user.username} (ID: {new_user.id})")
        return new_user

    except HTTPException:
        # إعادة رفع استثناءات HTTP المبرمجة مسبقاً دون تغيير
        raise
    except Exception as e:
        await db.rollback() # تراجع فوري عن أي تلوث في البيانات
        logger.critical(f"❌ [Auth Engine Error]: فشل تسجيل المستخدم - التفاصيل: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="خطأ داخلي حرج أثناء معالجة التسجيل السيادي. تم التراجع عن العملية لتأمين النظام."
        )

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
    استرجاع قائمة المستخدمين مع تقسيم الصفحات (Pagination).
    تمت هندسة هذا المسار لتجنب استنزاف الذاكرة (Memory Leaks) في قواعد البيانات الضخمة.
    """
    try:
        # حساب إزاحة البيانات
        offset = (page - 1) * page_size
        
        # 1. جلب البيانات المطلوبة فقط (Zero-Waste Query)
        query = select(User).offset(offset).limit(page_size)
        result = await db.execute(query)
        users = result.scalars().all()
        
        # 2. ⚡ التعديل الجوهري: حساب العدد الإجمالي عبر قاعدة البيانات مباشرة وليس الذاكرة
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
            detail="فشل استرداد البيانات من النواة المركزية. جارٍ التدقيق."
        )
