"""
AymnGuard Enterprise Logistics Platform - Advanced Enterprise User API Endpoints
موجهات وواجهات برمجة التطبيقات المتقدمة لإدارة المستخدمين، الكوادر، والصلاحيات اللوجستية الضخمة.
مصممة بأعلى معايير الأمان، التحقق الصارم (Pydantic v2)، والأداء الفائق غير المتزامن.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field

from app.db.database import get_db
from app.crud.user import user_crud

router = APIRouter(prefix="/users", tags=["Enterprise Users & Logistics Management"])

# ==========================================
# نماذج التحقق وهياكل البيانات (Pydantic Schemas)
# ==========================================

class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="البريد الإلكتروني المؤسسي المعتمد")
    full_name: str = Field(..., min_length=2, max_length=100, description="الاسم الكامل للمستخدم أو الموظف اللوجستي")
    password: str = Field(..., min_length=8, description="كلمة المرور الآمنة (يُفضل أن تحتوي على رموز وأرقام)")
    role: str = Field(default="logistics_operator", description="الدور الوظيفي داخل المنظومة اللوجستية")
    phone_number: Optional[str] = Field(None, description="رقم الهاتف للتواصل الميداني والعمليات")

class UserResponseSchema(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True

class EnterpriseListResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any]


# ==========================================
# المسارات والعمليات اللوجستية (API Endpoints)
# ==========================================

@router.get("/", response_model=EnterpriseListResponse, summary="استعراض الكوادر اللوجستية")
async def list_enterprise_users(
    skip: int = Query(0, ge=0, description="عدد السجلات المستبعدة لأغراض التصفح (Pagination)"),
    limit: int = Query(50, ge=1, le=200, description="الحد الأقصى للسجلات المعروضة في الصفحة الواحدة"),
    role: Optional[str] = Query(None, description="تصفية النتائج حسب الدور الوظيفي أو الصلاحية"),
    is_active: Optional[bool] = Query(None, description="تصفية حسب حالة الحساب (نشط / متوقف)"),
    search: Optional[str] = Query(None, description="بحث ذكي شامل عبر الاسم أو البريد الإلكتروني"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    استعراض قائمة المستخدمين والكوادر اللوجستية مع دعم التصفية المتقدمة وإدارة الأحمال العالية.
    """
    result = await user_crud.get_multi_filtered(
        db=db, 
        skip=skip, 
        limit=limit, 
        role=role, 
        is_active=is_active, 
        search_query=search
    )
    return {
        "status": "success",
        "message": "تم استرجاع قائمة المستخدمين المؤسسيين والبيانات اللوجستية بنجاح",
        "data": result
    }

@router.post("/", status_code=status.HTTP_201_CREATED, summary="تسجيل حساب مؤسسي جديد")
async def create_new_user(
    user_in: UserCreateSchema,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    تسجيل مستخدم أو عنصر إداري/تشغيلي لوجستي جديد في النظام مع التشفير التلقائي الفوري للبيانات والحماية الأمنية.
    """
    # التحقق من عدم تكرار البريد الإلكتروني المؤسسي
    existing_user = await user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني المدخل مستخدم مسبقاً في النظام اللوجستي المؤسسي"
        )
    
    # تحويل بيانات النطاق إلى القاموس مع تمريرها لطبقة الخدمات
    user_data = user_in.model_dump()
    new_user = await user_crud.create_enterprise_user(db=db, obj_in=user_data)
    
    return {
       "status": "success",
       "message": "تم إنشاء الحساب المؤسسي وتفعيل الصلاحيات اللوجستية بنجاح",
       "user_id": new_user.id,
       "email": new_user.email,
       "role": new_user.role
    }

@router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="الحذف الآمن للحسابات اللوجستية")
async def deactivate_user_account(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    تنفيذ الحذف الآمن (Soft Delete) وإيقاف حساب المستخدم للحفاظ التام على سجلات التدقيق التاريخي للعمليات والشحنات (Audit Trail).
    """
    deleted_user = await user_crud.soft_delete(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم المطلوب غير موجود في النظام أو تم إيقافه مسبقاً"
        )
    return {
        "status": "success",
        "message": f"تم إيقاف الحساب وأرشفة سجلاته بنجاح للمعرف المؤسسي: {user_id}"
    }

