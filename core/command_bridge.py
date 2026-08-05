# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Command & Market Bridge
جسر الأوامر والأسواق السيادي: يربط طلبات المستخدمين (مثل الاستعلام عن العملات والأسواق)
مع محرك ذكاء الأسواق والمحرك العصبي لتوليد تقارير مالية وتفاعلية فورية.
"""

import logging
from services.market_intelligence import MarketIntelligenceEngine
from core.neural_core import AdaptiveNeuralCore

logger = logging.getLogger("AymnGuard.CommandBridge")

class SovereignCommandBridge:
    """
    جسر توجيه الأوامر والتحليل المالي السيادي.
    """
    def __init__(self):
        self.market_engine = MarketIntelligenceEngine()
        self.neural_core = AdaptiveNeuralCore()
        logger.info("🌉 [Command Bridge]: تم إقلاع جسر الأوامر والأسواق السيادي بنجاح.")

    async def process_incoming_command(self, user_id: str, command_text: str) -> str:
        """
        معالجة الأوامر الواردة (مثل التحليل المالي أو الاستفسارات):
        - إذا كان الأمر متعلقاً بالأسواق (يبدأ بـ /market أو اسم عملة)، يتم جلب التحليل الفني.
        - إذا كان استفساراً عاماً، يتم تمريره للمحرك العصبي النفسي.
        """
        clean_text = command_text.strip()
        
        # فحص ما إذا كان الأمر طلباً لتحليل سوقي أو عملة رقمية
        if clean_text.lower().startswith("/market") or "تحليل" in clean_text or "سعر" in clean_text:
            # استخراج رمز العملة افتراضياً أو من النص (مثال افتراضي BTCUSDT)
            symbol = "BTCUSDT"
            parts = clean_text.split()
            if len(parts) > 1:
                symbol = parts[1].upper()
                if not symbol.endswith("USDT"):
                    symbol += "USDT"

            logger.info(f"📈 [Bridge Market Request]: جاري جلب التحليل السيادي للعملة [{symbol}] بناءً على طلب العميل [ID: {user_id}].")
            
            # جلب التقرير المالي من محرك الذكاء السوقي
            market_report = await self.market_engine.evaluate_market_condition(symbol)
            
            if market_report.get("status") == "success":
                summary = market_report.get("summary")
                rsi_status = market_report.get("rsi_status")
                
                response = (
                    f"📊 **التقرير المالي السيادي لأسواق العملات الرقمية:**\n\n"
                    f"{summary}\n"
                    f"💡 **التوجيه الفني:** {rsi_status}\n\n"
                    f"🛡️ *تم التحليل الفوري عبر AymnGuard Enterprise v5.0 Market Intelligence.*"
                )
                return response
            else:
                return "عذراً يا طود الإمبراطورية، تعذر جلب بيانات السوق الحية لهذه العملة حالياً. تأكد من صحة الرمز المحرف."

        else:
            # توجيه الطلب للمحرك العصبي النفسي للتفاعل الإنساني العام
            neural_reply = await self.neural_core.synthesize_adaptive_response(user_text=clean_text)
            return neural_reply
