# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Ultra-Speed Sovereign Proxy Manager (v34.9.0)
محرك التوجيه السيادي الخارق للسرعة والذكاء للبروكسيات
=============================================================================
"""

import socks
import random
import logging
import time
import socket
from typing import List, Tuple, Optional

logger = logging.getLogger("AymnGuard.EnterpriseUltraProxy")

class SovereignUltraProxyManager:
    """
    مدير بروكسيات سيادي متطور يعتمد على خوارزمية أقل زمن استجابة (Lowest-Latency)
    لضمان سرعة فائقة واستقرار تام للاتصال 24/7.
    """
    def __init__(self, proxy_pool: List[dict]):
        """
        proxy_pool: قائمة تحتوي على إعدادات البروكسيات مع تتبع الأداء (السرعة والحالة)
        """
        self.proxy_pool = []
        for p in proxy_pool:
            self.proxy_pool.append({
                "host": p.get("host"),
                "port": p.get("port"),
                "username": p.get("username"),
                "password": p.get("password"),
                "latency": 9999.0,  # زمن الاستجابة الابتدائي (افتراضي كبير)
                "is_healthy": True,
                "fail_count": 0
            })
        self._refresh_latencies()

    def _test_proxy_latency(self, host: str, port: int, timeout: float = 1.5) -> float:
        """
        قياس سرعة استجابة البروكسي (Ping/Latency Test) بدقة عالية بالمللي ثانية.
        """
        start_time = time.perf_counter()
        try:
            with socket.create_connection((host, int(port)), timeout=timeout):
                elapsed = (time.perf_counter() - start_time) * 1000.0  # تحويل إلى ميللي ثانية
                return elapsed
        except Exception:
            return 9999.0  # في حال فشل الاتصال

    def _refresh_latencies(self):
        """
        فحص سريع لجميع البروكسيات وترتيبها حسب الأسرع لتوجيه حركة البيانات فوراً.
        """
        for p in self.proxy_pool:
            lat = self._test_proxy_latency(p["host"], p["port"])
            p["latency"] = lat
            if lat < 5000.0:
                p["is_healthy"] = True
                p["fail_count"] = 0
            else:
                p["fail_count"] += 1
                if p["fail_count"] > 3:
                    p["is_healthy"] = False

        # فرز القائمة بحيث يكون الأسرع والأصح في المقدمة دائماً
        self.proxy_pool.sort(key=lambda x: (not x["is_healthy"], x["latency"]))

    def get_fastest_proxy_config(self) -> Optional[Tuple]:
        """
        إرجاع إعدادات البروكسي الأسرع على الإطلاق (Lowest Latency) لمكتبات تيليجرام (Pyrogram/Telethon).
        """
        # تحديث الدوري للسرعات إذا لزم الأمر
        healthy_proxies = [p for p in self.proxy_pool if p["is_healthy"]]
        
        if not healthy_proxies:
            logger.warning("تحذير سيادي: جميع البروكسيات مسجلة كغير صالحة، سيتم إعادة ضبط الشبكة أو الاتصال المباشر.")
            if self.proxy_pool:
                best = self.proxy_pool[0] # العودة لأفضل المتاح اضطرارياً
            else:
                return None
        else:
            # اختيار الأسرع (الأول في القائمة المرتبة)
            best = healthy_proxies[0]

        logger.info(f"توجيه فائق السرعة عبر البروكسي: {best['host']}:{best['port']} (زمن الاستجابة: {best['latency']:.2f}ms)")

        return (
            socks.SOCKS5,
            best["host"],
            int(best["port"]),
            True,  # rdns
            best.get("username"),
            best.get("password")
        )

    def report_failure(self, host: str):
        """
        نظام استجابة فورية لعزل البروكسي الفاشل وتحويل الاتصال لبروكسي بديل في أجزاء من الثانية.
        """
        for p in self.proxy_pool:
            if p["host"] == host:
                p["fail_count"] += 1
                if p["fail_count"] >= 2:
                    p["is_healthy"] = False
                   logger.error(f"[ERROR] عزل البروكسي البطيء/الميت: {host}")
                   break
