"""
=============================================================================
AymnGuard Enterprise Logistics Platform - API Router Aggregator
مجمع المسارات المركزي - ربط وتوحيد كافة نقاط نهاية الـ API الخاصة بالمنصة.
=============================================================================
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# ربط مسارات المصادقة وإدارة المستخدمين السيادية
api_router.include_router(auth.router)

# مجهز لاستقبال المزيد من المسارات والخدمات اللوجستية المستقبلية بكفاءة مطلقة
