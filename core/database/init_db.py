import asyncio
from engine import engine, Base
# نقوم باستدعاء النماذج ليتعرف عليها محرك قاعدة البيانات قبل بدء البناء
import models 

async def init_database():
    print("⏳ جاري الاتصال بترسانة البيانات...")
    async with engine.begin() as conn:
        # هذا الأمر يقوم بإنشاء جميع الجداول المحددة في models.py إذا لم تكن موجودة
        print("🏗️ جاري بناء هياكل الجداول (المستخدمين، المجموعات، إشارات السوق)...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ تم بناء وتفعيل الترسانة بنجاح! الإمبراطورية جاهزة الآن لاستقبال البيانات.")

if __name__ == "__main__":
    # تشغيل الدالة غير المتزامنة
    asyncio.run(init_database())
