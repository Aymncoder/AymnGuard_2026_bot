import logging
from core.database.engine import AsyncSessionLocal

class SovereignBaseAgent:
    """
    النواة الأساسية التي يرث منها جميع الوكلاء في الإمبراطورية.
    توفر إمكانية الوصول المشترك والمحمي لقاعدة البيانات ونظام التسجيل.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(self.agent_name)
        logger.setLevel(logging.INFO)
        # سيتم توجيه السجلات لاحقاً إلى Master Deployment Log
        return logger

    async def get_db(self):
        """فتح جلسة اتصال آمنة مع ترسانة البيانات"""
        async with AsyncSessionLocal() as session:
            yield session
