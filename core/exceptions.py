# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise - Sovereign Exception Hierarchy (v18.0.0-Master)
==============================================================================
جهاز المناعة المركزي: تصنيف وعزل أخطاء المنظومة لمنع الانهيار،
مع دعم كامل للاستجابات الديناميكية لواجهات فلاتر (JSON Responses).
"""

class AymnGuardError(Exception):
    """
    الفئة الجذرية (Base Exception) لجميع أخطاء المنظومة.
    تحمل بداخلها رسالة الخطأ وكود الحالة (HTTP Status) لتسهيل تصديرها عبر الـ API.
    """
    def __init__(self, message: str, code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code
        self.name = self.__class__.__name__

    def __str__(self) -> str:
        return f"[{self.code}] {self.name}: {self.message}"

    def to_dict(self) -> dict:
        """ميزة مؤسسية: تحويل الخطأ مباشرة إلى رد JSON مفهوم لتطبيق فلاتر"""
        return {
            "status": "error",
            "error_type": self.name,
            "message": self.message,
            "code": self.code
        }

# ============================================================================
# 1. أخطاء قواعد البيانات والتخزين المؤقت
# ============================================================================
class DatabaseError(AymnGuardError):
    """أخطاء الاتصال أو العمليات في مزود البيانات"""
    def __init__(self, message: str = "حدث خطأ في مزود البيانات", code: int = 500):
        super().__init__(message, code)

class RecordNotFoundError(DatabaseError):
    """عند البحث عن سجل أو مستخدم غير موجود"""
    def __init__(self, message: str = "السجل المطلوب غير موجود في قاعدة البيانات", code: int = 404):
        super().__init__(message, code)

# ============================================================================
# 2. أخطاء الشبكة، البوتات، والذكاء الاصطناعي (المحركات)
# ============================================================================
class NetworkAPIError(AymnGuardError):
    """فشل الاتصال بالخدمات الخارجية (Telegram, Binance, Web3)"""
    def __init__(self, message: str = "فشل الاتصال بالخوادم الخارجية", code: int = 502):
        super().__init__(message, code)

class RateLimitExceededError(AymnGuardError):
    """تجاوز الحد المسموح للطلبات (Flood Protection / Anti-Spam)"""
    def __init__(self, message: str = "تم تجاوز الحد المسموح للطلبات، يرجى الانتظار", code: int = 429):
        super().__init__(message, code)

class NeuralCoreError(AymnGuardError):
    """أخطاء محرك الذكاء الاصطناعي والمحرك العصبي"""
    def __init__(self, message: str = "فشل في معالجة البيانات أو التوليد عبر المحرك العصبي", code: int = 503):
        super().__init__(message, code)

class MarketEngineError(AymnGuardError):
    """أخطاء محرك التداول وسحب بيانات السوق الحية"""
    def __init__(self, message: str = "تعذر جلب بيانات السوق الحية أو تنفيذ العملية المالية", code: int = 500):
        super().__init__(message, code)

# ============================================================================
# 3. أخطاء الحماية، الصلاحيات، والجلسات
# ============================================================================
class UnauthorizedAccessError(AymnGuardError):
    """محاولة وصول غير مصرح بها أو تجاوز الصلاحيات (لوحة التحكم)"""
    def __init__(self, message: str = "صلاحيات غير كافية لتنفيذ هذا الإجراء", code: int = 403):
        super().__init__(message, code)

class SecurityTokenError(AymnGuardError):
    """انتهاء صلاحية التوكن (JWT) أو فشل التحقق"""
    def __init__(self, message: str = "بيانات المصادقة غير صالحة أو منتهية الصلاحية", code: int = 401):
        super().__init__(message, code)

class InvalidSessionError(AymnGuardError):
    """عندما يتم طرد أو حظر جلسة تيليجرام (Session Revoked)"""
    def __init__(self, message: str = "جلسة الاتصال ميتة أو تم سحب صلاحيتها من الخادم", code: int = 401):
        super().__init__(message, code)

