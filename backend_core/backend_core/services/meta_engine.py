# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise - Sovereign Meta-Engine API Router (v5.0)
نقطة النهاية التلقائية لتلقي طلبات التطوير الذاتي ونشر الميزات بأمان تام
"""

import os
import logging
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
# استيراد محرك الميتا (تأكد من أن المسار صحيح لديك)
from backend_core.services.meta_engine_core import SovereignMetaEngine

router = APIRouter(prefix="/api/v1/meta-engine", tags=["Autonomous Meta-Engine"])
logger = logging.getLogger("AymnGuardMetaRouter")

class FeatureDeploymentRequest(BaseModel):
    file_name: str = Field(..., description="اسم الملف البرمجي الجديد، مثل: auto_trader.py")
    source_code: str = Field(..., description="الكود البرمجي المكتوب بلغة Python")
    target_dir: str = Field(..., description="المسار المستهدف داخل المشروع")
    admin_signature: str = Field(..., description="المفتاح السيادي السري للنشر")

@router.post("/deploy", status_code=status.HTTP_200_OK)
async def deploy_new_feature_endpoint(payload: FeatureDeploymentRequest):
    """
    نقطة استقبال طلبات التطوير الذاتي: فحص الكود، التحقق من عدم الاختراق، ونشره ديناميكياً.
    """
    
    # 1. التحقق السيادي الآمن (استدعاء المفتاح من متغيرات البيئة وليس مكشوفاً)
    expected_signature = os.getenv("META_MASTER_KEY", "fallback_secure_key_do_not_use_in_prod")
    
    if payload.admin_signature != expected_signature:
        logger.warning(f"🚨 [Unauthorized Meta-Deploy Attempt]: تم رصد محاولة اختراق فاشلة للمحرك السيادي!")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="التوقيع السيادي غير صحيح. عمليات النشر الذاتي مقيدة ومحمية بالكامل."
        )

    # 2. درع حماية المسارات (Directory Traversal Protection)
    # نمنع المتسللين من استخدام "../" للخروج من مجلد المشروع
    safe_target = Path(payload.target_dir).resolve()
    base_project_dir = Path(__file__).parent.parent.parent.resolve() # تحديد جذر المشروع

    if not str(safe_target).startswith(str(base_project_dir)):
         logger.critical("🚨 [Security Breach]: محاولة زرع ملفات خارج حدود الإمبراطورية!")
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="المسار المستهدف غير آمن ومخالف للهندسة السيادية."
         )

    # 3. التنفيذ السيادي الآمن
    success = await SovereignMetaEngine.deploy_feature_safely(
        file_name=payload.file_name,
        source_code=payload.source_code,
        target_dir=str(safe_target)
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="الأمان أوقف نشر الميزة البرمجية بسبب انتهاك قواعد النحو (AST) أو الخطر الأمني."
        )

    return {
        "status": "success",
        "message": f"بالفعل الميزة البرمجية '{payload.file_name}' بنجاح تام.",
        "security_status": "Passed AST & Collision Checks"
    }
