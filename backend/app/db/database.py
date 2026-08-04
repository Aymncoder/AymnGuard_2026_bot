from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# إنشاء محرك الاتصال غير المتزامن بمعايير مؤسسية عالية
engine = create_async_engine(
    str(settings.DATABASE_URL), 
    echo=True,                   # تفعيل عرض الاستعلامات البرمجية لتتبع العمليات اللوجستية بدقة
    future=True,
    pool_size=20,                # مسبح الاتصالات المتزامنة
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

# صانع الجلسات اللوجستية والمؤسسية
async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,      
    autocommit=False,            
    autoflush=False
)

# القاعدة الأساسية لجميع نماذج وجداول المنصة اللوجستية
class Base(AsyncAttrs, DeclarativeBase):
    pass

