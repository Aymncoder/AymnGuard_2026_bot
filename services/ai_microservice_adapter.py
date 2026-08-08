# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : AI Forge Microservice Adapter (v18.0.0)
==============================================================================
مهايئ ميكروسيرفس الذكاء الاصطناعي المستقل: يغلف محرك الـ AGI والتحليل العصبي
ويسجله كخدمة معزولة داخل المنصة المركزية (SovereignPlatformHub).
"""

import logging
from typing import Dict, Any
from src.ai_engine import SovereignAIEngineCore
from core.sovereign_platform_hub import SovereignPlatformHub

logger = logging.getLogger("AegisAICore.AIMicroserviceAdapter")
logger.setLevel(logging.INFO)

async def ai_forge_service_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    معالج الخدمة المستقل للذكاء الاصطناعي: يستقبل السياق، نوع المهمة، ودرجة الإبداع،
    ويوجهها لعقل الـ AGI العصبي دون أي تداخل مع الخدمات الأخرى.
    """
    license_key = payload.get("license_key", "AG-STANDALONE-KEY")
    prompt = payload.get("prompt", "")
    task_type = payload.get("task_type", "general_analysis")
    temperature = payload.get("temperature", 0.7)
    max_tokens = payload.get("max_tokens", 1024)

    try:
        result = await SovereignAIEngineCore.process_neural_query(
            license_key=license_key,
            prompt=prompt,
            task_type=task_type,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return {
            "service": "ai_neural_forge",
            "status": "success",
            "neural_output": result
        }
    except Exception as e:
        logger.error(f"❌ [AI Microservice Error]: {str(e)}", exc_info=True)
        return {
            "service": "ai_neural_forge",
            "status": "error",
            "error": str(e)
        }

# تسجيل ميكروسيرفس الذكاء الاصطناعي تلقائياً في المنصة المستقلة
SovereignPlatformHub.register_service(
    service_id="sovereign_ai_forge",
    service_name="Enterprise AGI Neural Forge Microservice",
    handler_func=ai_forge_service_handler,
    metadata={
        "version": "18.0.0",
        "isolation_level": "absolute",
        "models": ["Aegis-AGI-v18", "Sovereign-Linguistic-Core"]
    }
)

logger.info("🧠 [AI Microservice]: تم عزل وتسجيل محرك الذكاء الاصطناعي بنجاح كخدمة مستقلة.")
