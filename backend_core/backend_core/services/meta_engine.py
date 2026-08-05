# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Meta-Engine API Router (v5.0)
نقطة النهاية لتلقي طلبات التطوير الذاتي ونشر الأدوات البرمجية الجديدة بأمان تام
=============================================================================
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from backend_core.services.meta_engine import SovereignMetaEngine

router = APIRouter(prefix="/api/v1/meta-engine", tags=["Autonomous Meta-Engine"])

logger = logging.getLogger("AymnGuardMetaRouter")

class FeatureDeploymentRequest(BaseModel):
    file_name: str = Field(..., description="اسم الملف البرمجي الجديد، مثل: custom_tool_router.py")
    source_code: str = Field(..., description="الكود البرمجي المكتوب باللغة Python والمراد فحصه ونشره")
    target_dir: str = Field(default="backend_core/api/v1/", description="المسار المستهدف لحفظ الملف داخل الهيكل")
    admin_signature: str = Field(..., description="التوقيع أو المفتاح السيادي المصرح له بعمليات النشر الذاتي")

@router.post("/deploy", status_code=status.HTTP_200_OK)
async def deploy_new_feature_endpoint(payload: FeatureDeploymentRequest):
    """
    نقطة استقبال طلبات التطوير الذاتي: تفحص الكود، تتحقق من عدم التكرار، وتنشره ديناميكياً.
    """
    # التحقق من الصلاحيات السيادية للمالك أو النظام الذاتي
    expected_signature = "AymnGuard-Sovereign-Meta-Master-Key"
    if payload.admin_signature != expected_signature:
        logger.warning("🚨 [Unauthorized Meta-Deploy Attempt]: محاولة نشر ميزة جديدة بتوقيع غير مسموح به.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="التوقيع السيادي غير صحيح. عمليات النشر الذاتي مقيدة ومحمية بالكامل."
        )

    # تنفيذ فحص الأمان ونشر الملف عبر محرك الميتا
    success = await SovereignMetaEngine.deploy_feature_safely(
        file_name=payload.file_name,
        source_code=payload.source_code,
        target_dir=payload.target_dir
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل فحص الأمان أو تعذر نشر الميزة البرمجية بسبب انتهاك قواعد النحو أو الحظر الأمني."
        )

    return {
        "status": "success",
        "message": f"تم نشر وتفعيل الميزة البرمجية '{payload.file_name}' بنجاح تام في المسار '{payload.target_dir}'.",
        "security_status": "Passed AST & Collision Checks"
    }
