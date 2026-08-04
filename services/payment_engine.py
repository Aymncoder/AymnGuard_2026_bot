# services/payment_engine.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from models import PaymentTransactionModel, UserAuthModel
from schemas import PaymentWebhookPayload

class SovereignPaymentEngine:
    PRICING_TIERS = {
        "tool": 15.0,
        "bot": 10.0,
        "vip": 30.0
    }

    @staticmethod
    async def verify_and_grant_license(payload: PaymentWebhookPayload, session: AsyncSession, alert_manager) -> dict:
        service_key = payload.target_service.lower()
        if service_key not in SovereignPaymentEngine.PRICING_TIERS:
            raise HTTPException(status_code=400, detail="الخدمة المستهدفة غير صالحة في نظام التسعير السيادي.")

        required_amount = SovereignPaymentEngine.PRICING_TIERS[service_key]

        if payload.amount < required_amount:
            return {
                "status": "rejected",
                "reason": f"المبلغ المدفوع ({payload.amount}) أقل من الحد الأدنى المطلوب ({required_amount})."
            }

        existing_tx = await session.execute(select(PaymentTransactionModel).where(PaymentTransactionModel.tx_id == payload.tx_id))
        if existing_tx.scalars().first():
            raise HTTPException(status_code=400, detail="معرف المعاملة (TxID) مستخدم مسبقاً.")

        new_tx = PaymentTransactionModel(
            tx_id=payload.tx_id,
            chat_id=payload.chat_id,
            amount=payload.amount,
            currency=payload.currency,
            target_service=service_key,
            status="verified"
        )
        session.add(new_tx)

        user_res = await session.execute(select(UserAuthModel).where(UserAuthModel.chat_id == payload.chat_id))
        user = user_res.scalars().first()

        if not user:
            user = UserAuthModel(
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

        await alert_manager.broadcast_alert({
            "level": "PAYMENT_SUCCESS",
            "message": f"تم استلام دفعة بقيمة {payload.amount} {payload.currency} بنجاح وتم فتح ترخيص ({service_key.upper()}).",
            "timestamp": datetime.now().isoformat()
        })

        return {
            "status": "success",
            "message": "تم التحقق من الدفع وفتح الترخيص بنجاح تام وبشكل آلي.",
            "service_unlocked": service_key,
            "tx_id": payload.tx_id
        }
