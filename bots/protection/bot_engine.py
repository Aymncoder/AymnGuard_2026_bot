# bots/protection/bot_engine.py
from core.license_manager import SovereignLicenseManager

class SovereignProtectionEngine:
    """محرك الحماية السيادية - البوت الأول في مصفوفة الخدمات المستقلة"""

    @staticmethod
    async def activate_protection(license_key: str, channel_id: str) -> dict:
        """
        تفعيل درع الحماية لمجموعة أو قناة جديدة.
        يتحقق تلقائياً من:
        1. حالة اشتراك الصيانة والدعم المستمر.
        2. توفر خانات فارغة في نظام الـ 5 مجموعات الديناميكي.
        """
        # 1. التحقق من صلاحية المفتاح وحالة الصيانة العامة
        is_active = await SovereignLicenseManager.check_service_access(license_key, "protection")
        if not is_active:
            return {
                "status": "error",
                "message": "❌ **فشل التفعيل:** اشتراك الصيانة والدعم الخاص بك منتهي، أو أن المفتاح موقوف. يرجى التجديد لاستمرار الحماية."
            }

        # 2. إدارة الخانات الديناميكية (التحقق من الحد الأقصى 5 مجموعات)
        slot_action = await SovereignLicenseManager.manage_protection_slot(license_key, "ADD")
        
        if slot_action["status"] == "limit_exceeded":
            return {
                "status": "limit_exceeded",
                "message": slot_action["message"] # تنبيه التوسع بـ 10 دولار أو إلغاء حماية قناة سابقة
            }
        elif slot_action["status"] == "error":
            return slot_action

        # 3. نجاح عملية التفعيل وبدء تشغيل درع الحماية للمجموعة
        return {
            "status": "success",
            "message": f"🛡️ **تم تفعيل الدرع السيادي بنجاح!**\n\n- معرف القناة/المجموعة: `{channel_id}`\n- {slot_action['message']}"
        }

    @staticmethod
    async def deactivate_protection(license_key: str, channel_id: str) -> dict:
        """
        إلغاء الحماية عن مجموعة أو قناة سابقة وتحرير الخانة فوراً 
        لتتمكن من نقل درع الحماية إلى قناة أخرى بكل مرونة.
        """
        slot_action = await SovereignLicenseManager.manage_protection_slot(license_key, "REMOVE")
        
        return {
            "status": "success",
            "message": f"🔓 **تم إلغاء الحماية بنجاح!**\n\n- تم تحرير الخانة من المجموعة: `{channel_id}`\n- {slot_action['message']}"
        }
