# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise - Sovereign Proxy Manager (v34.9.1)
Enterprise-grade proxy orchestration for cloud environments.
"""

import socks
import random
import logging
import time
import socket
import os
from typing import List, Tuple, Optional

# إعداد السجلات بشكل احترافي للأنظمة السحابية
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AymnGuard.EnterpriseUltraProxy")

class SovereignUltraProxyManager:
    """
    Enterprise proxy manager optimized for cloud-hosted environments.
    """
    def __init__(self, proxy_pool: List[dict]):
        self.proxy_pool = []
        for p in proxy_pool:
            self.proxy_pool.append({
                "host": p.get("host"),
                "port": p.get("port"),
                "username": p.get("username"),
                "password": p.get("password"),
                "latency": 9999.0,
                "is_healthy": True,
                "fail_count": 0
            })
        self._refresh_latencies()

    def _test_proxy_latency(self, host: str, port: int, timeout: float = 2.0) -> float:
        """
        Measurement optimized for cloud network stability.
        """
        start_time = time.perf_counter()
        try:
            with socket.create_connection((host, int(port)), timeout=timeout):
                return (time.perf_counter() - start_time) * 1000.0
        except (socket.timeout, ConnectionRefusedError, OSError):
            return 9999.0

    def _refresh_latencies(self):
        """
        Refreshes latency metrics and sorts by health and speed.
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

        self.proxy_pool.sort(key=lambda x: (not x["is_healthy"], x["latency"]))

    def get_fastest_proxy_config(self) -> Optional[Tuple]:
        """
        Returns the best proxy configuration for Telegram libraries.
        """
        healthy_proxies = [p for p in self.proxy_pool if p["is_healthy"]]
        
        if not healthy_proxies:
            logger.warning("All proxies unhealthy. Falling back to primary or direct connection.")
            best = self.proxy_pool[0] if self.proxy_pool else None
        else:
            best = healthy_proxies[0]

        if not best:
            return None

        logger.info(f"Routing traffic via: {best['host']}:{best['port']} | Latency: {best['latency']:.2f}ms")

        return (
            socks.SOCKS5,
            best["host"],
            int(best["port"]),
            True,
            best.get("username"),
            best.get("password")
        )

    def report_failure(self, host: str):
        """
        Isolates failing proxies to prevent bottlenecking.
        """
        for p in self.proxy_pool:
            if p["host"] == host:
                p["fail_count"] += 1
                if p["fail_count"] >= 2:
                    p["is_healthy"] = False
                    logger.error(f"Isolating failed proxy: {host}")
                break
