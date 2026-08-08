# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Trading, Market & Web3 Microservice Adapter (v18.0.0)
==============================================================================
مهايئ ميكروسيرفس الأسواق المالية والتداول وتدقيق عقود Web3:
يعزل التحليلات الفنية، مؤشرات الأسواق، وتدقيق البلوكتشين ضمن صندوق أسود آمن تماماً،
حتى تظل النواة الرئيسية مستقرة وخالية من أي استثناءات مالية أو تقنية.
"""

import logging
from typing import Dict, Any

try:
    from core.market_engine import SovereignMarketEngine
    from core.web3_nexus import SovereignWeb3Nexus
except ImportError:
    SovereignMarketEngine = None
    SovereignWeb3Nexus = None

from core.sovereign_platform_hub import SovereignPlatformHub

logger = logging.getLogger("AegisAICore.TradingMarketMicroservice")
logger.setLevel(logging.INFO)

async def trading_market_service_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    معالج الخدمة المستقل للأسواق والتداول:
    يستقبل طلب التحليل الفني للعملات أو تدقيق العقود الذكية وينفذه بمعزل تام.
    """
    action = payload.get("action", "market_analysis")
    
    try:
        # 1. مسار التحليل المالي وأسواق التداول
        if action == "market_analysis":
            symbol = payload.get("symbol", "BTCUSDT").upper()
            market_engine = SovereignMarketEngine() if SovereignMarketEngine else None
            
            if not market_engine:
                return {"status": "warning", "message": "محرك الأسواق غير مهيأ محلياً، تم تفعيل وضع الاستجابة الآمنة."}
                
            analysis_result = await market_engine.execute_market_analysis(symbol=symbol)
            return {
                "service": "trading_market_microservice",
                "action": "market_analysis",
                "status": "success",
                "data": analysis_result
            }

        # 2. مسار تدقيق عقود البلوكتشين (Web3 Audit)
        elif action == "audit_contract":
            contract_address = payload.get("contract_address", "0x...")
            web3_nexus = SovereignWeb3Nexus() if SovereignWeb3Nexus else None
            
            if not web3_nexus:
                return {"status": "warning", "message": "محرك Web3 غير مهيأ محلياً."}
                
            audit_result = await web3_nexus.audit_smart_contract(contract_address=contract_address)
            return {
                "service": "trading_market_microservice",
                "action": "audit_contract",
                "status": "success",
                "data": audit_result
            }

        else:
            return {
                "status": "error",
                "message": f"الإجراء '{action}' غير مدعوم في ميكروسيرفس الأسواق."
            }

    except Exception as e:
        logger.error(f"❌ [Trading Microservice Critical Error]: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "service": "trading_market_microservice",
            "error": str(e),
            "message": "حدث استثناء معزول في وحدة الأسواق وتم حماية النواة بنجاح."
        }

# تسجيل الميكروسيرفس تلقائياً في النواة الأم
SovereignPlatformHub.register_service(
    service_id="sovereign_trading_market",
    service_name="Enterprise Trading, Market & Web3 Microservice",
    handler_func=trading_market_service_handler,
    metadata={
        "version": "18.0.0",
        "isolation_level": "absolute",
        "capabilities": ["market_analysis", "smart_contract_audit", "crypto_risk_management"]
    }
)

logger.info("📈 [Trading Microservice]: تم عزل وتسجيل محرك الأسواق والتداول بنجاح تام.")
