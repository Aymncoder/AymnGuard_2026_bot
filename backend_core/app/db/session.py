import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import async_session_maker

# إعداد نظام التتبع والتدقيق اللوجستي للأخطاء
logger = logging.getLogger("AymnGuard.EnterpriseLogistics.DB")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    مُزود جلسات قاعدة البيانات المؤسسية المتقدم (Enterprise Async Session Dependency)
    مصمم خصيصاً للعمليات اللوجستية الضخمة ذات التزامن العالي (High Concurrency)،
    مع إدارة ذكية للمعاملات، الالتزام التلقائي (Commit)، والتراجع الآمن (Rollback) عند حدوث أي استثناء،
    وضمان إغلاق الاتصالات بدقة لمنع تسريب الموارد في مسبح الاتصالات (Connection Pool).
    """
    async with async_session_maker() as session:
        try:
            yield session
            # اعتماد المعاملة تلقائياً عند نجاح العمليات اللوجستية البرمجية
            await session.commit()
        except SQLAlchemyError as db_err:
            await session.rollback()
            logger.error(f"خطأ في قاعدة البيانات أثناء تنفيذ العملية اللوجستية: {str(db_err)}")
            raise
        except Exception as general_err:
            await session.rollback(
            )
            logger.critical(f"خطأ غير متوقع في البنية التحتية للمعاملة: {str(general_err)}")
            raise
        finally:
            # ضمان تحرير الاتصال وإعادته للمسبح بسلام تام
            await session.close()


class LogisticsTransactionManager:
    """
    مدير المعاملات المتقدم للعمليات اللوجستية المعقدة (Nested Savepoints Manager).
    يستخدم لإدارة العمليات الضخمة متعددة المراحل (مثل: سلاسل الإمداد وتحديثات الأساطيل المتزامنة)
    بحيث يمكن إنشاء نقاط حفظ فرعية (Savepoints) والتراجع عنها جزئياً عند الحاجة.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.transaction = await self.session.begin_nested()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.transaction.rollback()
            logger.warning("تم التراجع عن نقطة الحفظ الفرعية (Nested Savepoint) بسبب خطأ تشغيلي لوجستي.")
        else:
            await self.transaction.commit()

