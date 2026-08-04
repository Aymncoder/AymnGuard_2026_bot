from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.session import get_db
from app.services.telethon_manager import AymnGuardTelethonManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["Sovereign Telegram Core Operations"])

class SingleInviteSchema(BaseModel):
    api_id: int = Field(..., description="معرف التطبيق الخاص بحساب تيليجرام (API ID)")
    api_hash: str = Field(..., description="البصمة الأمنية للتطبيق (API Hash)")
    string_session: Optional[str] = Field(None, description="جلسة تيليجرام النصية المشفرة")
    target_group: str = Field(..., description="معرف أو رابط المجموعة المستهدفة")
    user_to_invite: str = Field(..., description="معرف أو اسم المستخدم المراد إضافته")

    @field_validator('api_id')
    @classmethod
    def v_api_id(cls, v):
        if v <= 0:
            raise ValueError("يجب أن يكون معرف الـ API رقماً موجباً صحيحاً.")
        return v

class OperationResponseSchema(BaseModel):
    status: str
    operation_result: Dict[str, Any]
    message: str
    system_version: str = "AymnGuard Enterprise v2.6"

@router.post(
    "/invite-member",
    response_model=OperationResponseSchema,
    summary="تنفيذ عملية إضافة عضو مؤمنة وسيادية",
    description="نقطة نهاية متطورة تدير الاتصال، تنفذ العمليات اللوجستية، وتحمي النظام من الحظر التفاعلي."
)
async def invite_member_endpoint(
    data: SingleInviteSchema,
    db: AsyncSession = Depends(get_db)
):
    manager = AymnGuardTelethonManager(
        api_id=data.api_id,
        api_hash=data.api_hash,
        string_session=data.string_session
    )
    
    is_connected = await manager.initialize_client()
    if not is_connected:
        logger.error("فشل الاتصال بخوادم تيليجرام أثناء محاولة تنفيذ أمر الإضافة.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل المصادقة أو أن جلسة تيليجرام غير صالحة أو منتهية الصلاحية."
        )
    
    try:
        result = await manager.safe_invite_member(
            target_group=data.target_group,
            user_to_invite=data.user_to_invite
        )
        
        if result.get("status") == "flood_wait":
            logger.warning(f"تم رصد تقييد FloodWait مؤقت لمدة {result.get('seconds')} ثانية.")
        
        return {
            "status": "success" if result.get("status") == "success" else "warning",
            "operation_result": result,
            "message": "تمت معالجة الطلب عبر النواة السيادية بنجاح."
        }
        
    except Exception as e:
        logger.critical(f"خطأ غير متوقع في طبقة الـ API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"حدث خطأ داخلي في النظام السيادي: {str(e)}"
        )
        
    finally:
        await manager.disconnect()
