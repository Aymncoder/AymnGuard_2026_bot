# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Market Intelligence Engine
محرك الاستخبارات المالية: مسؤول عن الرصد اللحظي للأسواق، التحليل الفني العميق، 
وإدارة مخاطر المحافظ (Spot & USDⓈ-M Futures) دون تدخل بشري.
"""

import aiohttp
import logging
from typing import Dict, Any, List

# إعداد نظام السجلات (Logging) الخاص بالمحرك المالي
logger = logging.getLogger("AymnGuard.MarketEngine")
logger.setLevel(logging.INFO)

class SovereignMarketEngine:
    def __init__(self):
        """
        تهيئة مسارات الاتصال المركزية مع الأسواق المالية.
        الاعتماد على بنية Binance كمركز رئيسي للسيولة.
        """
        self.spot_base_url = "https://api.binance.com/api/v3"
        self.futures_base_url = "https://fapi.binance.com/fapi/v1"
        self.default_assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]

    async def fetch_market_data(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, float]]:
        """
        جلب بيانات الشموع اليابانية (Klines) لحظياً.
        """
        url_base = self.futures_base_url if market_type == "futures" else self.spot_base_url
        endpoint = f"{url_base}/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # استخراج البيانات المطلوبة (الإغلاق، الأعلى، الأدنى، الحجم)
                        klines = [
                            {
                                "close": float(candle[4]),
                                "high": float(candle[2]),
                                "low": float(candle[3]),
                                "volume": float(candle[5])
                            }
                            for candle in data
                        ]
                        return klines
                    else:
                        logger.error(f"⚠️ [Market Engine]: فشل جلب البيانات للزوج {symbol} - رمز الخطأ: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"❌ [Market Engine Error]: خطأ في الاتصال بخوادم التداول -> {e}")
            return []

    def calculate_ema(self, closes: List[float], period: int = 20) -> float:
        """حساب المتوسط المتحرك الأسّي (EMA)"""
        if len(closes) < period:
            return 0.0
        
        multiplier = 2 / (period + 1)
        ema = sum(closes[:period]) / period  # SMA مبدئي لأول فترة
        
        for price in closes[period:]:
            ema = (price - ema) * multiplier + ema
            
        return ema

    def calculate_rsi(self, closes: List[float], period: int = 14) -> float:
        """حساب مؤشر القوة النسبية (RSI)"""
        if len(closes) < period + 1:
            return 50.0

        gains = []
        losses = []
        
        for i in range(1, len(closes)):
            change = closes[i] - closes[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0.0)
            else:
                gains.append(0.0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    async def calculate_indicators(self, klines: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        معالجة البيانات الخام وحساب المؤشرات الفنية الاستراتيجية.
        """
        if not klines or len(klines) < 20:
            return {"status": "insufficient_data"}

        closes = [candle["close"] for candle in klines]
        current_price = closes[-1]

        # حساب المؤشرات
        ema_20 = self.calculate_ema(closes, period=20)
        rsi_14 = self.calculate_rsi(closes, period=14)

        # تحديد اتجاه Parabolic SAR مبسط (استناداً لموقع السعر من EMA)
        sar_trend = "Bullish" if current_price > ema_20 else "Bearish"

        # تحديد حالة السوق بناءً على RSI
        if rsi_14 > 70:
            sentiment = "Overbought"
        elif rsi_14 < 30:
            sentiment = "Oversold"
        else:
            sentiment = "Neutral"

        return {
            "current_price": round(current_price, 4),
            "EMA_20": round(ema_20, 4),
            "RSI_14": round(rsi_14, 2),
            "Parabolic_SAR_Trend": sar_trend,
            "Market_Sentiment": sentiment
        }

    async def execute_market_analysis(self, symbol: str, interval: str = "1h", market_type: str = "spot") -> Dict[str, Any]:
        """
        أمر سيادي يجمع البيانات ويصدر تقرير حالة السوق وإشارات التداول.
        """
        logger.info(f"📊 [Market Scan]: بدء تحليل الزوج {symbol} في سوق {market_type.upper()}...")
        
        klines = await self.fetch_market_data(symbol=symbol, interval=interval, market_type=market_type)
        indicators = await self.calculate_indicators(klines)
        
        if indicators.get("status") == "insufficient_data":
            return {"error": "بيانات السوق غير كافية لإجراء التحليل."}

        analysis_report = {
            "symbol": symbol.upper(),
            "market": market_type.upper(),
            "interval": interval,
            "metrics": indicators,
            "action_signal": "HOLD"  # الإشارة الافتراضية
        }

        # مصفوفة اتخاذ القرار (Decision Matrix)
        rsi = indicators["RSI_14"]
        price = indicators["current_price"]
        ema = indicators["EMA_20"]

        if rsi < 30 and price > ema:
            analysis_report["action_signal"] = "STRONG_BUY (Long)"
        elif rsi > 70 and price < ema:
            analysis_report["action_signal"] = "STRONG_SELL (Short)"
        elif rsi < 40 and indicators["Parabolic_SAR_Trend"] == "Bullish":
            analysis_report["action_signal"] = "BUY (Spot accumulation)"

        logger.info(f"✅ [Market Scan Complete]: إشارة التداول للزوج {symbol} هي {analysis_report['action_signal']}")
        return analysis_report
