class AymnGuardError(Exception):
    """
    الفئة الجذرية (Base Exception) لجميع أخطاء المنظومة.
    تحمل بداخلها رسالة الخطأ وكود الحالة (HTTP/System Code) لتسهيل تصدير الأخطاء للـ API.
    """
    def __init__(self, message: str, code: int = 500):
        super().__init__(message)
        self.message = message
        self.code = code
        self.name = self.__class__.__name__

    def __str__(self):
        return f"[{self.code}] {self.name}: {self.message}"

# ==========================================
# 1. أخطاء قواعد البيانات والتخزين المؤقت
# ==========================================
class DatabaseError(AymnGuardError):
    """أخطاء الاتصال أو العمليات في PostgreSQL و Redis."""
    def __init__(self, message: str = "حدث خطأ في مزود البيانات", code: int = 503):
        super().__init__(message, code)

class RecordNotFoundError(DatabaseError):
    """عند البحث عن مستخدم أو عملية غير موجودة."""
    def __init__(self, message: str = "السجل المطلوب غير موجود في قاعدة البيانات", code: int = 404):
        super().__init__(message, code)

# ==========================================
# 2. أخطاء البوت والشبكة
# ==========================================
class NetworkAPIError(AymnGuardError):
    """أخطاء ناتجة عن فشل الاتصال بالخدمات الخارجية أو خوادم تيليجرام."""
    def __init__(self, message: str = "فشل الاتصال بالخوادم الخارجية", code: int = 502):
        super().__init__(message, code)

class RateLimitExceededError(AymnGuardError):
    """تجاوز الحد المسموح للطلبات (Spam/Flood Protection)."""
    def __init__(self, message: str = "تم تجاوز الحد المسموح للطلبات، يرجى الانتظار.", code: int = 429):
        super().__init__(message, code)

# ==========================================
# 3. أخطاء الحماية والصلاحيات
# ==========================================
class UnauthorizedAccessError(AymnGuardError):
    """محاولة وصول غير مصرح بها للوحة التحكم أو تنفيذ سكربتات إدارية."""
    def __init__(self, message: str = "صلاحيات غير كافية لتنفيذ هذا الإجراء", code: int = 403):
        super().__init__(message, code)

class SecurityTokenError(AymnGuardError):
    """خطأ في التحقق من صحة التوكن أو التشفير."""
    def __init__(self, message: str = "بيانات المصادقة غير صالحة أو منتهية", code: int = 401):
        super().__init__(message, code)

