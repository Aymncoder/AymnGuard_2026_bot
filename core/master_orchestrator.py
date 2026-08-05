# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Master Sovereign Orchestrator (AGI Core Nexus)
المنسق السيادي المركزي (النسخة المدمجة الشاملة):
العقل المدبر الأعلى الذي يربط جميع محركات الإمبراطورية:
(الذاكرة، الوكيل العصبي، ذكاء الأسواق، السوق الشامل، أتمتة الشبكات، وتدقيق البلوكتشين).
تمت الهندسة ليعمل ككيان AGI واحد بأسلوب التوجيه اللامتزامن (Zero-Lag Routing).
"""

import logging
from typing import Dict, Any, Optional

# --- الأذرع السيادية المتقدمة (Zero-Lag Engines) ---
from core.market_engine import SovereignMarketEngine
from core.web3_nexus import SovereignWeb3Nexus

# --- محركات الإمبراطورية الأساسية ---
from core.agents.security_agent import CommunitySecurityAgent
from services.market_intelligence import MarketIntelligenceEngine
from core.universal_marketplace import UniversalMarketplaceEngine
from core.command_bridge import SovereignCommandBridge
from core.ecosystem_automation import EcosystemAutomationEngine

logger = logging.getLogger("AymnGuard.MasterOrchestrator")

class MasterSovereignOrchestrator:
    """
    المنسق المركزي الفائق (Master Sovereign Orchestrator):
    المحرك الأب المسؤول عن استقبال الطلبات وتوجيهها بدقة جراحية للذراع المختص.
    """
    def __init__(self):
        # تهيئة المحركات الأساسية القديمة (Legacy/Core)
        self.security_agent = CommunitySecurityAgent()
        self.market_engine = MarketIntelligenceEngine()
        self.marketplace = UniversalMarketplaceEngine()
        self.command_bridge = SovereignCommandBridge()
        self.automation_engine = EcosystemAutomationEngine()
        
        # تهيئة وربط الأذرع السيادية المتطورة الجديدة
        self.sovereign_market_engine = SovereignMarketEngine()
        self.web3_nexus = SovereignWeb3Nexus()
        
        logger.info("🧠 [Master Orchestrator]: تم إقلاع العقل المدبر الأعلى للإمبراطورية وتكامل كافة المحركات (السوق والبلوكتشين) بنجاح تام.")

    async def orchestrate_user_request(self, telegram_id: int, username: str, message_text: str, db_session=None) -> Dict[str, Any]:
        """
        التوجيه المركزي الذكي للطلبات:
        يتم فحص الرسالة بشكل هرمي (Hierarchical Routing)، بدءاً بالأوامر الصريحة، 
        مروراً بالكلمات المفتاحية، وصولاً إلى التحليل العصبي العام.
        """
        logger.info(f"🌐 [Orchestration Nexus]: معالجة طلب وارد من [ID: {telegram_id}] -> النص: '{message_text}'")

        response_payload = {}
        message_lower = message_text.lower().strip()

        try:
            # =========================================================
            # 1. مسار الاستخبارات المالية العميقة (أوامر التداول المباشرة)
            # =========================================================
            if message_lower.startswith("/analyze"):
                parts = message_text.split()
                symbol = parts[1].upper() if len(parts) > 1 else "BTCUSDT"
                
                logger.info(f"⚡ [Market Intelligence]: توجيه طلب التحليل الفني للزوج {symbol} إلى SovereignMarketEngine.")
                analysis = await self.sovereign_market_engine.execute_market_analysis(symbol=symbol)
                
                if "error" in analysis:
                    report_content = f"⚠️ **تنبيه من النظام المالي:** {analysis['error']}"
                else:
                    metrics = analysis['metrics']
                    report_content = (
                        f"📊 **تقرير الاستخبارات المالية | {analysis['symbol']}**\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🌐 السوق: `{analysis['market']}` | ⏱ الإطار: `{analysis['interval']}`\n\n"
                        f"💵 **السعر الحالي:** `{metrics['current_price']}`\n"
                        f"📈 **مؤشر (RSI 14):** `{metrics['RSI_14']}` ⟪{metrics['Market_Sentiment']}⟫\n"
                        f"📊 **متوسط (EMA 20):** `{metrics['EMA_20']}`\n"
                        f"🎯 **اتجاه (SAR):** `{metrics['Parabolic_SAR_Trend']}`\n\n"
                        f"⚠️ **القرار السيادي (Action Signal):**\n"
                        f"» **{analysis['action_signal']}** «"
                    )

                response_payload = {"type": "market_analysis_report", "content": report_content, "status": "success"}

            # =========================================================
            # 2. مسار تدقيق البلوكتشين والعقود الذكية (Web3)
            # =========================================================
            elif message_lower.startswith("/audit"):
                parts = message_text.split()
                if len(parts) < 2:
                    report_content = "⚠️ **تنبيه سيادي:** يرجى إرسال عنوان العقد الذكي بعد الأمر. \nمثال: `/audit 0x1234...`"
                else:
                    contract_address = parts[1]
                    logger.info(f"🛡️ [Web3 Nexus]: توجيه طلب تدقيق العقد {contract_address[:8]}...")
                    
                    audit = await self.web3_nexus.audit_smart_contract(contract_address=contract_address)
                    
                    report_content = (
                        f"🛡️ **التقرير السيادي لتدقيق العقد الذكي**\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🔗 **العنوان:** `{audit['address']}`\n"
                        f"🌐 **الشبكة:** `{audit['network']}`\n"
                        f"📦 **النوع:** `{audit['type']}`\n"
                        f"💰 **الرصيد الأصلي:** `{audit['native_balance']} (BNB/ETH)`\n"
                        f"📏 **حجم الكود الأساسي:** `{audit['bytecode_length']}`\n\n"
                        f"⚠️ **التقييم الأمني (Security Flag):**\n"
                        f"» **{audit['security_flag']}** «"
                    )

                response_payload = {"type": "web3_audit_report", "content": report_content, "status": "success"}

            # =========================================================
            # 3. مسار الاستعلامات السوقية العامة (الكلمات المفتاحية)
            # =========================================================
            elif "/market" in message_lower or "تحليل" in message_text or "سعر" in message_text:
                logger.info(f"🔍 [General Market Query]: توجيه طلب عام عبر جسر الأوامر.")
                market_reply = await self.command_bridge.process_incoming_command(str(telegram_id), message_text)
                response_payload = {"type": "market_intelligence", "content": market_reply, "status": "success"}

            # =========================================================
            # 4. مسار الأسواق الشاملة (Universal Marketplace)
            # =========================================================
            elif "/marketplaces" in message_lower or "سوق" in message_text or "شراء" in message_text:
                logger.info(f"🛍️ [Universal Marketplace]: العميل يستعرض سوق الإمبراطورية.")
                assets = await self.marketplace.list_available_assets()
                response_payload = {
                    "type": "universal_marketplace",
                    "assets": assets,
                    "content": "💎 إليك الأصول والخدمات المتاحة حالياً في سوق الإمبراطورية السيادي بلمسة زر واحدة.",
                    "status": "success"
                }

            # =========================================================
            # 5. مسار الوكيل العصبي للأمان (Fallback & Natural Language)
            # =========================================================
            else:
                logger.info(f"🧠 [Neural Routing]: توجيه النص للمحرك العصبي لفهم النوايا.")
                neural_reply = await self.security_agent.analyze_user_behavior(
                    telegram_id=telegram_id,
                    username=username,
                    message_text=message_text,
                    db_session=db_session
                )
                response_payload = {"type": "neural_support_agent", "content": neural_reply, "status": "success"}

            logger.info(f"✅ [Orchestration Success]: تمت هندسة الاستجابة السيادية بنجاح للعميل [ID: {telegram_id}].")
            return response_payload

        except Exception as e:
            logger.error(f"❌ [Orchestrator Error]: فشل حرج في تنسيق الطلب للعميل {telegram_id}: {e}", exc_info=True)
            return {
                "type": "error",
                "content": "⚠️ **تنبيه طوارئ:** عذراً يا طود الإمبراطورية، حدث استثناء طارئ في العقل المركزي. يتم الآن تفعيل المعالجة الآلية البديلة...",
                "status": "failed",
                "error": str(e)
            }
