# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Sovereign Market Intelligence Engine (Cloud Optimized)
==============================================================================
محرك الاستخبارات المالية (النسخة المحصنة ضد الأخطاء وخالية من الرموز):
رصد لحظي للأسواق، تحليل فني عميق، وحماية مطلقة للمحافظ (Spot & Futures) 
مع دروع رياضية ضد القيم التالفة والاتصالات المتقطعة.
==============================================================================
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, List

# إعداد نظام السجلات الخاص بالمحرك المالي
logger = logging.getLogger("AymnGuard.MarketEngine")
logger.setLevel(logging.INFO)

class SovereignMarketEngine:
    def __init__(self):
        """
        تهيئة مسارات الاتصال المركزية مع الأسواق المالية العالمية.
        الاعتماد على بنية Binance كمركز رئيسي للسيولة السحابية.
        """
        self.spot_base_url = "https://api.binance.com/api/v3"
        self.futures_base_url = "https://fapi.binance.com/fapi/v1"
        self.default_assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"]

    async def fetch_market_data(self, symbol: str, interval: str = "1h", limit: int = 100, market_type: str = "spot") -> List[Dict[str, float]]:
        """
        جلب بيانات الشموع اليابانية (Klines) لحظياً مع درع إعادة المحاولة الآلي.
        """
        url_base = self.futures_base_url if market_type.lower() == "futures" else self.spot_base_url
        endpoint = f"{url_base}/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

        max_retries = 3
        timeout = aiohttp.ClientTimeout(total=10.0)

        for attempt in range(1, max_retries + 1):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(endpoint, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            if not isinstance(data, list):
                                logger.warning(f"[Market Engine Warning]: استجابة غير صالحة من بينانس للزوج {symbol}")
                                return []

                            klines = []
                            for candle in data:
                                try:
                                    # حماية صارمة ضد أي بيانات تالفة أو ناقصة في الشموع
                                    klines.append({
                                        "close": float(candle[4]),
                                        "high": float(candle[2]),
                                        "low": float(candle[3]),
                                        "volume": float(candle[5])
                                    })
                                except (IndexError, ValueError, TypeError):
                                    continue # تخطي الشمعة التالفة دون انهيار النظام

                            return klines
                        else:
                            logger.warning(f"[Market Engine Warning]: فشل جلب البيانات للزوج {symbol} (محاولة {attempt}/{max_retries}) - الكود: {response.status}")
                            await asyncio.sleep(1)
            except asyncio.TimeoutError:
                logger.warning(f"[Market Engine Timeout]: انقضت مهلة الاتصال لـ {symbol} (محاولة {attempt})")
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f"[Market Engine Error]: خطأ في الاتصال بخوادم التداول للزوج {symbol} -> {e}")
                await asyncio.sleep(1)

        logger.error(f"[Market Engine Failure]: تعذر جلب بيانات السوق للزوج {symbol} بعد استنفاد المحاولات.")
        return []

    def calculate_ema(self, closes: List[float], period: int = 20) -> float:
        """حساب المتوسط المتحرك الأسّي (EMA) مع درع ضد الأخطاء الرياضية"""
        if not closes or len(closes) < period:
            return closes[-1] if closes else 0.0
        
        try:
            multiplier = 2 / (period + 1)
            ema = sum(closes[:period]) / period  
            
            for price in closes[period:]:
                ema = (price - ema) * multiplier + ema
                
            return ema
        except Exception as e:
            logger.error(f"[EMA Math Error]: {e}")
            return closes[-1] if closes else 0.0

    def calculate_rsi(self, closes: List[float], period: int = 14) -> float:
        """حساب مؤشر القوة النسبية (RSI) مع حماية مطلقة من القسمة على صفر"""
        if not closes or len(closes) < period + 1:
            return 50.0

        try:
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
                return 100.0 if avg_gain > 0 else 50.0
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return max(0.0, min(100.0, rsi)) # ضمان بقاء المؤشر بين 0 و 100 دائماً
        except Exception as e:
            logger.error(f"[RSI Math Error]: {e}")
            return 50.0

    async def calculate_indicators(self, klines: List[Dict[str, float]]) -> Dict[str, Any]:
        """معالجة البيانات الخام وحساب المؤشرات الفنية بدقة استراتيجية وآمنة."""
        if not klines or len(klines) < 20:
            return {"status": "insufficient_data"}

        try:
            closes = [candle["close"] for candle in klines]
            current_price = closes[-1]

            ema_20 = self.calculate_ema(closes, period=20)
            rsi_14 = self.calculate_rsi(closes, period=14)

            sar_trend = "Bullish" if current_price > ema_20 else "Bearish"

            if rsi_14 > 70:
                sentiment = "Overbought"
            elif rsi_14 < 30:
                sentiment = "Oversold"
            else:
                sentiment = "Neutral"

            return {
                "status": "success",
                "current_price": round(current_price, 4),
                "EMA_20": round(ema_20, 4),
                "RSI_14": round(rsi_14, 2),
                "Parabolic_SAR_Trend": sar_trend,
                "Market_Sentiment": sentiment
            }
        except Exception as e:
            logger.error(f"[Indicators Calculation Error]: {e}")
            return {"status": "insufficient_data"}

    async def execute_market_analysis(self, symbol: str, interval: str = "1h", market_type: str = "spot") -> Dict[str, Any]:
        """أمر سيادي يجمع البيانات ويصدر تقرير حالة السوق وإشارات التداول بأمان تام."""
        logger.info(f"[Market Scan]: بدء تحليل الزوج {symbol.upper()} في سوق {market_type.upper()}...")
        
        try:
            klines = await self.fetch_market_data(symbol=symbol, interval=interval, market_type=market_type)
            indicators = await self.calculate_indicators(klines)
            
            if not indicators or indicators.get("status") != "success":
                return {"status": "error", "message": "بيانات السوق غير كافية أو حدث خطأ أثناء سحب الشموع."}

            action_signal = "HOLD"
            rsi = indicators["RSI_14"]
            price = indicators["current_price"]
            ema = indicators["EMA_20"]

            if rsi < 30 and price > ema:
                action_signal = "STRONG_BUY (Long)"
            elif rsi > 70 and price < ema:
                action_signal = "STRONG_SELL (Short)"
            elif rsi < 40 and indicators["Parabolic_SAR_Trend"] == "Bullish":
                action_signal = "BUY (Spot accumulation)"

            analysis_report = {
                "status": "success",
                "symbol": symbol.upper(),
                "market": market_type.upper(),
                "interval": interval,
                "metrics": {
                    "current_price": indicators["current_price"],
                    "EMA_20": indicators["EMA_20"],
                    "RSI_14": indicators["RSI_14"],
                    "Parabolic_SAR_Trend": indicators["Parabolic_SAR_Trend"],
                    "Market_Sentiment": indicators["Market_Sentiment"]
                },
                "action_signal": action_signal
            }

            logger.info(f"[Market Scan Complete]: إشارة التداول للزوج {symbol.upper()} هي {action_signal}")
            return analysis_report
        except Exception as e:
            logger.error(f"[Market Execution Error]: فشل التحليل المالي للزوج {symbol}: {e}")
            return {"status": "error", "message": "حدث خطأ داخلي في محرك الاستخبارات المالية."}
