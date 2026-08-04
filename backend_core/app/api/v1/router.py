"""
=============================================================================
Project: AymnGuard Enterprise Edition (v2.6)
Module: Central API Router Hub
Description: التوجيه المركزي المتقدم لجميع المسارات البرمجية، الخدمات اللوجستية، 
المالية، وتقنيات الذكاء الاصطناعي مع هيكلة مؤمنة وقابلة للتوسع المستقبلي.
=============================================================================
"""

from fastapi import APIRouter, Depends
from app.api.v1.endpoints import (
    telegram,
    telegram_bot,
    telethon_transfer,
    users,
    ai_services,
    web3_financial
)
# استيراد الاعتماديات السيادية العامة إن وجدت (مثل التحقق من رتبة النظام)
# from app.api.dependencies.auth import verify_sovereign_gateway

# إنشاء الموجه الرئيسي مع متطلبات توثيق متطورة
api_router = APIRouter()

# 1. قطاع أتمتة وعمليات التليجرام السيادية (Userbot Core)
api_router.include_router(
    telegram.router,
    prefix="",
    tags=["Sovereign Telegram Operations"]
)

# 2. قطاع إدارة البوتات التفاعلية والخدمية (Telegram Bot API)
api_router.include_router(
    telegram_bot.router,
    prefix="/bot",
    tags=["Telegram Bot Management"]
)

# 3. قطاع اللوجستيات الرقمية وعمليات النقل الضخمة (Bulk Logistics & Scraping)
api_router.include_router(
    telethon_transfer.router,
    prefix="/logistics",
    tags=["Sovereign Telethon Logistics & Transfers"]
)

# 4. قطاع إدارة المستخدمين، الهويات، والصلاحيات (Identity & Access)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Enterprise User & Security Management"]
)

# 5. قطاع محركات الذكاء الاصطناعي والأتمتة المعرفية (AI Cognitive Engines)
api_router.include_router(
    ai_services.router,
    prefix="/ai",
    tags=["Advanced AI & Neural Services"]
)

# 6. قطاع العملات الرقمية، البوابات المالية والـ Web3 (Sovereign Finance)
api_router.include_router(
    web3_financial.router,
    prefix="/finance",
    tags=["Web3 & Decentralized Financial Gateways"]
)

