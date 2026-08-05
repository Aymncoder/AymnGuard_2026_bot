# -*- coding: utf-8 -*-
from fastapi import APIRouter
from backend_core.app.api.v1.endpoints.auth import router as auth_router

api_router = APIRouter()

# إدراج محرك المصادقة والتوكنات ضمن البوابات النشطة
api_router.include_router(auth_router)
