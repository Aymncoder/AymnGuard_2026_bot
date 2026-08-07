# core/license_manager.py
import secrets
from datetime import datetime, timedelta
from sqlalchemy.future import select
from core.master_kernel import async_session, MasterLicenseModel

class SovereignLicenseManager:
    """محرك إدارة التراخيص والصلاحيات المؤسسي والإمبراطوري الشامل"""

    @staticmethod
    async def generate_license_key(
        has_migration: bool = False, 
        has_trading: bool = False, 
        has_creative: bool = False,
        max_slots: int = 5
    ) -> str:
        """توليد مفتاح سيادي فريد للمستخدم مع تحديد الصلاحيات المبدئية"""
        key = f"AG-EMPIRE-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"
        async with async_session() as session:
            new_license = MasterLicenseModel(
                license_key=key,
                has_migration_tool=has_migration,
                has_trading_analyzer=has_trading,
                has_creative_studio=has_creative,
                max_protection_slots=max_slots,
                used_protection_slots=0,
                maintenance_expires_at=datetime.utcnow() + timedelta(days=30)  # رسوم الصيانة الشهرية الأولية
            )
            session.add(new_license)
            await session.commit()
        return key

    @staticmethod
    async def verify_and_link_user(license_key: str, new_chat_id: str) -> dict:
        """ربط المفتاح بحساب تليجرام جديد (نظام استعادة الحسابات والترحيل الآمن)"""
        async with async_session() as session:
            result = await session.execute(
                select(MasterLicenseModel).where(MasterLicenseModel.license_key == license_key)
            )
            license_obj = result.scalars().first()

            if not license_obj:
                return {"status": "error", "message": "❌ المفتاح غير موجود في السجلات السيادية."}
            
            if not license_obj.is_active:
                return {"status": "error", "message": "❌ هذا المفتاح موقوف أو محظور إدارياً."}

            # تحديث أو ربط الحساب الجديد بالمفتاح السيادي
            license_obj.owner_chat_id = str(new_chat_id)
            await session.commit()
            
            return {
                "status": "success",
                "message": "✅ تمت استعادة الصلاحيات وربط المفتاح بنجاح بالحساب الجديد.",
                "details": {
                    "migration_tool": license_obj.has_migration_tool,
                    "trading_analyzer": license_obj.has_trading_analyzer,
                    "creative_studio": license_obj.has_creative_studio,
                    "max_slots": license_obj.max_protection_slots,
                    "used_slots": license_obj.used_protection_slots,
                    "maintenance_expires_at": license_obj.maintenance_expires_at.strftime("%Y-%m-%d") if license_obj.maintenance_expires_at else "Lifetime"
                }
            }

    @staticmethod
    async def check_service_access(license_key: str, service_name: str) -> bool:
        """التحقق من صلاحية الخدمة وحالة اشتراك الصيانة والدعم المستمر"""
        async with async_session() as session:
            result = await session.execute(
                select(MasterLicenseModel).where(MasterLicenseModel.license_key == license_key)
            )
            license_obj = result.scalars().first()

            if not license_obj or not license_obj.is_active:
                return False

            # فحص حالة اشتراك الصيانة التشغيلية والدعم
            if license_obj.maintenance_expires_at and license_obj.maintenance_expires_at < datetime.utcnow():
                return False  # توقف الخدمات مؤقتاً لعدم سداد رسوم الصيانة والدعم

            # فحص الخدمة المستهدفة بدقة
            if service_name == "migration" and not license_obj.has_migration_tool:
                return False
            if service_name == "trading" and not license_obj.has_trading_analyzer:
                return False
            if service_name == "creative" and not license_obj.has_creative_studio:
                return False

            return True

    @staticmethod
    async def manage_protection_slot(license_key: str, action: str) -> dict:
        """إدارة خانات الحماية (نظام الـ 5 مجموعات الديناميكي ونقل الحماية)"""
        async with async_session() as session:
            result = await session.execute(
                select(MasterLicenseModel).where(MasterLicenseModel.license_key == license_key)
            )
            license_obj = result.scalars().first()

            if not license_obj or not license_obj.is_active:
                return {"status": "error", "message": "❌ المفتاح غير صالح أو موقوف."}

            if action == "ADD":
                if license_obj.used_protection_slots >= license_obj.max_protection_slots:
                    return {
                        "status": "limit_exceeded", 
                        "message": "⚠️ تم استنفاد الحد الأقصى لخانات الحماية (5 مجموعات). يرجى إلغاء حماية مجموعة سابقة أو التوسع بـ 10$."
                    }
                license_obj.used_protection_slots += 1
                await session.commit()
                return {"status": "success", "message": f"✅ تمت الإضافة بنجاح. الخانات المستخدمة: {license_obj.used_protection_slots}/{license_obj.max_protection_slots}"}

            elif action == "REMOVE":
                if license_obj.used_protection_slots > 0:
                    license_obj.used_protection_slots -= 1
                    await session.commit()
                return {"status": "success", "message": f"✅ تم تحرير الخانة بنجاح. الخانات المستخدمة: {license_obj.used_protection_slots}/{license_obj.max_protection_slots}"}

            return {"status": "error", "message": "❌ إجراء غير معروف."}
