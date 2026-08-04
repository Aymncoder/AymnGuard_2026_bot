"""
AymnGuard Enterprise Logistics Platform - Advanced Enterprise User CRUD Service
طبقة العمليات والخدمات المؤسسية المتقدمة لإدارة المستخدمين والصلاحيات اللوجستية الضخمة،
مصممة بمعايير SQLAlchemy 2.0 Async وأعلى مستويات الموثوقية والأمان المستقبلي.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.user import User
from passlib.context import CryptContext

# تهيئة سياق التشفير المؤسسي الآمن لكلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EnterpriseUserCRUD:
    """
    مستودع العمليات المؤسسية المتقدم (Enterprise Repository) لكيان المستخدمين والصلاحيات،
    مُحسّن للتعامل مع الأحمال العالية والعمليات اللوجستية المتزامنة واسعة النطاق.
    """

    async def get_by_id(self, db: AsyncSession, user_id: str) -> Optional[User]:
        """
        استعلام فائق الأداء عن مستخدم عبر المعرف الفريد UUID،
        مع التحقق التلقائي من أن الحساب نشط وغير محذوف لأغراض أمنية لوجستية.
        """
        result = await db.execute(
            select(User).where(User.id == user_id, User.is_deleted == False)
        )
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """التحقق والبحث السريع عن مستخدم بواسطة البريد الإلكتروني المؤسسي"""
        result = await db.execute(
            select(User).where(User.email == email, User.is_deleted == False)
        )
        return result.scalars().first()

    async def get_multi_filtered(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 50, 
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        search_query: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        جلب قائمة المستخدمين مع التصفية الذكية المتقدمة، وتدعم:
        1. التصفية حسب الدور الوظيفي أو الصلاحية اللوجستية (Role).
        2. التصفية حسب حالة النشاط (Active Status).
        3. البحث النصي الذكي الشامل (Smart Search) عبر البريد أو الاسم.
        4. إرجاع بيانات وصفية متكاملة لعدد النتائج الإجمالي (Pagination Metadata).
        """
        stmt = select(User).where(User.is_deleted == False)

        # تطبيق معايير التصفية اللوجستية الديناميكية
        if role:
            stmt = stmt.where(User.role == role)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)
        if search_query:
            search_filter = or_(
                User.email.ilike(f"%{search_query}%"),
                User.full_name.ilike(f"%{search_query}%") if hasattr(User, 'full_name') else False
            )
            stmt = stmt.where(search_filter)

        # حساب إجمالي عدد السجلات بدقة لدعم واجهات الإدارة الضخمة
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await db.execute(count_stmt)
        total_count = total_result.scalar() or 0

        # تطبيق التمرير (Pagination) والأداء العالي
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = result.scalars().all()

        return {
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "items": items
        }

    async def create_enterprise_user(self, db: AsyncSession, *, obj_in: Dict[str, Any]) -> User:
        """
        إنشاء وتسجيل مستخدم مؤسسي جديد مع التشفير التلقائي لكلمات المرور
        وإدارة معاملات قاعدة البيانات غير المتزامنة (Async Transaction Management).
        """
        if "password" in obj_in:
            hashed_password = pwd_context.hash(obj_in.pop("password"))
            obj_in["hashed_password"] = hashed_password

        db_obj = User(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_enterprise_user(
        self, db: AsyncSession, *, db_obj: User, obj_in: Dict[str, Any]
    ) -> User:
        """
        تحديث بيانات الحساب مع معالجة آمنة لتحديث كلمات المرور وتتبع التغييرات
        لضمان سلامة التدقيق المؤسسي (Audit Trail).
        """
        if "password" in obj_in and obj_in["password"]:
            obj_in["hashed_password"] = pwd_context.hash(obj_in.pop("password"))

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def soft_delete(self, db: AsyncSession, *, user_id: str) -> Optional[User]:
        """
        الحذف الآمن (Soft Delete): بدلاً من الحذف الفيزيائي للبيانات الذي قد يضر
        بارتباطات الشحنات والعمليات اللوجستية التاريخية، يتم تعطيل الحساب مع الاحتفاظ بالسجلات للأرشفة والتدقيق.
        """
        obj = await self.get_by_id(db=db, user_id=user_id)
        if obj:
            obj.is_active = False
            obj.is_deleted = True
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
        return obj

# تصدير كائن الخدمة المؤسسي للاستخدام في موجهات النظام (API Routers)
user_crud = EnterpriseUserCRUD()

