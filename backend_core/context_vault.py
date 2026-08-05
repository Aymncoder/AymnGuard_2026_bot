# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Context Vault (Memory Management)
==============================================================================
خزنة الذاكرة السياقية: مسؤولة عن تذكر سياق المستخدمين وحالة الجلسات (Sessions)
لمنع تكرار معالجة البيانات، تقليل الضغط على المحرك العصبي، وتسريع الاستجابة.
"""

import logging
from typing import Dict, Any, Optional
import time

# إعداد مسجل الأحداث لطبقة الذاكرة
logger = logging.getLogger("AymnGuard.ContextVault")

class ContextVault:
    """
    نظام ذاكرة فائق السرعة يعتمد على الذاكرة الحية (In-Memory) كبداية.
    مصمم معمارياً (Adapter Pattern) ليرتبط بقواعد بيانات ضخمة (مثل Redis) لاحقاً 
    دون الحاجة لتغيير أي سطر كود في باقي النظام.
    """
    
    # قاموس الذاكرة المركزي: يخزن البيانات مع منع التداخل بين المستخدمين
    _memory_store: Dict[str, Dict[str, Any]] = {}
    
    # مدة بقاء الذاكرة قبل التدمير التلقائي (هنا محددة بساعة واحدة لضمان أمان البيانات)
    _ttl_seconds: int = 3600  

    @classmethod
    async def store_context(cls, user_id: str, context_data: Dict[str, Any]) -> None:
        """
        تخزين حالة أو سياق المستخدم مع ختم زمني دقيق.
        """
        cls._memory_store[user_id] = {
            "data": context_data,
            "timestamp": time.time()
        }
        logger.info(f"💾 [Context Vault]: Context securely saved for user: {user_id}")

    @classmethod
    async def retrieve_context(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """
        استرجاع سياق المستخدم لحظياً، مع فحص صلاحية انتهاء الجلسة.
        """
        record = cls._memory_store.get(user_id)
        if not record:
            return None
        
        # تفعيل قاطع أمان زمني: مسح البيانات تلقائياً إذا انتهت صلاحيتها
        if time.time() - record["timestamp"] > cls._ttl_seconds:
            logger.info(f"⏳ [Context Vault]: Context expired for user: {user_id}. Auto-clearing...")
            await cls.clear_context(user_id)
            return None
            
        logger.debug(f"⚡ [Context Vault]: Ultra-fast retrieval for user: {user_id}")
        return record["data"]

    @classmethod
    async def clear_context(cls, user_id: str) -> None:
        """
        التدمير الآمن لسياق المستخدم (يُستخدم فور انتهاء المعاملة أو تسجيل الخروج).
        """
        if user_id in cls._memory_store:
            del cls._memory_store[user_id]
            logger.info(f"🧹 [Context Vault]: Context permanently cleared for user: {user_id}")
