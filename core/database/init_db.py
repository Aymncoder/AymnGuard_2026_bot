# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Database Initializer (Cloud Enterprise)
==============================================================================
محطة تهيئة وبناء قاعدة البيانات المركزية لبيئة الإنتاج السحابية.
تم تصحيح الأخطاء النحوية في الاستيراد وتطهيره من الرموز التعبيرية لضمان الاستقرار.
==============================================================================
"""

import asyncio
import logging
from .engine import engine, Base
from . import models

logger = logging.getLogger("SovereignDBInitializer")
logger.setLevel(logging.INFO)

async def init_database():
    """
    تهيئة وبناء جداول قاعدة البيانات بأسلوب غير متزامن وآمن تماماً.
    """
    try:
        logger.info("[DB Initializer]: جاري الاتصال بترسانة البيانات...")
        async with engine.begin() as conn:
            logger.info("[DB Initializer]: جاري بناء هياكل الجداول (المستخدمين، المجموعات، إدارات السوق)...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("[DB Initializer]: تمت تهيئة وتفعيل الترسانة بنجاح وجاهزة لاستقبال البيانات.")
    except Exception as e:
        logger.critical(f"[DB Initializer Error]: فشل حرج أثناء بناء قاعدة البيانات: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_database())
