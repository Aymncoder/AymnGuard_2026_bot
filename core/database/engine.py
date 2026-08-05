from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# نستخدم SQLite غير المتزامن كبداية صلبة ومرنة
DATABASE_URL = "sqlite+aiosqlite:///aymnguard_enterprise.db"

# إنشاء المحرك غير المتزامن (Async Engine)
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, # اجعلها True لاحقاً إذا أردت رؤية أوامر SQL في الطرفية للتدقيق
    future=True
)

# إنشاء مصنع الجلسات (Session Factory)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# القاعدة الأساسية التي سترث منها جميع الجداول
Base = declarative_base()

# دالة لتوليد جلسات الاتصال بقاعدة البيانات بأمان
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
