# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise - Sovereign Base Agent (v34.9.1)
=============================================================================
"""

import logging
from core.database.engine import AsyncSessionLocal

logger = logging.getLogger("AymnGuard.SovereignBaseAgent")

class SovereignBaseAgent:
    """
    النواة الأساسية التي يرث منها جميع الوكلاء في الإمبراطورية.
    توفير إمكانية الوصول المشترك والمحمي لقاعدة البيانات ونظام التسجيل.
    """
    def __init__(self, agent_name: str = "EnterpriseAgent"):
        self.agent_name = agent_name
        self.logger = self._setup_logger()

    def _setup_logger(self):
        agent_logger = logging.getLogger(self.agent_name)
        agent_logger.setLevel(logging.INFO)
        return agent_logger

    async def get_db(self):
        """
        فتح جلسة اتصال آمنة مع قاعدة البيانات السحابية.
        """
        async with AsyncSessionLocal() as session:
            yield session
