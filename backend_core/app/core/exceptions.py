"""
=============================================================================
AymnGuard Enterprise Logistics Platform - Sovereign Exceptions Engine
محرك الاستثناءات والأخطاء المؤسسي السيادي - معالجة استباقية، تتبع ذكي، وأمان مطلق.
=============================================================================
"""

from datetime import datetime
from typing import Dict, Any, Optional

class SovereignBaseException(Exception):
    """
    الاستثناء الأساسي السيادي لكافة أخطاء المنصة المؤسسية.
    يضمن هيكلة موحدة للردود ومعالجة استباقية دقيقة للعمليات الضخمة.
    """
    def __init__(
        self, 
        message: str, 
        error_code: str = "ERR_SOVEREIGN_CORE", 
        status_code: int = 400, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """تحويل الاستثناء إلى هيكل بيانات منظم وجاهز للإرسال عبر الـ API"""
        return {
            "status": "error",
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class SovereignAuthenticationError(SovereignBaseException):
    """خطأ في المصادقة السيادية أو انتهاك مفتاح المالك."""
    def __init__(self, message: str = "فشل التوثيق السيادي أو مفتاح الأمان غير صالح."):
        super().__init__(
            message=message, 
            error_code="ERR_AUTH_SOVEREIGN_BREACH", 
            status_code=403
        )


class LogisticsExecutionError(SovereignBaseException):
    """أخطاء العمليات اللوجستية الضخمة وإدارة التوزيع السحابي والذكي."""
    def __init__(self, details: str, custom_message: str = "حدث خطأ في تنفيذ العمليات اللوجستية الضخمة."):
        super().__init__(
            message=custom_message,
            error_code="ERR_LOGISTICS_EXECUTION_FAILURE",
            status_code=500,
            details={"execution_error": details}
        )


class RateLimitExceededError(SovereignBaseException):
    """حماية البنية التحتية ضد الضغط الهائل والطلبات المتكررة والهجمات."""
    def __init__(self, message: str = "تم تجاوز الحد الأقصى المسموح للطلبات. يرجى التهدئة قليلاً."):
        super().__init__(
            message=message,
            error_code="ERR_RATE_LIMIT_EXCEEDED",
            status_code=429
        )


class Web3FinancialTransactionError(SovereignBaseException):
    """أخطاء المعاملات المالية اللامركزية والبلوكشين والعقود الذكية."""
    def __init__(self, details: str):
        super().__init__(
            message="فشل تنفيذ المعاملة المالية أو العقود الذكية عبر الشبكة.",
            error_code="ERR_WEB3_FINANCIAL_FAILURE",
            status_code=400,
            details={"web3_error": details}
        )


class TelegramAutomationError(SovereignBaseException):
    """أخطاء أتمتة تيليجرام، الجلسات، وتجاوز القيود البرمجية."""
    def __init__(self, details: str):
        super().__init__(
            message="حدث خطأ أثناء تنفيذ عملية الأتمتة عبر شبكة تيليجرام.",
            error_code="ERR_TELEGRAM_AUTOMATION_FAILURE",
            status_code=502,
            details={"telegram_error": details}
        )
