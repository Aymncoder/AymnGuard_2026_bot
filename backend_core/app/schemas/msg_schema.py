"""
=============================================================================
AymnGuard Enterprise Logistics Platform - Advanced Message & Response Schemas
هياكل الاستجابات والرسائل المؤسسية السيادية - معايير عالمية متقدمة للتكامل.
=============================================================================
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class MsgResponse(BaseModel):
    """هيكل الاستجابة المؤسسي الموحد والنقي لكافة خدمات المنصة العالمية"""
    status: str = Field("success", description="حالة العملية (success, error, warning)")
    code: int = Field(200, description="كود الاستجابة البرمجي أو HTTP Status")
    message: str = Field(..., description="الرسالة التوضيحية الناتجة عن التنفيذ")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="تاريخ ووقت الاستجابة السيادية")
    request_id: Optional[str] = Field(None, description="المعرف الفريد لتتبع الطلب وتجنب التشويش")
    data: Optional[Any] = Field(None, description="بيانات الحمولة الناتجة عن العملية أو الـ Payload")

class ErrorMsgResponse(BaseModel):
    """هيكل الاستجابة للأخطاء الاستباقية المتقدمة"""
    status: str = Field("error", description="حالة الطلب البرمجي (خطأ)")
    error_code: str = Field("ERR_SOVEREIGN_CORE", description="الرمز البرمجي المعياري للخطأ")
    message: str = Field(..., description="رسالة الخطأ التفصيلية")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="تفاصيل تقنية إضافية لتشخيص الأخطاء")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="وقت حدوث الاستثناء")
