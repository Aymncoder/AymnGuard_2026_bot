# -*- coding: utf-8 -*-
"""
=============================================================================
AymnGuard Enterprise Edition - Core Module Gateway
بوابة النواة السيادية - التحكم الصارم في تصدير أدوات الأمان والإعدادات
=============================================================================
"""

# 1. استدعاء الإعدادات الأساسية (سيتم إنشاؤها لاحقاً في config.py)
# from .config import settings

# 2. استدعاء محركات التشفير والمصادقة (سيتم إنشاؤها لاحقاً في security.py)
# from .security import verify_password, get_password_hash, create_access_token

# 3. قائمة التصدير الحصرية (The Allowed Export List)
# أي أداة غير موجودة في هذه القائمة لن يتمكن النظام من الوصول إليها، مما يمنع التداخل المعماري.

__all__ = [
    # "settings",
    # "verify_password",
    # "get_password_hash",
    # "create_access_token",
]

import logging
logger = logging.getLogger("AymnGuardCore")
logger.debug("🛡️ [Core Gateway]: تم تهيئة نواة النظام بنجاح وتأمين قنوات الاتصال الداخلية.")
