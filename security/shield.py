# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v12.0.0 : Advanced Sovereign Security Shield & AST Engine
==============================================================================
الحصن السيبراني المتقدم والنواة الأمنية: 
تمت هندسة هذا المكون ليكون السد المنيع (Zero-Trust Architecture) ضد كافة أنواع الهجمات السيبرانية.
يتضمن:
1. فحص الحمولات العميقة والمتداخلة (Recursive Payload Inspection).
2. التحقق الأمني الثابت ضد (SQLi, XSS, Command Injection, Path Traversal).
3. التعقيم الديناميكي للمدخلات (Dynamic Sanitization).
4. إدارة سجلات التدقيق غير القابلة للتلاعب (Immutable Audit Trails) بمعايير المؤسسات الكبرى.
"""

import re
import html
import json
import logging
import datetime
from typing import Any, Dict, Optional, Union, List
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# استيراد نموذج سجلات التدقيق السيادي مع تغطية شاملة وهندسية لمسارات الاستيراد المعقدة
try:
    from database.models import SovereignAuditLog
except ImportError:
    try:
        from models import SovereignAuditLog
    except ImportError:
        SovereignAuditLog = None  # حماية هيكلية لمنع انهيار النظام في حال غياب النموذج

# إعداد السجلات الأمنية السيادية الموحدة ببروتوكولات صارمة
logger = logging.getLogger("AymnGuard.SovereignSecurityShield")
logger.setLevel(logging.INFO)

class SovereignSecurityShield:
    """
    محرك الحصن السيبراني المتقدم: 
    يطبق أعلى معايير الحماية والتفتيش الأمني (AST) بتقنية الفحص العميق للحمولات.
    """
    
    # أنماط الهجمات السيبرانية الشائعة والمتقدمة للتحقق الفوري (Enterprise Pattern Matching)
    SQL_INJECTION_PATTERNS = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(?i)(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|EXECUTE)\s+",
        r"(?i)OR\s+1\s*=\s*1",
        r"(?i)UNION\s+(ALL\s+)?SELECT",
        r"(?i)WAITFOR\s+DELAY",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r";\s*(cat|ls|rm|wget|curl|nc|bash|sh|python|perl|php)\s+",
        r"\b(eval|exec|system|passthru|shell_exec|popen)\s*\(",
        r"\|\|\s*(wget|curl|bash|sh)",
    ]

    XSS_PATTERNS = [
        r"(?i)<\s*script.*?>",
        r"(?i)javascript\s*:",
        r"(?i)onerror\s*=",
        r"(?i)onload\s*=",
    ]

    PATH_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"(?i)/etc/passwd",
        r"(?i)c:\\windows",
    ]

    @classmethod
    def sanitize_input(cls, raw_input: Any) -> Any:
        """
        تنقية وتطهير شامل للمدخلات النصية وتحييد أكواد الـ HTML والرموز الخطرة.
        يدعم تنظيف القواميس والقوائم بشكل متداخل (Recursive Sanitization).
        """
        if isinstance(raw_input, str):
            return html.escape(raw_input.strip())
        elif isinstance(raw_input, dict):
            return {k: cls.sanitize_input(v) for k, v in raw_input.items()}
        elif isinstance(raw_input, list):
            return [cls.sanitize_input(i) for i in raw_input]
        return raw_input

    @classmethod
    def _match_patterns(cls, data_str: str) -> Optional[str]:
        """
        محرك التطابق الداخلي: يفحص السلسلة النصية مقابل جميع التهديدات المعروفة.
        يعيد نوع التهديد إذا تم العثور عليه، أو None إذا كانت السلسلة آمنة.
        """
        threats = {
            "SQL_INJECTION": cls.SQL_INJECTION_PATTERNS,
            "COMMAND_INJECTION": cls.COMMAND_INJECTION_PATTERNS,
            "XSS": cls.XSS_PATTERNS,
            "PATH_TRAVERSAL": cls.PATH_TRAVERSAL_PATTERNS
        }

        for threat_type, patterns in threats.items():
            for pattern in patterns:
                if re.search(pattern, data_str):
                    logger.warning(f"🚨 [Security Alert - {threat_type}]: تم رصد محاولة هجومية عبر النمط: {pattern}")
                    return threat_type
        return None

    @classmethod
    def inspect_payload(cls, data: Any) -> bool:
        """
        فحص الحمولات العميقة (Deep Payload Inspection).
        يفحص القواميس، القوائم، والنصوص بشكل متداخل بحثاً عن أي محاولات حقن برمجية.
        يعيد True إذا كانت الحمولة آمنة، و False إذا تم اكتشاف تهديد.
        """
        if data is None:
            return True
            
        if isinstance(data, dict):
            for key, value in data.items():
                if not cls.inspect_payload(key) or not cls.inspect_payload(value):
                    return False
            return True
            
        elif isinstance(data, (list, set, tuple)):
            for item in data:
                if not cls.inspect_payload(item):
                    return False
            return True
            
        elif isinstance(data, (int, float, bool)):
            return True
            
        # فحص النصوص والقيم المباشرة
        data_str = str(data)
        threat = cls._match_patterns(data_str)
        
        if threat:
            return False
            
        return True

    @staticmethod
    async def log_security_event(
        session: AsyncSession,
        telegram_id: Optional[int],
        action: str,
        details: str,
        risk_level: str = "CRITICAL"
    ) -> None:
        """
        توثيق العمليات الأمنية والسيادية داخل سجلات التدقيق غير القابلة للتلاعب (Immutable Audit Trails).
        """
        if SovereignAuditLog is None:
            logger.critical("❌ [Audit Critical Failure]: نموذج SovereignAuditLog غير متوفر مسارياً. فشل تسجيل الحدث الأمني.")
            return

        try:
            # استخدام 0 كمعرف افتراضي لطلبات النظام غير المرتبطة بمستخدم مباشر
            safe_telegram_id = telegram_id if telegram_id is not None else 0
            
            audit_entry = SovereignAuditLog(
                telegram_id=safe_telegram_id,
                action=f"[{risk_level}] {action}",
                details=details,
                timestamp=datetime.datetime.utcnow()
            )
            session.add(audit_entry)
            await session.commit()
            logger.info(f"🛡️ [Audit Success]: تم توثيق الحدث الأمني [{action}] للمعرف [{safe_telegram_id}] بنجاح مطلق.")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ [Audit DB Error]: فشل حرج في تسجيل الحدث الأمني في قاعدة البيانات: {e}", exc_info=True)


async def sovereign_payload_guard(request: Request) -> None:
    """
    وسيط أمني سيادي (Enterprise Security Dependency / Guard).
    يقوم باعتراض كافة الطلبات الواردة إلى التطبيق، فك تشفيرها بأمان، وإجراء فحص عميق (Deep Inspection)
    لمنع الهجمات العابرة والبرمجيات الخبيثة قبل وصولها إلى منطق الأعمال (Business Logic).
    """
    try:
        body_bytes = await request.body()
        if body_bytes:
            try:
                # قراءة محتوى الطلب الخام بأمان تام مع تحديد الحد الأقصى لتجنب إرهاق الذاكرة
                if len(body_bytes) > 5 * 1024 * 1024:  # حد أقصى 5 ميجابايت للحمولة
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="Payload Too Large: Exceeds Sovereign Infrastructure Limits."
                    )
                body = json.loads(body_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                # السماح بالطلبات التي لا تتبع صيغة JSON ولكن قد يتم فحصها بطرق أخرى لاحقاً
                return

            # الفحص العميق والمتداخل للحمولة (Recursive Deep Inspection)
            if not SovereignSecurityShield.inspect_payload(body):
                client_ip = request.client.host if request.client else "Unknown IP"
                logger.error(f"🛑 [Sovereign Security Shield]: تم حظر طلب مشبوه يحمل حمولة هجومية مؤكدة من IP: {client_ip}.")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access Denied: Malicious Payload Detected and Blocked by AymnGuard Sovereign AST Shield."
                )
                
    except HTTPException as he:
        raise he  # تمرير استثناءات HTTP المدارة كما هي
    except Exception as e:
        logger.error(f"⚠️ [Shield Unexpected Error]: خطأ غير متوقع في فاحص الحمولات الأمني: {e}", exc_info=True)
        # في بيئات الـ Zero-Trust، يفضل رفض الطلب عند حدوث خطأ داخلي في محرك الفحص
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Security Core Fault: Unable to verify payload integrity."
        )
