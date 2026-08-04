from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="اسم المستخدم الفريد في النظام")
    email: EmailStr = Field(..., description="البريد الإلكتروني المؤسسي المعتمد")
    full_name: Optional[str] = Field(None, max_length=100, description="الاسم الكامل للمستخدم أو الكيان")
    phone_number: Optional[str] = Field(None, description="رقم الهاتف الدولي مع رمز الدولة")
    is_active: bool = Field(True, description="حالة الحساب (نشط / موقوف)")
    is_verified: bool = Field(False, description="حالة توثيق الهوية السيادية")
    role: str = Field("operator", description="الدور الصلاحي داخل المنصة (admin, operator, client)")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match("^[a-zA-Z0-9_.-]+$", v):
            raise ValueError("اسم المستخدم يجب أن يحتوي فقط على أحرف، أرقام، شرطة سفلية، أو نقاط.")
        return v.lower()

class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, description="كلمة المرور القوية (تتطلب أحرف وأرقام ورموز)")
    sovereign_passkey: Optional[str] = Field(None, description="مفتاح الأمان السيادي الإضافي إن وجد")

    @field_validator('password')
    @classmethod
    def validate_strong_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v) or not re.search(r"[a-z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("كلمة المرور يجب أن تحتوي على أحرف كبيرة وصغيرة وأرقام على الأقل.")
        return v

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class UserResponseSchema(UserBaseSchema):
    id: int = Field(..., description="المعرف الرقمي الفريد للمستخدم")
    two_factor_enabled: bool = Field(False, description="حالة المصادقة الثنائية 2FA")
    last_login_at: Optional[datetime] = Field(None, description="تاريخ ووقت آخر تسجيل دخول ناجح")
    created_at: datetime = Field(..., description="تاريخ ووقت إنشاء الحساب السيادي")
    updated_at: Optional[datetime] = Field(None, description="تاريخ آخر تحديث لبيانات الحساب")

    class Config:
        from_attributes = True

class UserListResponseSchema(BaseModel):
    status: str = "success"
    total_count: int
    page: int
    page_size: int
    users: List[UserResponseSchema]
