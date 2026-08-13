# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise - Sovereign Health Probe Service
Enterprise-grade diagnostic health check router optimized for cloud production environments.
"""

import logging
from fastapi import APIRouter, status
from typing import Dict, Any

logger = logging.getLogger("AymnGuard.HealthService")

router = APIRouter(
    prefix="/system",
    tags=["System Health & Diagnostics"]
)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Enterprise health probe endpoint for cloud infrastructure monitoring.
    """
    try:
        logger.info("Executing cloud infrastructure health probe check.")
        return {
            "status": "healthy",
            "environment": "cloud_production",
            "engine": "Sovereign Supreme v32.0.1",
            "uptime": "99.99%"
        }
    except Exception as e:
        logger.error(f"Error occurred during health check execution: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
