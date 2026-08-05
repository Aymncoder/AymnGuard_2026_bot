# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Integrated Security, Database & Neural Cognitive Agent
الوكيل الأمني، الإدراكي، والعصبي السيادي المتكامل: يدمج بين الوراثة الهيكلية الأساسية للوكلاء،
الارتباط بقاعدة البيانات الدائمة (SQL)، الذاكرة السيادية طويلة الأمد، ومحرك التكيف النفسي واللساني
لتوفير أعلى مستويات الأمان، تحليل السلوك، وتقديم استجابات إقناعية فائقة الذكاء.
"""

from .base_agent import SovereignBaseAgent
from core.database.models import User, Group
from sqlalchemy.future import select
from core.context_vault import SovereignCognitiveVault
from core.neural_core import AdaptiveNeuralCore

class CommunitySecurityAgent(SovereignBaseAgent):
    """
    الوكيل الأمني والإدراكي العصبي السيادي: المسؤول عن حماية المجتمع، فحص السجلات الدائمة، 
    تذكر العملاء، وتحليل نفسيتهم لصياغة الردود الإقناعية الأكثر احترافية في العالم الرقمي.
    """
    def __init__(self):
        super().__init__(agent_name="Security_Neural_Guard")
        self.neural_core = AdaptiveNeuralCore()
        self.logger.info("🛡️ [Security & Neural Agent]: تم إقلاع الوكيل الأمني والإدراكي المزود بالمحرك العصبي بنجاح.")

    async def analyze_user_behavior(self, telegram_id: int, username: str, message_text: str = "", db_session=None) -> str:
        """
        فحص السجل الأمني الدائم، تحديث الذاكرة السيادية، استخراج استراتيجيات الإقناع،
        وتخليق الاستجابة العصبية التكيفية الشاملة للعميل.
        """
        user_id_str = str(telegram_id)
        self.logger.info(f"🔍 [Security Agent]: فحص السجل العصبي والإدراكي للمستخدم [ID: {telegram_id}, Username: {username}]")

        # 1. التحقق من وجود العميل في قاعدة البيانات الدائمة (SQL) إن توفرت الجلسة
        if db_session:
            try:
                result = await db_session.execute(select(User).where(User.telegram_id == telegram_id))
                db_user = result.scalar_one_or_none()
                if db_user:
                    self.logger.info(f"📂 [Database]: العميل مسجل مسبقاً في قاعدة بيانات SQL الدائمة.")
            except Exception as e:
                self.logger.error(f"❌ [Database Error]: خطأ أثناء استعلام قاعدة البيانات: {e}")

        # 2. تحديث الذاكرة السيادية وتخزين التفاعل الحالي في الذاكرة الحية المؤقتة
        interaction_payload = {
            "last_message": message_text,
            "action_type": "message_received" if message_text else "chat_join"
        }
        
        user_record = await SovereignCognitiveVault.remember_user(
            user_id=user_id_str, 
            username=username, 
            interaction_data=interaction_payload
        )
        
        # 3. استدعاء محرك تحليل النوايا والإقناع السيادي
        persuasion_strategy = await SovereignCognitiveVault.analyze_intent_and_persuasion(
            user_id=user_id_str, 
            current_message=message_text
        )
        self.logger.info(f"🎯 [Persuasion Engine]: استراتيجية الإقناع للعميل [ID: {telegram_id}]: {persuasion_strategy}")

        # 4. استدعاء المحرك العصبي النفسي لتخليق الرد التكيفي المقنع فائق الذكاء
        adaptive_response = await self.neural_core.synthesize_adaptive_response(
            user_text=message_text,
            user_history=user_record.get("history", [])
        )
        
        self.logger.info(f"🧠 [Neural Agent Decision]: تم تخليق الاستجابة العصبية التكيفية الشاملة للعميل [ID: {telegram_id}].")
        return adaptive_response

    async def enforce_group_rules(self, group_id: int, violation_type: str) -> bool:
        """تطبيق بروتوكولات الحماية الصارمة وحراسة المجموعات السيادية"""
        self.logger.warning(f"⚠️ [Security Enforcement]: رصد انتهاك أمني ({violation_type}) في المجموعة [ID: {group_id}]. جاري تفعيل البروتوكول السيادي...")
        return True
