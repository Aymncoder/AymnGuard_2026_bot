import socks
import random
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger("AymnGuard.EnterpriseProxy")

class SovereignProxyManager:
    """
    محرك إدارة وتدوير البروكسيات السيادي (Enterprise SOCKS5/MTProto Pool)
    يضمن استمرارية الاتصال بـ Telegram 24/7 دون انقطاع عبر التبديل التلقائي.
    """
    def __init__(self, proxy_pool: List[dict]):
        """
        proxy_pool: قائمة تحتوي على إعدادات البروكسيات المتعددة
        [
            {"host": "IP1", "port": 1080, "username": "...", "password": "..."},
            {"host": "IP2", "port": 1080, "username": "...", "password": "..."}
        ]
        """
        self.proxy_pool = proxy_pool
        self.current_index = 0

    def get_active_proxy(self) -> Optional[Tuple]:
        """
        استخراج البروكسي الحالي بالتناوب (Round-Robin) وتنسيقه لـ Telethon / Pyrogram
        """
        if not self.proxy_pool:
            logger.warning("⚠️ لا توجد بروكسيات مسجلة في المسبح! سيتم استخدام الاتصال المباشر.")
            return None

        p_config = self.proxy_pool[self.current_index]
        # التبديل للبروكسي التالي في المرة القادمة
        self.current_index = (self.current_index + 1) % len(self.proxy_pool)

        # صيغة التنسيق المتوافقة مع مكتبات تيليجرام (SOCKS5)
        return (
            socks.SOCKS5,
            p_config["host"],
            p_config["port"],
            True,  # rdns
            p_config.get("username"),
            p_config.get("password")
        )

    def get_resilient_client_config(self) -> Optional[Tuple]:
        """
        اختيار بروكسي عشوائي ذكي في حال فشل الاتصال الأساسي
        """
        if not self.proxy_pool:
            return None
        p_config = random.choice(self.proxy_pool)
        return (
            socks.SOCKS5,
            p_config["host"],
            p_config["port"],
            True,
            p_config.get("username"),
            p_config.get("password")
        )
