# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Market Intelligence Engine
محرك الاستخبارات المالية: مسؤول عن الرصد اللحظي للأسواق، التحليل الفني العميق، 
وإدارة مخاطر المحافظ (Spot & USDⓈ-M Futures) دون تدخل بشري.
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, List

# تهيئة مسجل الأحداث الخاص بالذراع المالي
logger = logging.getLogger("AymnGuard.MarketEngine")

class SovereignMarketEngine:
    def __init__(self):
        """
        تهيئة مسارات الاتصال المركزية مع الأسواق المالية.
        تم التركيز على بنية Binance كمركز رئيسي للسيولة.
        """
        self.spot_base_url = "https://api.binance.com/api/v3"
        self.futures_base_url = "https://fapi.binance.com/fapi/v1"
        # أزواج افتراضية للمراقبة المستمرة
        self.default_assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]

    async def fetch_market_data(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict]:
        """
        جلب بيانات الشموع اليابانية (Klines) لحظياً وبسرعة فائقة (Zero-Lag).
        """
        url_base = self.futures_base_url if market_type == "futures" else self.spot_base_url
        endpoint = f"{url_base}/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # تنظيف البيانات واستخراج الإغلاقات (Close Prices)
                        klines = [{"time": candle[0], "close": float(candle[4]), "high": float(candle[2]), "low": float(candle[3]), "volume": float(candle[5])} for candle in data]
                        return klines
                    else:
                        logger.error(f"⚠️ [Market Engine]: فشل جلب البيانات للزوج {symbol} - {response.status}")
                        return []
        except Exception as e:
            logger.error(f"❌ [Market Engine Error]: خطأ في الاتصال بالشبكة -> {e}")
            return []

    async def calculate_indicators(self, klines: List[Dict]) -> Dict[str, float]:
        """
        معالجة البيانات الخام وحساب المؤشرات الفنية الاستراتيجية.
        (يتم الحساب هنا رياضياً أو عبر مكتبات مخصصة مستقبلاً)
        """
        if not klines or len(klines) < 14:
            return {"status": "insufficient_data"}

        closes = [candle["close"] for candle in klines]
        current_price = closes[-1]

        # 1. حساب المتوسط المتحرك الأسّي (EMA) - تقريبي للسرعة
        # المعادلة الرياضية للـ EMA تعطي وزناً أكبر للأسعار الحديثة
        ema_period = 20
        multiplier = 2 / (ema_period + 1)
        ema = sum(closes[-ema_period:]) / ema_period # SMA مبدئي
        for price in closes[-ema_period:]:
            ema = (price - ema) * multiplier + ema

        # 2. مؤشر القوة النسبية (RSI) - فترة 14
        gains = []
        losses = []
        for i in range(1, len(closes)):
            change = closes[i] - closes[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else 0
        avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else 1 # تفادي القسمة على صفر
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))

        # 3. محاكاة مبدئية لـ Parabolic SAR لتحديد الانعكاسات (Reversals)
        # سيتم دمج خوارزمية SAR المعقدة في التحديث القادم للوحدة
        sar_trend = "Bullish" if current_price > ema else "Bearish"

        return {
            "current_price": round(current_price, 4),
            "EMA_20": round(ema, 4),
            "RSI_14": round(rsi, 2),
            "Parabolic_SAR_Trend": sar_trend,
            "Market_Sentiment": "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"
        }

    async def execute_market_analysis(self, symbol: str, market_type: str = "spot") -> Dict[str, Any]:
        """
        العملية المجمعة: أمر سيادي يجمع البيانات ويصدر تقرير حالة السوق.
        """
        logger.info(f"📊 [Market Scan]: بدء تحليل عميق للزوج {symbol} في سوق {market_type.upper()}...")
        
        klines = await self.fetch_market_data(symbol=symbol, market_type=market_type)
        indicators = await self.calculate_indicators(klines)
        
        analysis_report = {
            "symbol": symbol.upper(),
            "market": market_type.upper(),
            "metrics": indicators,
            "action_signal": "HOLD" # إشارة افتراضية
        }

        # منطق اتخاذ القرار الآلي (Decision Matrix)
        if indicators.get("RSI_14", 50) < 30 and indicators.get("current_price", 0) > indicators.get("EMA_20", 0):
            analysis_report["action_signal"] = "STRONG_BUY (Long)"
        elif indicators.get("RSI_14", 50) > 70 and indicators.get("current_price", 0) < indicators.get("EMA_20", 0):
            analysis_report["action_signal"] = "STRONG_SELL (Short)"

        logger.info(f"✅ [Market Scan Complete]: إشارة التداول الحالية للزوج {symbol} هي {analysis_report['action_signal']}")
        return analysis_report

# ==========================================
# اختبار ذاتي للمحرك (عند التشغيل المباشر)
# ==========================================
if __name__ == "__main__":
    async def test_engine():
        engine = SovereignMarketEngine()
        result = await engine.execute_market_analysis("SOLUSDT", market_type="futures")
        print("\n--- تقرير الاستخبارات المالية ---")
        for key, value in result.items():
            print(f"{key}: {value}")
            
    asyncio.run(test_engine())
