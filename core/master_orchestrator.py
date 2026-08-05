# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Master Sovereign Orchestrator (AGI Core Nexus)
المنسق السيادي المركزي: العقل المدبر الأعلى الذي يربط جميع محركات الإمبراطورية
(الذاكرة، الوكيل العصبي، ذكاء الأسواق، السوق الشامل، وأتمتة الشبكات) لتعمل بتناغم ككيان AGI واحد.
"""

import logging
from typing import Dict, Any, Optional
from core.market_engine import SovereignMarketEngine

from core.agents.security_agent import CommunitySecurityAgent
from services.market_intelligence import MarketIntelligenceEngine
from core.universal_marketplace import UniversalMarketplaceEngine
from core.command_bridge import SovereignCommandBridge
from core.ecosystem_automation import EcosystemAutomationEngine

logger = logging.getLogger("AymnGuard.MasterOrchestrator")

class MasterSovereignOrchestrator:
    """
    المنسق المركزي الفائق (Master Sovereign Orchestrator):
    المحرك الأب المسؤول عن توجيه تدفقات البيانات والطلبات بين كافة أنظمة الإمبراطورية أوتوماتيكياً.
    """
    def __init__(self):
        self.security_agent = CommunitySecurityAgent()
        self.market_engine = MarketIntelligenceEngine()
        self.marketplace = UniversalMarketplaceEngine()
        self.command_bridge = SovereignCommandBridge()
        self.automation_engine = EcosystemAutomationEngine()
        
        logger.info("🧠 [Master Orchestrator]: تم إقلاع العقل المدبر الأعلى للإمبراطورية وتكامل كافة المحركات بنجاح تام.")

    async def orchestrate_user_request(self, telegram_id: int, username: str, message_text: str, db_session=None) -> Dict[str, Any]:
        """
        التوجيه المركزي الذكي للطلبات:
        يستقبل رسالة المستخدم، يحلل ماهيتها عبر الوكيل العصبي والجسر، ويوجهها للمحرك المختص فوراً.
        """
        logger.info(f"🌐 [Orchestration Nexus]: معالجة طلب وارد من المستخدم [ID: {telegram_id}] -> النص: '{message_text}'")

        response_payload = {}

        try:
            # 1. إذا كان الطلب استعلاماً سوقياً أو مالياً
            if "/market" in message_text.lower() or "تحليل" in message_text or "سعر" in message_text:
                market_reply = await self.command_bridge.process_incoming_command(str(telegram_id), message_text)
                response_payload = {
                    "type": "market_intelligence",
                    "content": market_reply,
                    "status": "success"
                }

            # 2. إذا كان الطلب تصفحاً للسوق أو اقتناء أصل رقمي
            elif "/marketplaces" in message_text.lower() or "سوق" in message_text or "شراء" in message_text:
                assets = await self.marketplace.list_available_assets()
                response_payload = {
                    "type": "universal_marketplace",
                    "assets": assets,
                    "content": "إليك الأصول والخدمات المتاحة حالياً في سوق الإمبراطورية السيادي بلمسة زر واحدة.",
                    "status": "success"
                }

            # 3. الطلبات العامة والتفاعلية (يتم تمريرها للوكيل العصبي والذاكرة السيادية)
            else:
                neural_reply = await self.security_agent.analyze_user_behavior(
                    telegram_id=telegram_id,
                    username=username,
                    message_text=message_text,
                    db_session=db_session
                )
                response_payload = {
                    "type": "neural_support_agent",
                    "content": neural_reply,
                    "status": "success"
                }

            logger.info(f"⚡ [Orchestration Success]: تمت هندسة الاستجابة السيادية بنجاح للعميل [ID: {telegram_id}].")
            return response_payload

        except Exception as e:
            logger.error(f"❌ [Orchestrator Error]: فشل في تنسيق الطلب للعميل {telegram_id}: {e}")
            return {
                "type": "error",
                "content": "عذراً يا طود الإمبراطورية، حدث استثناء طارئ في العقل المركزي. جاري المعالجة الآلية...",
                "status": "failed",
                "error": str(e)
            }
