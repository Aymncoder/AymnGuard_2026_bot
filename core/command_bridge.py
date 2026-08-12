# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Sovereign Command & Market Bridge (Cloud Optimized)
==============================================================================
جسر الأوامر والأسواق السيادي: يربط طلبات المستخدمين مع محرك ذكاء الأسواق والمحرك العصبي
لتوليد تقارير مالية وتفاعلية فورية.
تم تطهيره بالكامل من الرموز التعبيرية لضمان الاستقرار المطلق في بيئة الإنتاج السحابية.
==============================================================================
"""

import logging
import traceback
from typing import Optional
from core.market_engine import SovereignMarketEngine
from core.neural_core import AdaptiveNeuralCore

logger = logging.getLogger("AymnGuard.CommandBridge")
logger.setLevel(logging.INFO)

class SovereignCommandBridge:
    """
    جسر توجيه الأوامر والتحليل المالي السيادي
    """
    def __init__(self):
        # تهيئة المحركات الأساسية
        self.market_engine = SovereignMarketEngine()
        self.neural_core = AdaptiveNeuralCore()
        logger.info("[Command Bridge]: تم إقلاع جسر الأوامر والأسواق السيادي بنجاح.")

    async def process_incoming_command(self, user_id: str, command_text: str) -> str:
        """
        معالجة الأوامر الواردة (التحليل المالي أو الاستفسارات العامة) مع درع ضد الانهيار.
        """
        if not command_text or not str(command_text).strip():
            return "يرجى إرسال أمر أو استفسار صحيح."

        clean_text = str(command_text).strip()

        try:
            # ==========================================
            # 1. نظام التوجيه المالي (Market Routing)
            # ==========================================
            if clean_text.lower().startswith("/market") or "تحليل" in clean_text:
                symbol = "BTCUSDT"  # القيمة الافتراضية
                parts = clean_text.split()
                
                # استخراج ذكي وآمن لرمز العملة
                if len(parts) > 1:
                    target_word = parts[1].upper()
                    if target_word not in ["تحليل", "/MARKET"]:
                        symbol = target_word
                        # درع حماية لتجنب إضافة USDT لعملات تحتوي على أزواج معروفة
                        known_pairs = ["USDT", "BUSD", "BTC", "ETH", "BNB", "USDC"]
                        if not any(symbol.endswith(pair) for pair in known_pairs):
                            symbol += "USDT"

                logger.info(f"[Bridge Market Request]: بدء تحليل السوق للرمز {symbol} للعميل {user_id}")
                
                # استدعاء محرك التداول المحدث
                market_report = await self.market_engine.execute_market_analysis(symbol)
                
                if market_report and market_report.get("status") == "success":
                    metrics = market_report.get("metrics", {})
                    current_price = metrics.get("current_price", 0.0)
                    rsi = metrics.get("RSI_14", 50.0)
                    sentiment = metrics.get("Market_Sentiment", "Neutral")
                    signal = market_report.get("action_signal", "HOLD")
                    
                    response = (
                        f"[التقرير المالي السيادي]\n\n"
                        f"- الرمز: `{symbol}`\n"
                        f"- السعر الحالي: `{current_price}`\n"
                        f"- مؤشر القوة النسبية (RSI): `{rsi}`\n"
                        f"- حالة السوق: `{sentiment}`\n"
                        f"- إشارة التداول: » **{signal}** «\n\n"
                        f"AymnGuard Enterprise Market Intelligence"
                    )
                    return response
                else:
                    logger.warning(f"[Market Engine]: تعذر جلب بيانات {symbol}.")
                    return f"عذراً، لم أتمكن من جلب بيانات السوق الحية للرمز `{symbol}` حالياً. تأكد من صحة الرمز (مثال: /market SOL)."

            # ==========================================
            # 2. التوجيه إلى المحرك العصبي (Neural AI)
            # ==========================================
            else:
                logger.info(f"[Bridge Neural Request]: توجيه طلب المستخدم {user_id} للمحرك العصبي.")
                neural_reply = await self.neural_core.synthesize_adaptive_response(clean_text)
                return neural_reply if neural_reply else "عذراً، المحرك العصبي يعيد ضبط نفسه للرد عليك بشكل أفضل."

        except Exception as e:
            # الدرع الفولاذي: يمنع توقف البوت تماماً ويرسل تنبيه مسجل
            logger.error(f"[Command Bridge Error]: فشل في معالجة الأمر للمستخدم {user_id}: {e}")
            logger.debug(traceback.format_exc())
            return "حدث خطأ داخلي عابر في جسر الأوامر السيادي. تم تحويل الخطأ للصيانة التلقائية."
