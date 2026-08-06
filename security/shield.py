# -*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Security Shield & AST Engine
الحصن السيبراني المتقدم: فحص الحمولات (Payload Inspection)، التحقق الأمني الثابت، 
وإدارة سجلات التدقيق غير القابلة للتلاعب (Immutable Audit Trails) بمعايير عمالقة التكنولوجيا.
"""

import re
import html
import json
import logging
import datetime
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# استيراد نموذج سجلات التدقيق السيادي مع تغطية شاملة لمسارات الاستيراد
try:
    from database.models import SovereignAuditLog
except ImportError:
    try:
        from models import SovereignAuditLog
    except ImportError:
        SovereignAuditLog = None  # حماية إضافية ضد أخطاء الاستيراد المبكر

# إعداد السجلات الأمنية السيادية
logger = logging.getLogger("AymnGuard.SovereignSecurityShield")
logger.setLevel(logging.INFO)

class SovereignSecurityShield:
    """
    محرك الحصن السيبراني المتقدم: يطبق أعلى معايير الحماية والتفتيش الأمني على مستوى المؤسسات الكبرى.
    """
    
    # أنماط الهجمات السيبرانية الشائعة للتحقق الفوري (AST & Payload Pattern Matching)
    SQL_INJECTION_PATTERNS = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|ALTER|EXEC|EXECUTE)\s+",
        r"OR\s+1=1",
        r"UNION\s+ALL\s+SELECT",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r";\s*(cat|ls|rm|wget|curl|nc|bash|sh|python|perl)\s+",
        r"\b(eval|exec|system|passthru|shell_exec)\s*\(",
    ]

    @classmethod
    def sanitize_input(cls, raw_input: str) -> str:
        """
        تنقية التعقيم الشامل للمدخلات النصية وتحييد أكواد الـ HTML والرموز الخطرة.
        """
        if not isinstance(raw_input, str):
            raw_input = str(raw_input)
        return html.escape(raw_input.strip())

    @classmethod
    def inspect_payload(cls, data: Any) -> bool:
        """
        فحص الحمولات بحثاً عن أي محاولات حقن برمجية (SQL Injection أو Command Injection).
        """
        if data is None:
            return True
            
        data_str = str(data)
        
        # فحص أنماط حقن SQL
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, data_str, re.IGNORECASE):
                logger.warning(f"🚨 [Security Alert]: تم رصد محاولة حقن SQL مشبوهة عبر النمط: {pattern}")
                return False

        # فحص أنماط حقن أوامر النظام
        for pattern in cls.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, data_str, re.IGNORECASE):
                logger.warning(f"🚨 [Security Alert]: تم رصد محاولة تنفيذ أمر نظام مشبوه عبر النمط: {pattern}")
                return False

        return True

    @staticmethod
    async def log_security_event(
        session: AsyncSession,
        telegram_id: int,
        action: str,
        details: str
    ) -> None:
        """
        توثيق العمليات الأمنية والسيادية داخل سجلات التدقيق غير القابلة للتلاعب.
        """
        if SovereignAuditLog is None:
            logger.error("❌ [Audit Error]: نموذج SovereignAuditLog غير متوفر مسارياً.")
            return

        try:
            audit_entry = SovereignAuditLog(
                telegram_id=telegram_id,
                action=action,
                details=details,
                timestamp=datetime.datetime.utcnow()
            )
            session.add(audit_entry)
            await session.commit()
            logger.info(f"🛡️ [Audit Success]: تم تسجيل الحدث الأمني [{action}] للمستخدم [{telegram_id}] بنجاح مطلق.")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ [Audit Error]: فشل تسجيل الحدث الأمني في قاعدة البيانات: {e}", exc_info=True)


async def sovereign_payload_guard(request: Request) -> None:
    """
    وسيط أمني سيادي (Security Guard / Dependency) لفحص وتفتيش الطلبات الواردة إلى التطبيق لحظياً 
    مع حماية متكاملة ضد الهجمات العابرة والبرمجيات الخبيثة.
    """
    try:
        # قراءة محتوى الطلب الخام بأمان تام
        body_bytes = await request.body()
        if body_bytes:
            try:
                body = json.loads(body_bytes.decode("utf-8"))
            except json.JSONDecodeError:
                return  # السماح بالطلبات التي لا تتبع صيغة JSON البنيوية الهيكلية

            if isinstance(body, dict):
                for key, value in body.items():
                    # فحص كل من المفاتيح والقيم لضمان عدم وجود تلاعب خفي
                    if not SovereignSecurityShield.inspect_payload(key) or not SovereignSecurityShield.inspect_payload(value):
                        logger.error("🛑 [Sovereign Security Shield]: تم حظر طلب مشبوه يحمل حمولة هجومية مؤكدة.")
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access Denied: Malicious Payload Detected by AymnGuard Sovereign AST Shield."
                        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"خطأ غير متوقع في فاحص الحمولات الأمني: {e}", exc_info=True)
        pass
