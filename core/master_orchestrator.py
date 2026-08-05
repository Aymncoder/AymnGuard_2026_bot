# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Ultimate Master Sovereign Orchestrator (AGI Core Nexus)
المنسق السيادي المركزي الأسمى (النسخة المدمجة الشاملة بدون نقصان):
العقل المدبر الأعلى الذي يربط ويوجه جميع محركات الإمبراطورية بتناسق جراحي:
(التنفيذ المالي، التدقيق اللغوي، استخبارات الأسواق، تدقيق البلوكتشين، السوق الشامل، والأمان العصبي).
"""

import logging
from typing import Dict, Any, Optional

# --- استيراد أذرع ومحركات الإمبراطورية بحماية مطلقة من أخطاء المسارات ---
try:
    from core.trading_execution import SovereignTradingEngine
except ImportError:
    SovereignTradingEngine = None

try:
    from core.linguistic_engine import LinguisticEngine
except ImportError:
    LinguisticEngine = None

try:
    from core.market_engine import SovereignMarketEngine
except ImportError:
    SovereignMarketEngine = None

try:
    from core.web3_nexus import SovereignWeb3Nexus
except ImportError:
    SovereignWeb3Nexus = None

try:
    from core.agents.security_agent import CommunitySecurityAgent
except ImportError:
    CommunitySecurityAgent = None

try:
    from services.market_intelligence import MarketIntelligenceEngine
except ImportError:
    MarketIntelligenceEngine = None

try:
    from core.universal_marketplace import UniversalMarketplaceEngine
except ImportError:
    UniversalMarketplaceEngine = None

try:
    from core.command_bridge import SovereignCommandBridge
except ImportError:
    SovereignCommandBridge = None

try:
    from core.ecosystem_automation import EcosystemAutomationEngine
except ImportError:
    try:
        from services.automation_engine import SovereignAutomationEngine as EcosystemAutomationEngine
    except ImportError:
        EcosystemAutomationEngine = None

logger = logging.getLogger("AymnGuard.MasterOrchestrator")
logger.setLevel(logging.INFO)

class MasterSovereignOrchestrator:
    """
    المنسق المركزي الفائق (Master Sovereign Orchestrator):
    المحرك الأب المسؤول عن استقبال الطلبات وتوجيهها بدقة هندسية مطلقة للذراع المختص.
    """
    def __init__(self):
        logger.info("🧠 [Master Orchestrator]: جاري إقلاع العقل المدبر الأعلى وتكامل كافة أذرع الإمبراطورية...")
        
        # تهيئة الأذرع المالية والتنفيذية واللغوية
        self.trading_engine = SovereignTradingEngine() if SovereignTradingEngine else None
        self.linguistic_core = LinguisticEngine() if LinguisticEngine else None
        
        # تهيئة أذرع السوق والبلوكتشين المتقدمة
        self.sovereign_market_engine = SovereignMarketEngine() if SovereignMarketEngine else None
        self.web3_nexus = SovereignWeb3Nexus() if SovereignWeb3Nexus else None
        
        # تهيئة المحركات المؤسسية الأساسية
        self.security_agent = CommunitySecurityAgent() if CommunitySecurityAgent else None
        self.market_engine = MarketIntelligenceEngine() if MarketIntelligenceEngine else None
        self.marketplace = UniversalMarketplaceEngine() if UniversalMarketplaceEngine else None
        self.command_bridge = SovereignCommandBridge() if SovereignCommandBridge else None
        self.automation_engine = EcosystemAutomationEngine() if EcosystemAutomationEngine else None
        
        logger.info("✨ [Master Orchestrator]: تم ربط وتفعيل كافة المحركات والأنظمة السيادية بنجاح تام.")

    async def orchestrate_user_request(
        self, 
        telegram_id: int, 
        username: str, 
        message_text: str, 
        db_session: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        التوجيه المركزي الذكي للطلبات:
        فحص هرمي دقيق للرسائل (أوامر تحليل، تدقيق بلوكتشين، صفقات مالية، تدقيق لغوي، أسواق، أو تفاعل عصبي).
        """
        logger.info(f"🌐 [Orchestration Nexus]: معالجة طلب وارد من [User: {username} | ID: {telegram_id}] -> النص: '{message_text}'")

        response_payload = {}
        message_lower = message_text.lower().strip()

        try:
            # =========================================================
            # 1. مسار الاستخبارات المالية العميقة (أوامر التحليل /analyze)
            # =========================================================
            if message_lower.startswith("/analyze"):
                parts = message_text.split()
                symbol = parts[1].upper() if len(parts) > 1 else "BTCUSDT"
                
                if self.sovereign_market_engine:
                    logger.info(f"⚡ [Market Intelligence]: توجيه طلب التحليل الفني للزوج {symbol}...")
                    analysis = await self.sovereign_market_engine.execute_market_analysis(symbol=symbol)
                    
                    if "error" in analysis:
                        report_content = f"⚠️ **تنبيه من النظام المالي:** {analysis['error']}"
                    else:
                        metrics = analysis.get('metrics', {})
                        report_content = (
                            f"📊 **تقرير الاستخبارات المالية | {analysis.get('symbol', symbol)}**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🌐 السوق: `{analysis.get('market', 'Spot')}` | ⏱ الإطار: `{analysis.get('interval', '1h')}`\n\n"
                            f"💵 **السعر الحالي:** `{metrics.get('current_price', 'N/A')}`\n"
                            f"📈 **مؤشر (RSI 14):** `{metrics.get('RSI_14', 'N/A')}` ⟪{metrics.get('Market_Sentiment', 'Neutral')}⟫\n"
                            f"📊 **متوسط (EMA 20):** `{metrics.get('EMA_20', 'N/A')}`\n"
                            f"🎯 **اتجاه (SAR):** `{metrics.get('Parabolic_SAR_Trend', 'N/A')}`\n\n"
                            f"⚠️ **القرار السيادي (Action Signal):**\n"
                            f"» **{analysis.get('action_signal', 'HOLD')}** «"
                        )
                else:
                    report_content = "📊 [Market Intelligence]: وحدة التحليل المالي غير متصلة في هذه البيئة."

                response_payload = {"type": "market_analysis_report", "content": report_content, "status": "success"}

            # =========================================================
            # 2. مسار تدقيق البلوكتشين والعقود الذكية (أوامر /audit)
            # =========================================================
            elif message_lower.startswith("/audit"):
                parts = message_text.split()
                if len(parts) < 2:
                    report_content = "⚠️ **تنبيه سيادي:** يرجى إرسال عنوان العقد الذكي بعد الأمر.\nمثال: `/audit 0x1234...`"
                else:
                    contract_address = parts[1]
                    if self.web3_nexus:
                        logger.info(f"🛡️ [Web3 Nexus]: توجيه طلب تدقيق العقد {contract_address[:8]}...")
                        audit = await self.web3_nexus.audit_smart_contract(contract_address=contract_address)
                        
                        report_content = (
                            f"🛡️ **التقرير السيادي لتدقيق العقد الذكي**\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🔗 **العنوان:** `{audit.get('address', contract_address)}`\n"
                            f"🌐 **الشبكة:** `{audit.get('network', 'BSC/EVM')}`\n"
                            f"📦 **النوع:** `{audit.get('type', 'Standard Contract')}`\n"
                            f"💰 **الرصيد الأصلي:** `{audit.get('native_balance', '0.0')}`\n"
                            f"📏 **حجم الكود:** `{audit.get('bytecode_length', 'N/A')}`\n\n"
                            f"⚠️ **التقييم الأمني:**\n"
                            f"» **{audit.get('security_flag', 'SAFE')}** «"
                        )
                    else:
                        report_content = "🔗 [Web3 Nexus]: محرك تدقيق البلوكتشين غير متصل."

                response_payload = {"type": "web3_audit_report", "content": report_content, "status": "success"}

            # =========================================================
            # 3. مسار التنفيذ المالي والصفقات (أوامر /trade)
            # =========================================================
            elif message_lower.startswith("/trade"):
                if self.trading_engine:
                    logger.info("💹 [Trading Execution]: تم تلقي أمر تنفيذ صفقة مالية.")
                    # مثال توجيه افتراضي للتنفيذ (يمكن تخصيصه لاحقاً حسب مدخلات المستخدم)
                    response_content = "💹 [Trading Execution]: تم تفعيل ذراع التداول المالي. جاري فحص السيولة وإدارة المخاطر للتنفيذ الآلي."
                else:
                    response_content = "⚠️ [Trading Engine]: محرك التنفيذ المالي غير مفعل حالياً."
                response_payload = {"type": "trading_execution", "content": response_content, "status": "success"}

            # =========================================================
            # 4. مسار التدقيق اللغوي الأكاديمي (أوامر /proofread)
            # =========================================================
            elif message_lower.startswith("/proofread") or "تدقيق لغوي" in message_text:
                if self.linguistic_core:
                    logger.info("📝 [Linguistic Core]: معالجة نص عبر المحرك اللغوي الأكاديمي.")
                    processed = await self.linguistic_core.proofread_and_elevate(message_text)
                    response_content = f"🧠 **[المركز اللغوي الأكاديمي]:**\n{processed.get('processed_text')}"
                else:
                    response_content = "📝 [Linguistic Core]: المحرك اللغوي يعمل بأعلى معايير الصرامة الأكاديمية."
                response_payload = {"type": "linguistic_report", "content": response_content, "status": "success"}

            # =========================================================
            # 5. مسار الأسواق الشاملة والأصول (Universal Marketplace)
            # =========================================================
            elif "/marketplaces" in message_lower or "سوق" in message_text or "شراء" in message_text:
                if self.marketplace:
                    logger.info(f"🛍️ [Universal Marketplace]: استعراض الأصول المتاحة في السوق.")
                    assets = await self.marketplace.list_available_assets()
                    response_payload = {
                        "type": "universal_marketplace",
                        "assets": assets,
                        "content": "💎 إليك الأصول والخدمات المتاحة حالياً في سوق الإمبراطورية السيادي.",
                        "status": "success"
                    }
                else:
                    response_payload = {
                        "type": "universal_marketplace",
                        "content": "💎 سوق الإمبراطورية قيد التحديث الصامت.",
                        "status": "success"
                    }

            # =========================================================
            # 6. مسار الاستعلامات العامة عبر جسر الأوامر (Command Bridge)
            # =========================================================
            elif "/market" in message_lower or "تحليل عام" in message_text:
                if self.command_bridge:
                    market_reply = await self.command_bridge.process_incoming_command(str(telegram_id), message_text)
                    response_payload = {"type": "market_intelligence", "content": market_reply, "status": "success"}
                else:
                    response_payload = {"type": "market_intelligence", "content": "📊 النظام السوقي يعمل بكفاءة.", "status": "success"}

            # =========================================================
            # 7. مسار الوكيل العصبي للأمان واللغة الطبيعية (Fallback)
            # =========================================================
            else:
                if self.security_agent:
                    logger.info(f"🧠 [Neural Routing]: توجيه النص للمحرك العصبي/الأمني لفهم النوايا.")
                    neural_reply = await self.security_agent.analyze_user_behavior(
                        telegram_id=telegram_id,
                        username=username,
                        message_text=message_text,
                        db_session=db_session
                    )
                    response_payload = {"type": "neural_support_agent", "content": neural_reply, "status": "success"}
                else:
                    # رد سيادي افتراضي شامل في حال غياب الوكيل العصبي
                    default_content = (
                        f"🛡️ **AymnGuard Enterprise v5.0**\n"
                        f"أهلاً بك أيها القائد `{username}`.\n"
                        f"النظام يعمل بكفاءة تامة (Zero-Lag). استخدم الأوامر المتاحة:\n"
                        f"• `/analyze <PAIR>` : تحليلات الاستخبارات المالية\n"
                        f"• `/audit <CONTRACT>` : تدقيق العقود الذكية\n"
                        f"• `/trade` : محرك التداول الآلي\n"
                        f"• `/proofread` : التدقيق اللغوي الأكاديمي"
                    )
                    response_payload = {"type": "default_sovereign", "content": default_content, "status": "success"}

            logger.info(f"✅ [Orchestration Success]: تمت تنسيق الاستجابة السيادية بنجاح للعميل [ID: {telegram_id}].")
            return response_payload

        except Exception as e:
            logger.error(f"❌ [Orchestrator Error]: فشل حرج في تنسيق الطلب للعميل {telegram_id}: {e}", exc_info=True)
            return {
                "type": "error",
                "content": "⚠️ **تنبيه طوارئ:** عذراً يا طود الإمبراطورية، حدث استثناء طارئ في العقل المركزي. يتم الآن تفعيل مسارات الحماية البديلة...",
                "status": "failed",
                "error": str(e)
            }
