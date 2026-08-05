# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Search & Media API Router
نقطة النهاية السيادية لخدمات البحث الشامل وتشغيل الوسائط
=============================================================================
"""

from fastapi import APIRouter, HTTPException, status, Query
from backend_core.services.search_media_engine import UniversalSearchEngine

router = APIRouter(prefix="/api/v1/search", tags=["Universal Search & Media"])

@router.get("/")
async def execute_universal_search(
    q: str = Query(..., description="نص الاستعلام أو الكلمة المراد البحث عنها"),
    platform: str = Query("all", description="المنصة المستهدفة: all, youtube, social, web")
):
    """
    نقطة النهاية السيادية لإجراء البحث الموحد والفوري عبر كافة المنصات.
    """
    try:
        if not q.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="يجب إدخال نص البحث المطلوب."
            )
            
        data = await UniversalSearchEngine.search_everything(q, platform)
        return data
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ داخلي في محرك البحث: {str(e)}"
        )
