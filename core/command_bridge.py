# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Command & Market Bridge
جسر الأوامر والأسواق السيادي: يربط طلبات المستخدمين مع محرك ذكاء الأسواق والمحرك العصبي لتوليد تقارير مالية وتفاعلية فورية
"""

import logging
import traceback
from typing import Optional
from services.market_intelligence import MarketIntelligenceEngine
from core.neural_core import AdaptiveNeuralCore

logger = logging.getLogger("AymnGuard.CommandBridge")

class SovereignCommandBridge:
    """
    جسر توجيه الأوامر والتحليل المالي السيادي
    """
    def __init__(self):
        # تهيئة المحركات الأساسية
        self.market_engine = MarketIntelligenceEngine()
        self.neural_core = AdaptiveNeuralCore()
        logger.info("🌉 [Command Bridge]: تم إقلاع جسر الأوامر والأسواق السيادي بنجاح.")

    async def process_incoming_command(self, user_id: str, command_text: str) -> str:
        """
        معالجة الأوامر الواردة (التحليل المالي أو الاستفسارات العامة) مع درع ضد الانهيار
        """
        clean_text = command_text.strip()
        if not clean_text:
            return "🛡️ يرجى إرسال أمر أو استفسار صحيح."

        try:
            # ==========================================
            # 1. نظام التوجيه المالي (Market Routing)
            # ==========================================
            if clean_text.lower().startswith("/market") or "تحليل" in clean_text:
                symbol = "BTCUSDT"  # القيمة الافتراضية
                parts = clean_text.split()
                
                # استخراج ذكي وآمن لرمز العملة
                if len(parts) > 1:
                    # أخذ الكلمة الثانية وتجاهل الكلمات مثل "تحليل"
                    target_word = parts[1].upper()
                    if target_word not in ["تحليل", "/MARKET"]:
                        symbol = target_word
                        # درع حماية لتجنب إضافة USDT لعملات تحتوي على أزواج معروفة
                        known_pairs = ["USDT", "BUSD", "BTC", "ETH", "BNB", "USDC"]
                        if not any(symbol.endswith(pair) for pair in known_pairs):
                            symbol += "USDT"

                logger.info(f"📈 [Bridge Market Request]: بدء تحليل السوق للرمز {symbol} للعميل {user_id}")
                
                # استدعاء محرك التداول
                market_report = await self.market_engine.evaluate_market_condition(symbol)
                
                if market_report and market_report.get("status") == "success":
                    summary = market_report.get("summary", "لا توجد بيانات تفصيلية.")
                    rsi_status = market_report.get("rsi_status", "غير متوفر")
                    
                    response = (
                        f"📊 **التقرير المالي السيادي** 📊\n\n"
                        f"🔹 **الرمز:** `{symbol}`\n"
                        f"📝 **الملخص:**\n{summary}\n\n"
                        f"💡 **التوجيه الفني (RSI):** {rsi_status}\n\n"
                        f"🛡️ *AymnGuard Enterprise v5.0 Market Intelligence*"
                    )
                    return response
                else:
                    logger.warning(f"⚠️ [Market Engine]: تعذر جلب بيانات {symbol}.")
                    return f"❌ عذراً، لم أتمكن من جلب بيانات السوق الحية للرمز `{symbol}` حالياً. تأكد من صحة الرمز (مثال: /market SOL)."

            # ==========================================
            # 2. التوجيه إلى المحرك العصبي (Neural AI)
            # ==========================================
            else:
                logger.info(f"🧠 [Bridge Neural Request]: توجيه طلب المستخدم {user_id} للمحرك العصبي.")
                neural_reply = await self.neural_core.synthesize_adaptive_response(user_id, clean_text)
                return neural_reply if neural_reply else "🛡️ عذراً، المحرك العصبي يعيد ضبط نفسه للرد عليك بشكل أفضل."

        except Exception as e:
            # الدرع الفولاذي: يمنع توقف البوت تماماً ويرسل تنبيه للمستخدم
            logger.error(f"❌ [Command Bridge Error]: فشل في معالجة الأمر للمستخدم {user_id}: {e}")
            logger.debug(traceback.format_exc())
            return "⚠️ حدث خطأ داخلي عابر في جسر الأوامر السيادي. تم تحويل الخطأ للصيانة التلقائية."
