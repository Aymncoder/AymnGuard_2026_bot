# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign License Manager (v18.0.0-Master)
==============================================================================
محرك إدارة التراخيص والصلاحيات المؤسسي: يمنع اختطاف التراخيص (Hijack Protection)،
يدير الاشتراكات (Maintenance)، ويحمي قواعد البيانات من التداخل.
"""

import secrets
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from core.master_kernel import async_session, MasterLicenseModel

logger = logging.getLogger("SovereignLicenseManager")

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
        
        try:
            async with async_session() as session:
                new_license = MasterLicenseModel(
                    license_key=key,
                    has_migration_tool=has_migration,
                    has_trading_analyzer=has_trading,
                    has_creative_studio=has_creative,
                    max_protection_slots=max_slots,
                    used_protection_slots=0,
                    # استخدام التوقيت العالمي الحديث والموثوق
                    maintenance_expires_at=datetime.now(timezone.utc) + timedelta(days=30) 
                )
                session.add(new_license)
                await session.commit()
                logger.info(f"🗝️ [License Vault]: تم إصدار مفتاح سيادي جديد بنجاح: {key}")
                return key
        except SQLAlchemyError as e:
            logger.error(f"❌ [License Vault Error]: فشل في توليد المفتاح: {e}")
            return "ERROR_GENERATING_KEY"

    @staticmethod
    async def verify_and_link_user(license_key: str, new_chat_id: str) -> dict:
        """ربط المفتاح بحساب تليجرام جديد (مع نظام الحماية من الاختطاف)"""
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(MasterLicenseModel).where(MasterLicenseModel.license_key == license_key)
                )
                license_obj = result.scalars().first()

                if not license_obj:
                    logger.warning(f"⚠️ [License Vault]: محاولة استخدام مفتاح غير صالح: {license_key}")
                    return {"status": "error", "message": "❌ المفتاح غير موجود في السجلات السيادية."}
                
                if not license_obj.is_active:
                    return {"status": "error", "message": "❌ هذا المفتاح موقوف أو محظور إدارياً."}

                # 🛡️ الحماية من اختطاف التراخيص (Anti-Hijack Lock)
                new_chat_id_str = str(new_chat_id)
                if license_obj.owner_chat_id and license_obj.owner_chat_id != new_chat_id_str:
                    logger.critical(f"🚨 [Security Breach]: محاولة اختطاف مفتاح! الحساب {new_chat_id_str} حاول سرقة مفتاح {license_obj.owner_chat_id}")
                    return {"status": "error", "message": "❌ هذا المفتاح مستخدم ومربوط بحساب آخر مسبقاً. يرجى التواصل مع الإدارة."}

                # تحديث أو ربط الحساب الجديد بالمفتاح السيادي
                license_obj.owner_chat_id = new_chat_id_str
                await session.commit()
                
                logger.info(f"✅ [License Vault]: تم ربط المفتاح {license_key} بالحساب {new_chat_id_str}")
                return {
                    "status": "success",
                    "message": "✅ تمت استعادة الصلاحيات وربط المفتاح بنجاح بالحساب.",
                    "details": {
                        "migration_tool": license_obj.has_migration_tool,
                        "trading_analyzer": license_obj.has_trading_analyzer,
                        "creative_studio": license_obj.has_creative_studio,
                        "max_slots": license_obj.max_protection_slots,
                        "used_slots": license_obj.used_protection_slots,
                        "maintenance_expires_at": license_obj.maintenance_expires_at.strftime("%Y-%m-%d") if license_obj.maintenance_expires_at else "Lifetime"
                    }
                }
        except SQLAlchemyError as e:
            logger.error(f"❌ [Database Error]: فشل التحقق من المفتاح {license_key}: {e}")
            return {"status": "error", "message": "❌ خطأ في الاتصال بخزنة التراخيص."}

    @staticmethod
    async def check_service_access(license_key: str, service_name: str) -> bool:
        """التحقق من صلاحية الخدمة وحالة اشتراك الصيانة والدعم المستمر"""
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(MasterLicenseModel).where(MasterLicenseModel.license_key == license_key)
                )
                license_obj = result.scalars().first()

                if not license_obj or not license_obj.is_active:
                    return False

                # فحص حالة اشتراك الصيانة التشغيلية والدعم
                if license_obj.maintenance_expires_at and license_obj.maintenance_expires_at < datetime.now(timezone.utc):
                    logger.debug(f"💳 [License Expired]: انتهت صلاحية الدعم للمفتاح {license_key}")
                    return False

                # فحص الخدمة المستهدفة بدقة
                if service_name == "migration" and not license_obj.has_migration_tool:
                    return False
                if service_name == "trading" and not license_obj.has_trading_analyzer:
                    return False
                if service_name == "creative" and not license_obj.has_creative_studio:
                    return False

                return True
        except Exception:
            return False

    @staticmethod
    async def manage_protection_slot(license_key: str, action: str) -> dict:
        """إدارة خانات الحماية (نظام الـ 5 مجموعات الديناميكي ونقل الحماية)"""
        try:
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
                            "message": "⚠️ تم استنفاد الحد الأقصى لخانات الحماية. يرجى إلغاء حماية مجموعة سابقة أو التوسع بـ 10$."
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
        except SQLAlchemyError as e:
            logger.error(f"❌ [Database Error]: فشل إدارة خانات الحماية: {e}")
            return {"status": "error", "message": "❌ خطأ في التواصل مع الخزنة."}
