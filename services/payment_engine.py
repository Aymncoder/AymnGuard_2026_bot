# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Payment Engine
محرك المعاملات المالية، التحقق من المدفوعات، وإصدار التراخيص السيادية
=============================================================================
"""

from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# 🛡️ تصحيح المسارات المعمارية لتوحيد الجذور داخل backend_core
from backend_core.models.user import User
# ملاحظة: تأكد من توافق أسماء النماذج والسكيمات مع الجداول المعتمدة لديك
from backend_core.models.payment import PaymentTransactionModel  # نموذج المعاملات المالية
from backend_core.schemas.payment_schema import PaymentWebhookPayload

class SovereignPaymentEngine:
    PRICING_TIERS = {
        "tool": 15.0,
        "bot": 10.0,
        "vip": 30.0
    }

    @staticmethod
    async def verify_and_grant_license(payload: PaymentWebhookPayload, session: AsyncSession, alert_manager=None) -> dict:
        service_key = payload.target_service.lower()
        if service_key not in SovereignPaymentEngine.PRICING_TIERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="الخدمة المستهدفة غير صالحة في نظام التسعير السيادي."
            )

        required_amount = SovereignPaymentEngine.PRICING_TIERS[service_key]

        if payload.amount < required_amount:
            return {
                "status": "rejected",
                "reason": f"المبلغ المدفوع ({payload.amount}) أقل من الحد الأدنى المطلوب ({required_amount})."
            }

        # التحقق من عدم تكرار معرف المعاملة (TxID) لمنع الاحتيال المالي
        existing_tx_query = select(PaymentTransactionModel).where(PaymentTransactionModel.tx_id == payload.tx_id)
        existing_tx_result = await session.execute(existing_tx_query)
        if existing_tx_result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="معرف المعاملة (TxID) مستخدم مسبقاً في النظام."
            )

        # تسجيل المعاملة الجديدة
        new_tx = PaymentTransactionModel(
            tx_id=payload.tx_id,
            chat_id=payload.chat_id,
            amount_payload=payload.amount,
            currency=payload.currency,
            target_service=service_key,
            status="verified"
        )
        session.add(new_tx)

        # التحقق من وجود المستخدم أو إنشائه ومنح الصلاحية
        user_query = select(User).where(User.chat_id == payload.chat_id)
        user_res = await session.execute(user_query)
        user = user_res.scalars().first()

        if not user:
            user = User(
                chat_id=payload.chat_id,
                username="VerifiedUser",
                is_vip=1 if service_key == "vip" else 0,
                subscription_type=f"Licensed-{service_key.upper()}"
            )
            session.add(user)
        else:
            if service_key == "vip":
                user.is_vip = 1
            user.subscription_type = f"Licensed-{service_key.upper()}"

        await session.commit()

        if alert_manager:
            await alert_manager.broadcast_alert({
                "level": "PAYMENT_SUCCESS",
                "message": f"تم استلام دفعة بقيمة {payload.amount} {payload.currency} لباقة {service_key.upper()}.",
                "timestamp": datetime.now().isoformat()
            })

        return {
            "status": "success",
            "message": "تم التحقق من الدفع وفتح الترخيص بنجاح تام وبشكل آلي.",
            "service_unlocked": service_key,
            "tx_id": payload.tx_id
        }
