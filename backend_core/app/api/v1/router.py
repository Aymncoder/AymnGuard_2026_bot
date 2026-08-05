# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise Edition - The Sovereign API Gateway (v1)
البوابة المركزية الموحدة - دمج وتوجيه كافة قطاعات المنصة السيادية
تضمن هذه الهندسة العزل التام للنطاقات (Domain Isolation) ومنع أي تداخل.
=============================================================================
"""

import logging
from fastapi import APIRouter

# استيراد كافة أدمغة المنصة وقطاعاتها الحيوية
from app.api.v1.endpoints import (
    auth, system, users, 
    telegram, telegram_bot, telethon_transfer, 
    ai_services, web3_financial
)

logger = logging.getLogger("AymnGuardGateway")

# 🛡️ إنشاء الموجه المركزي الأوحد
api_v1_router = APIRouter()

# ==============================================================================
# 1. قطاع الهوية والتشخيص (Identity, Access & Health)
# ==============================================================================
api_v1_router.include_router(auth.router) # البادئة معرفة مسبقاً داخل الملف
api_v1_router.include_router(system.router)
api_v1_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["Enterprise User Management"]
)

# ==============================================================================
# 2. قطاع أتمتة الشبكات واللوجستيات الرقمية (Automation & Telethon Logistics)
# ==============================================================================
# 🚨 تصحيح الثغرة: تم منح بادئة مخصصة للتليجرام لمنع التلوث المساري (Namespace Pollution)
api_v1_router.include_router(
    telegram.router, 
    prefix="/network/telegram-core", 
    tags=["Sovereign Telegram Operations"]
)
api_v1_router.include_router(
    telegram_bot.router, 
    prefix="/network/bot-manager", 
    tags=["Telegram Bot API"]
)
api_v1_router.include_router(
    telethon_transfer.router, 
    prefix="/logistics/telethon-bulk", 
    tags=["Sovereign Telethon Logistics & Transfers"]
)

# ==============================================================================
# 3. قطاع محركات الذكاء الاصطناعي (Cognitive AI Engines)
# ==============================================================================
api_v1_router.include_router(
    ai_services.router, 
    prefix="/ai-core", 
    tags=["Advanced AI & Neural Services"]
)

# ==============================================================================
# 4. قطاع البوابات المالية اللامركزية (Web3 Sovereign Finance)
# ==============================================================================
api_v1_router.include_router(
    web3_financial.router, 
    prefix="/finance/web3", 
    tags=["Web3 & Decentralized Financial Gateways"]
)

logger.info("🌐 [Sovereign Gateway]: تم دمج وتأمين كافة قطاعات المنصة. لا يوجد أي تداخل مساري.")
