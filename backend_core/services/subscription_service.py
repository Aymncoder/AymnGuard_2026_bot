# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Subscription & Licensing Service
خدمة إدارة الاشتراكات، التراخيص، والتحقق من صلاحيات المشتركين
=============================================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend_core.models.database_models import UserModel, TransactionModel
from datetime import datetime, timedelta

class SubscriptionService:
    """
    مدير العمليات والاشتراكات السيادية للمستخدمين.
    """

    @staticmethod
    async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str, first_name: str) -> UserModel:
        """
        التحقق من وجود المشترك في قاعدة البيانات، وإنشاؤه تلقائياً إذا كان دخولاً جديداً.
        """
        result = await db.execute(select(UserModel).where(UserModel.telegram_id == telegram_id))
        user = result.scalars().first()

        if not user:
            user = UserModel(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                is_vip=False,
                subscription_tier="free"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    @staticmethod
    async def upgrade_subscription(db: AsyncSession, telegram_id: int, tier: str, amount: float, coupon: str = None) -> UserModel:
        """
        ترقية اشتراك المستخدم وتسجيل المعاملة المالية في السجلات الدائمة.
        """
        result = await db.execute(select(UserModel).where(UserModel.telegram_id == telegram_id))
        user = result.scalars().first()

        if user:
            user.subscription_tier = tier
            user.is_vip = (tier == "vip_all")
            user.subscription_expires_at = datetime.utcnow() + timedelta(days=30) # ترخيص ساري لمدة 30 يوماً

            # تسجيل المعاملة المالية في جدول التدقيق والدعم
            tx = TransactionModel(
                telegram_id=telegram_id,
                amount=amount,
                service_type=tier,
                coupon_used=coupon,
                status="completed"
            )
            db.add(tx)
            await db.commit()
            await db.refresh(user)
            return user
        return None
