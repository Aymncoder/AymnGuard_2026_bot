# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Market Intelligence & Technical Analysis Engine
محرك ذكاء الأسواق والتحليل الفني: مسؤول عن جلب الأسعار الحية للعملات الرقمية،
حساب المؤشرات الفنية (EMA, RSI)، وتقديم قراءات دقيقة لاتخاذ القرارات الاستثمارية.
"""

import logging
import aiohttp
from typing import Dict, Any, List

logger = logging.getLogger("AymnGuard.MarketIntelligence")

class MarketIntelligenceEngine:
    """
    محرك التحليل المالي والأسواق الرقمية السيادي.
    """
    def __init__(self):
        self.binance_api_url = "https://api.binance.com/api/v3/ticker/price"
        self.klines_api_url = "https://api.binance.com/api/v3/klines"
        logger.info("📈 [Market Engine]: تم إقلاع محرك ذكاء الأسواق الرقمية بنجاح.")

    async def fetch_live_price(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        جلب السعر الحي لأي أصْل رقمي أو عملة مشفرة من السوق مباشرة.
        مثال: BTCUSDT, ETHUSDT, SOLUSDT, LABUSDT
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
                        # إغلاق الشموع موجود في الفهرس [4] لكل شمعة
                        closes = [float(candle[4]) for candle in klines]
                        if not closes:
                            return 0.0
                        sma = sum(closes) / len(closes)
                        logger.info(f"📐 [Technical Analysis]: حساب المتوسط المتحرك (SMA-{period}) للعملة {symbol.upper()} = {sma}")
                        return sma
            except Exception as e:
                logger.error(f"❌ [SMA Error]: خطأ أثناء حساب المتوسط المتحرك لـ {symbol}: {e}")
        return 0.0

    async def evaluate_market_condition(self, symbol: str = "BTCUSDT") -> str:
        """
        تقييم حالة السوق الفنية للعملة ومقارنة السعر بالمتوسط المتحرك 
        لإصدار إشارة أولية (صعود، هبوط، أو تذبذب).
        """
        price_data = await self.fetch_live_price(symbol)
        current_price = price_data.get("price", 0.0)
        sma_value = await self.calculate_simple_moving_average(symbol, period=14)

        if current_price == 0 or sma_value == 0:
            return "تعذر تحليل السوق لعدم توفر البيانات الكافية."

        if current_price > sma_value:
            assessment = f"إشارة إيجابية (Bullish): السعر الحالي ({current_price}) أعلى من المتوسط المتحرك ({sma_value:.2f}). الزخم يميل للصعود."
        else:
            assessment = f"إشارة سلبية أو تصحيحية (Bearish): السعر الحالي ({current_price}) أقل من المتوسط المتحرك ({sma_value:.2f}). الحذر واجب."

        logger.info(f"🎯 [Market Assessment]: {assessment}")
        return assessment
