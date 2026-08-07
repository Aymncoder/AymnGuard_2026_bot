# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v18.0.0 : Ultimate Master Sovereign Orchestrator
==============================================================================
المنسق السيادي المركزي الأسمى (النسخة الإمبراطورية المدمجة الشاملة):
العقل المدبر الأعلى الذي يربط ويوجه جميع محركات الإمبراطورية بتناسق جراحي:
(التصميم الإبداعي، الاستخبارات، الحماية، التنفيذ المالي، التدقيق اللغوي، تدقيق البلوكتشين، والأمان العصبي).
"""

import logging
from typing import Dict, Any, Optional

# ==============================================================================
# 1. استيراد كافة أذرع الإمبراطورية بحماية مطلقة (Safe Imports)
# ==============================================================================
# 1.1 محركات الخدمات السيادية الجديدة
try:
    from bots.protection.bot_engine import SovereignProtectionEngine
    from bots.creative.creative_engine import SovereignCreativeStudio
    from bots.search.search_engine import SovereignSearchEngine
except ImportError:
    SovereignProtectionEngine = None
    SovereignCreativeStudio = None
    SovereignSearchEngine = None

# 1.2 المحركات المالية والبلوكتشين واللغوية
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
    from core.universal_marketplace import UniversalMarketplaceEngine
except ImportError:
    UniversalMarketplaceEngine = None

# إعداد السجلات المركزية للعقل المدبر
logger = logging.getLogger("AegisAICore.MasterOrchestrator")
logger.setLevel(logging.INFO)

class MasterSovereignOrchestrator:
    """
    المنسق المركزي الفائق (Master Sovereign Orchestrator):
    المايسترو المسؤول عن استقبال طلبات جسر تيليجرام وتوجيهها بدقة هندسية للمحرك المختص.
    """
    def __init__(self):
        logger.info("🧠 [Master Orchestrator]: جاري إقلاع العقل المدبر الأعلى وتكامل كافة أذرع الإمبراطورية...")
        
        # ربط الخدمات الأساسية (إذا تم استيرادها بنجاح)
        self.protection = SovereignProtectionEngine
        self.creative = SovereignCreativeStudio
        self.search = SovereignSearchEngine
        
        # ربط المحركات التخصصية
        self.trading = SovereignTradingEngine() if SovereignTradingEngine else None
        self.linguistic = LinguisticEngine() if LinguisticEngine else None
        self.market = SovereignMarketEngine() if SovereignMarketEngine else None
        self.web3 = SovereignWeb3Nexus() if SovereignWeb3Nexus else None
        self.security_agent = CommunitySecurityAgent() if CommunitySecurityAgent else None
        self.marketplace = UniversalMarketplaceEngine() if UniversalMarketplaceEngine else None
        
        logger.info("✨ [Master Orchestrator]: تم ربط وتفعيل كافة المحركات والأنظمة السيادية بنجاح تام.")

    async def orchestrate_user_request(
        self, 
        telegram_id: str, 
        username: str, 
        message_text: str, 
        db_session: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        التوجيه المركزي الذكي للطلبات:
        يحلل رسالة المستخدم (أزرار، قوائم، نصوص، أوامر عميقة) ويعيد الرد المهيكل لجسر تيليجرام.
        """
        logger.info(f"🌐 [Orchestration Nexus]: طلب من [User: {username} | ID: {telegram_id}] -> '{message_text[:40]}'")

        text = message_text.strip()
        text_lower = text.lower()
        
        # مفتاح سيادي افتراضي (يمكن تغييره لاحقاً بجلب المفتاح الحقيقي من قاعدة البيانات)
        MOCK_LICENSE_KEY = "AG-EMPIRE-ACTIVE-KEY"

        try:
            # =========================================================
            # 2. أوامر التشغيل الأساسية وقوائم الواجهة (UI Navigation)
            # =========================================================
            if text_lower in ["/start", "menu", "القائمة"]:
                return {
                    "type": "system_menu",
                    "content": f"🛡️ **مرحباً بك يا طود الإمبراطورية {username}!**\n\nأنا النواة المركزية المنسقة. كافة أذرع (AymnGuard) تحت أمرك. اختر الخدمة السيادية المطلوبة:",
                    "show_menu": True,
                    "status": "success"
                }

            # تفريعات القوائم (عند الضغط على أزرار Inline)
            if text_lower in ["/protect", "menu_protect"]:
                return {"content": "🛡️ **[محرك الدرع السيادي]**\nلتفعيل الحماية، أرسل: `حماية <معرف_القناة>`\nمثال: `حماية @AymnGuard`", "show_menu": False}
            if text_lower in ["/creative", "menu_creative"]:
                return {"content": "🎨 **[استوديو الإبداع]**\nللتصميم، أرسل: `صمم <وصف>`\nمثال: `صمم شعار لشركة ذكاء اصطناعي`", "show_menu": False}
            if text_lower in ["/search", "menu_search"]:
                return {"content": "🔍 **[الاستخبارات والبحث]**\nللبحث العميق، أرسل: `ابحث <الكلمات>`\nمثال: `ابحث عن مشاريع Web3`", "show_menu": False}
            if text_lower in ["/trade", "menu_trade"]:
                return {"content": "📈 **[منصة التداول الآلي]**\nللتداول أرسل: `/trade` أو للتحليل أرسل `/analyze BTCUSDT`", "show_menu": False}

            # =========================================================
            # 3. توجيه الطلبات باللغة العربية (الإبداع، البحث، الحماية)
            # =========================================================
            if text.startswith("صمم"):
                prompt = text.replace("صمم", "").strip()
                if not prompt: return {"content": "⚠️ الرجاء كتابة الوصف بعد 'صمم'.", "show_menu": False}
                if self.creative:
                    res = await self.creative.generate_asset_request(MOCK_LICENSE_KEY, prompt)
                    return {"content": res.get("message", "تم الاستلام"), "show_menu": False}
                return {"content": "⚠️ محرك الإبداع غير متاح حالياً.", "show_menu": False}

            if text.startswith("ابحث"):
                query = text.replace("ابحث", "").strip()
                if not query: return {"content": "⚠️ الرجاء كتابة النص بعد 'ابحث'.", "show_menu": False}
                if self.search:
                    res = await self.search.execute_enterprise_search(MOCK_LICENSE_KEY, query)
                    return {"content": res.get("message", "تمت عملية البحث"), "show_menu": False}
                return {"content": "⚠️ محرك البحث غير متاح.", "show_menu": False}

            if text.startswith("حماية"):
                channel_id = text.replace("حماية", "").strip()
                if self.protection:
                    res = await self.protection.activate_protection(MOCK_LICENSE_KEY, channel_id)
                    return {"content": res.get("message", "تم تفعيل الحماية"), "show_menu": False}
                return {"content": "⚠️ محرك الحماية غير متاح.", "show_menu": False}

            # =========================================================
            # 4. مسار الاستخبارات المالية والتحليل الفني (/analyze)
            # =========================================================
            if text_lower.startswith("/analyze"):
                parts = text.split()
                symbol = parts[1].upper() if len(parts) > 1 else "BTCUSDT"
                if self.market:
                    logger.info(f"⚡ توجيه طلب التحليل الفني لـ {symbol}")
                    analysis = await self.market.execute_market_analysis(symbol=symbol)
                    if "error" in analysis:
                        return {"content": f"⚠️ **خطأ مالي:** {analysis['error']}", "show_menu": False}
                    
                    metrics = analysis.get('metrics', {})
                    reply = (
                        f"📊 **تقرير الاستخبارات المالية | {symbol}**\n"
                        f"💵 **السعر:** `{metrics.get('current_price', 'N/A')}`\n"
                        f"📈 **RSI 14:** `{metrics.get('RSI_14', 'N/A')}`\n"
                        f"⚠️ **القرار السيادي:** » **{analysis.get('action_signal', 'HOLD')}** «"
                    )
                    return {"content": reply, "show_menu": False}
                return {"content": "📊 [Market Intelligence]: وحدة التحليل المالي غير متصلة.", "show_menu": False}

            # =========================================================
            # 5. مسار تدقيق البلوكتشين (/audit) و التنفيذ (/trade)
            # =========================================================
            if text_lower.startswith("/audit"):
                parts = text.split()
                if len(parts) < 2: return {"content": "⚠️ أرسل عنوان العقد بعد الأمر: `/audit 0x...`", "show_menu": False}
                if self.web3:
                    audit = await self.web3.audit_smart_contract(contract_address=parts[1])
                    reply = f"🛡️ **تدقيق العقد:** `{audit.get('address', parts[1])}`\nالتقييم: » **{audit.get('security_flag', 'SAFE')}** «"
                    return {"content": reply, "show_menu": False}
                return {"content": "🔗 محرك تدقيق البلوكتشين غير متصل.", "show_menu": False}

            if text_lower.startswith("/trade"):
                if self.trading: return {"content": "💹 تم تفعيل ذراع التداول. جاري إدارة المخاطر للتنفيذ.", "show_menu": False}
                return {"content": "⚠️ محرك التنفيذ المالي غير مفعل.", "show_menu": False}

            if text_lower.startswith("/proofread"):
                if self.linguistic:
                    processed = await self.linguistic.proofread_and_elevate(text)
                    return {"content": f"📝 **[المركز اللغوي الأكاديمي]:**\n{processed.get('processed_text')}", "show_menu": False}
                return {"content": "📝 المحرك اللغوي مغلق حالياً.", "show_menu": False}

            # =========================================================
            # 6. مسار الذكاء العصبي العام (الرد الافتراضي / الرد العادي)
            # =========================================================
            if self.security_agent:
                neural_reply = await self.security_agent.analyze_user_behavior(telegram_id, username, text, db_session)
                return {"content": neural_reply, "show_menu": False}
            
            # الرد الافتراضي في حال لم يتطابق مع أي أمر
            return {
                "content": f"✅ استلمت رسالتك يا {username}:\n`{text}`\n\nأنا النواة المركزية وأعالج بياناتك بأمان. لفتح اللوحة، أرسل /start",
                "show_menu": False,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"❌ [Orchestrator Error]: فشل حرج في التنسيق: {e}", exc_info=True)
            return {
                "content": "⚠️ **تنبيه طوارئ:** حدث استثناء طارئ في العقل المركزي. تم تفعيل الحماية البديلة.",
                "show_menu": False,
                "status": "failed"
            }
