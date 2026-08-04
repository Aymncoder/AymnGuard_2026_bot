# schemas.py (نماذج الكوبونات والمدفوعات)
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CouponCreatePayload(BaseModel):
    code: str = Field(..., description="كود الخصم أو التفعيل الفريد")
    discount_value: float = Field(..., description="قيمة أو نسبة التخفيض")
    target_service: str = Field("all", description="الخدمة المستهدفة: tool, bot, vip, all")
    max_uses: int = Field(1, description="الحد الأقصى لعدد مرات الاستخدام")
    expires_at: Optional[datetime] = Field(None, description="وقت انتهاء الصلاحية")

class CouponRedeemPayload(BaseModel):
    chat_id: str = Field(..., description="معرف المستخدم المستفيد")
    code: str = Field(..., description="الكود المراد استبداله وتفعليه")

class PaymentWebhookPayload(BaseModel):
    tx_id: str = Field(..., description="معرف المعاملة الفريد أو الـ Transaction Hash")
    chat_id: str = Field(..., description="معرف المستخدم صاحب الطلب")
    amount: float = Field(..., description="المبلغ المدفوع الفعلي")
    currency: str = Field("USDT", description="عملة الدفع")
    target_service: str = Field(..., description="الخدمة المطلوب ترخيصها: tool, bot, vip")
