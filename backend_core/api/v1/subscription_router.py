# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Subscription & Licensing API Router
نقطة النهاية السيادية لمعالجة الاشتراكات وعمليات الشراء من داخل التطبيق
=============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from backend_core.database import get_db
from backend_core.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/api/v1/subscriptions", tags=["Subscriptions & Licensing"])

class PurchaseRequest(BaseModel):
    telegram_id: int
    tier: str # مثل: bot_only, transfer_tool, vip_all
    amount: float
    coupon: str = None

@router.post("/purchase")
async def purchase_subscription_endpoint(payload: PurchaseRequest, db: AsyncSession = Depends(get_db)):
    """
    معالجة طلب شراء أو تفعيل باقة اشتراك وترقية حساب المشترك فوراً.
    """
    try:
        user = await SubscriptionService.upgrade_subscription(
            db, payload.telegram_id, payload.tier, payload.amount, payload.coupon
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="المستخدم غير مسجل في قاعدة البيانات السيادية."
            )

        return {
            "status": "success",
            "message": f"تم تفعيل ترخيص {payload.tier} بنجاح تام وحفظه في السجلات.",
            "subscription": {
                "telegram_id": user.telegram_id,
                "tier": user.subscription_tier,
                "is_vip": user.is_vip,
                "expires_at": user.subscription_expires_at.isoformat() if user.subscription_expires_at else None
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في معالجة الاشتراك السيادي: {str(e)}"
        )
