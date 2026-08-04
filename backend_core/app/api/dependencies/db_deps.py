# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Database Dependencies Injection
==============================================================================
وحدة الحقن الاعتمادي (Dependency Injection) المعزولة لقواعد البيانات.
صُممت لتوفير اتصالات آمنة، غير متزامنة (Asynchronous)، ومستقلة تماماً.
تمنع تداخل المسارات (Data Leakage/Overlap) وتضمن الاستقرار المطلق للنظام العصبي
أثناء عمليات الذكاء الاصطناعي والمهام اللوجستية المعقدة.
"""

import logging
from typing import AsyncGenerator
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

# استيراد مصنع الجلسات الموزع من الطبقة الأساسية لقاعدة البيانات
from database.db import async_session_maker

logger = logging.getLogger("AegisAICore.DBDependencies")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    مولد الجلسات المعزول (Isolated Session Generator):
    يفتح مساراً مستقلاً وآمناً لكل طلب (Request) قادم من محركات الذكاء الاصطناعي أو البوت.
    يتكفل بمعالجة الأخطاء آلياً (Rollback) وتأمين إغلاق المسار (Close).
    """
    # فتح جلسة اتصال جديدة عبر السياق (Context Manager) لضمان الإدارة الذاتية
    async with async_session_maker() as session:
        try:
            # تسليم الجلسة المعزولة للمسار (Route) الذي طلبها
            yield session
            
        except SQLAlchemyError as db_error:
            # 🛡️ الحماية الذاتية (Self-Healing): التراجع الفوري عن المعاملة لتجنب تلوث البيانات
            await session.rollback()
            logger.error(
                f"⚠️ [DB Security Shield]: رُصد خطأ في مسار البيانات، تم تفعيل التراجع (Rollback) لمنع التداخل. "
                f"التفاصيل: {str(db_error)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="حدث تعارض مؤقت في مسارات البيانات الأساسية. تم تأمين النظام بنجاح وتصحيح المسار."
            )
            
        except Exception as critical_error:
            # 🚨 التقاط أي أخطاء برمجية شاذة أو غير متوقعة لمنع انهيار النظام
            await session.rollback()
            logger.critical(
                f"🚨 [Critical Core Error]: خطأ غير متوقع في مسار المعاملة. "
                f"التفاصيل: {str(critical_error)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="خطأ داخلي حرج في النظام العصبي. تم التدخل الآلي وفصل المسار المتضرر."
            )
            
        finally:
            # 🔒 الإغلاق الإجباري: ضمان عدم تسرب الاتصالات (No Connection Leaks)
            # حتى لو حدث انهيار شامل، سيتم إغلاق المسار وتحرير الذاكرة فوراً
            await session.close()
