# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Market Intelligence & Technical Analysis Engine
محرك ذكاء الأسواق والتحليل الفني الشامل: مسؤول عن جلب الأسعار الحية للعملات الرقمية،
حساب المؤشرات الفنية المتقدمة (EMA, RSI, SMA)، وتقديم قراءات سيادية دقيقة لاتخاذ القرارات الاستثمارية.
"""

import logging
import aiohttp
from typing import Dict, Any, List

logger = logging.getLogger("AymnGuard.MarketIntelligence")

class MarketIntelligenceEngine:
    """
    محرك التحليل المالي والأسواق الرقمية السيادي المتطور.
    """
    def __init__(self):
        self.binance_api_url = "https://api.binance.com/api/v3/ticker/price"
        self.klines_api_url = "https://api.binance.com/api/v3/klines"
        logger.info("📈 [Market Engine]: تم إقلاع محرك ذكاء الأسواق الرقمية المتقدم بنجاح.")

    async def fetch_live_price(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        جلب السعر الحي لأي أصل رقمي أو عملة مشفرة من السوق مباشرة.
        """
        url = f"{self.binance_api_url}?symbol={symbol.upper()}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        price = float(data.get("price", 0))
                        logger.info(f"📊 [Market Data]: سعر العملة {symbol.upper()} الحالي = {price}")
                        return {"symbol": symbol.upper(), "price": price, "status": "success"}
                    else:
                        logger.error(f"❌ [Market Error]: فشل جلب السعر للرمز {symbol}, الكود: {response.status}")
                        return {"symbol": symbol.upper(), "price": 0.0, "status": "failed"}
            except Exception as e:
                logger.error(f"❌ [Market Exception]: خطأ شبكي أثناء جلب السعر لـ {symbol}: {e}")
                return {"symbol": symbol.upper(), "price": 0.0, "status": "error", "message": str(e)}

    async def calculate_simple_moving_average(self, symbol: str = "BTCUSDT", period: int = 14) -> float:
        """
        حساب المتوسط المتحرك البسيط (SMA) بناءً على الشموع التاريخية للسوق.
        """
        url = f"{self.klines_api_url}?symbol={symbol.upper()}&interval=1h&limit={period}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        klines = await response.json()
                        closes = [float(candle[4]) for candle in klines]
                        if not closes:
                            return 0.0
                        sma = sum(closes) / len(closes)
                        logger.info(f"📐 [Technical Analysis]: حساب المتوسط المتحرك (SMA-{period}) للعملة {symbol.upper()} = {sma}")
                        return sma
            except Exception as e:
                logger.error(f"❌ [SMA Error]: خطأ أثناء حساب المتوسط المتحرك لـ {symbol}: {e}")
        return 0.0

    async def calculate_rsi(self, symbol: str = "BTCUSDT", period: int = 14) -> float:
        """
        حساب مؤشر القوة النسبية (RSI) لتحديد حالات التشبع البيعي أو الشرائي في السوق.
        """
        url = f"{self.klines_api_url}?symbol={symbol.upper()}&interval=1h&limit={period + 1}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        klines = await response.json()
                        closes = [float(candle[4]) for candle in klines]
                        if len(closes) < period + 1:
                            return 50.0
                        
                        gains, losses = 0.0, 0.0
                        for i in range(1, len(closes)):
                            change = closes[i] - closes[i - 1]
                            if change > 0:
                                gains += change
                            else:
                                losses -= change
                        
                        avg_gain = gains / period
                        avg_loss = losses / period
                        if avg_loss == 0:
                            return 100.0
                        
                        rs = avg_gain / avg_loss
                        rsi = 100 - (100 / (1 + rs))
                        logger.info(f"📊 [Technical Analysis]: مؤشر RSI للعملة {symbol.upper()} = {rsi:.2f}")
                        return round(rsi, 2)
            except Exception as e:
                logger.error(f"❌ [RSI Error]: خطأ أثناء حساب مؤشر RSI لـ {symbol}: {e}")
        return 50.0

    async def calculate_ema(self, symbol: str = "BTCUSDT", period: int = 14) -> float:
        """
        حساب المتوسط المتحرك الأسي (EMA) لتعقب الاتجاهات الحية بدقة عالية.
        """
        url = f"{self.klines_api_url}?symbol={symbol.upper()}&interval=1h&limit={period * 2}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        klines = await response.json()
                        closes = [float(candle[4]) for candle in klines]
                        if not closes:
                            return 0.0
                        
                        multiplier = 2 / (period + 1)
                        ema = closes[0]
                        for price in closes[1:]:
                            ema = (price - ema) * multiplier + ema
                        
                        logger.info(f"📐 [Technical Analysis]: حساب المتوسط المتحرك الأسي (EMA-{period}) للعملة {symbol.upper()} = {ema:.2f}")
                        return round(ema, 2)
            except Exception as e:
                logger.error(f"❌ [EMA Error]: خطأ أثناء حساب EMA لـ {symbol}: {e}")
        return 0.0

    async def evaluate_market_condition(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        تقييم شامل لحالة السوق الفنية عبر دمج السعر، المتوسطات، ومؤشر القوة النسبية (RSI)
        لإصدار تقرير استثماري سيادي متكامل.
        """
        price_data = await self.fetch_live_price(symbol)
        current_price = price_data.get("price", 0.0)
        sma_value = await self.calculate_simple_moving_average(symbol, period=14)
        ema_value = await self.calculate_ema(symbol, period=14)
        rsi_value = await self.calculate_rsi(symbol, period=14)

        if current_price == 0:
            return {"status": "error", "message": "تعذر تحليل السوق لعدم توفر البيانات الحية."}

        # تحديد حالة التشبع والزخم
        rsi_status = "محايد"
        if rsi_value > 70:
            rsi_status = "تشبع شرائي (Overbought) - احتمال حدوث تصحيح هبوطي قريب."
        elif rsi_value < 30:
            rsi_status = "تشبع بيعي (Oversold) - فرصة محتملة للاستحواذ والارتداد الصعودي."

        trend = "صعودي (Bullish)" if current_price > ema_value else "هبوطي (Bearish)"

        assessment_summary = (
            f"الرمز: {symbol.upper()} | السعر: {current_price} | "
            f"الاتجاه (EMA): {trend} | مؤشر RSI: {rsi_value} ({rsi_status})"
        )

        logger.info(f"🎯 [Sovereign Market Assessment]: {assessment_summary}")
        return {
            "symbol": symbol.upper(),
            "price": current_price,
            "sma_14": sma_value,
            "ema_14": ema_value,
            "rsi_14": rsi_value,
            "rsi_status": rsi_status,
            "trend": trend,
            "summary": assessment_summary,
            "status": "success"
        }
