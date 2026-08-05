# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Community Security & Cognitive Agent
الوكيل الأمني والإدراكي السيادي: يدمج بين الوراثة الهيكلية الأساسية للوكلاء، 
الارتباط بقاعدة البيانات، والذاكرة السيادية طويلة الأمد لإدارة وتحليل سلوك العملاء باحترافية مطلقة.
"""

from .base_agent import SovereignBaseAgent
from core.database.models import User, Group
from sqlalchemy.future import select
from core.context_vault import SovereignCognitiveVault

class CommunitySecurityAgent(SovereignBaseAgent):
    """
    الوكيل الأمني والإدراكي السيادي: المسؤول عن حماية المجتمع، فحص السجلات، 
    وتفعيل محرك الإقناع الذكي المتطور بناءً على الذاكرة طويلة الأمد.
    """
    def __init__(self):
        super().__init__(agent_name="Security_Guard")
        self.logger.info("🛡️ [Security & Cognitive Agent]: تم إقلاع الوكيل الأمني والإدراكي بنجاح وتفعيل الارتباط السيادي.")

    async def analyze_user_behavior(self, telegram_id: int, username: str, message_text: str = "", db_session=None) -> str:
        """
        فحص السلوك وتحليل النوايا الشامل:
        1. فحص سجل الموثوقية وقاعدة البيانات المؤسسية.
        2. تحديث الذاكرة السيادية طويلة الأمد وتخزين تاريخ التفاعلات.
        3. تشغيل محرك تحليل النوايا واستخراج استراتيجية الإقناع السيادية للتفوق في خدمة العملاء.
        """
        user_id_str = str(telegram_id)
        self.logger.info(f"🔍 [Security Agent]: فحص السجل الأمني والإدراكي للمستخدم [ID: {telegram_id}, Username: {username}]")

        # (اختياري مستقبلي): فحص الوجود في قاعدة البيانات SQL الدائمة عبر db_session إن وجد
        if db_session:
            try:
                result = await db_session.execute(select(User).where(User.telegram_id == telegram_id))
                db_user = result.scalar_one_or_none()
                if db_user:
                    self.logger.info(f"📂 [Database]: العميل مسجل مسبقاً في قاعدة بيانات SQL الدائمة.")
            except Exception as e:
                self.logger.error(f"❌ [Database Error]: خطأ أثناء استعلام قاعدة البيانات: {e}")

        # 1. تحديث الذاكرة السيادية وتخزين التفاعل الحالي في الذاكرة الحية المؤقتة
        interaction_payload = {
            "last_message": message_text,
            "action_type": "message_received" if message_text else "chat_join"
        }
        
        user_record = await SovereignCognitiveVault.remember_user(
            user_id=user_id_str, 
            username=username, 
            interaction_data=interaction_payload
        )
        
        # 2. استدعاء محرك تحليل النوايا والإقناع المتقدم
        persuasion_strategy = await SovereignCognitiveVault.analyze_intent_and_persuasion(
            user_id=user_id_str, 
            current_message=message_text
        )
        
        self.logger.info(f"🧠 [Agent Decision]: تم تقييم العميل [ID: {telegram_id}]. الاستراتيجية المقترحة: {persuasion_strategy}")
        
        # بناء التوجيه أو الاستجابة السيادية الشاملة
        return f"مرحباً بك مجدداً يا طود الإمبراطورية. التوجيه الحالي للعميل: {persuasion_strategy}"

    async def enforce_group_rules(self, group_id: int, violation_type: str) -> bool:
        """
        تطبيق بروتوكولات الحماية الصارمة على المجموعة وإدارة أمن الإمبراطورية بكفاءة عالية.
        """
        self.logger.warning(f"⚠️ [Security Enforcement]: تم رصد انتهاك أمني ({violation_type}) في المجموعة [ID: {group_id}]. جاري تفعيل البروتوكول السيادي...")
        # سيتم إضافة منطق التدخل السريع، الحظر، أو الإنذار الموجه هنا
        return True
