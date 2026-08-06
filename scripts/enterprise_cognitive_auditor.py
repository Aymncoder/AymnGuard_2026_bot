# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v100.0.0 : The Sovereign AI Hive-Mind & Cognitive Enforcer
==============================================================================
الدمج الأعظم (The Ultimate Integration):
بنية السرب الديناميكي المتعدد (Dynamic Multi-Agent Swarm) مدمجة مع قوة 
"الوكيل الإدراكي المالي" الصارمة.

الميزات الحصرية المدمجة:
1. التوجيه الديناميكي (Dynamic Routing): استدعاء وكلاء متخصصين بناءً على محتوى الكود.
2. التحليل المالي والسيادي (Cognitive Audit): فهم عميق لـ CCXT، Spot/Futures، والسيولة.
3. تدقيق العقود (Solidity 0.8.34+): حماية محافظ التسويق وثغرات الاختراق.
4. الإجماع الهرمي (Supreme Consensus): محكمة إجماع نهائية تصدر تقريراً شاملاً.
5. الاعتماد الصارم (Strict Enforcer): الرد بصيغة JSON، وإيقاف خطوط الأنابيب (exit 1) 
   تلقائياً إذا تم اكتشاف أي ثغرة، لمنع النشر في خوادم الإنتاج.
==============================================================================
"""

import os
import sys
import asyncio
import httpx
import logging
import json
from typing import List, Dict

# =============================================================================
# 1. إعداد السجلات المؤسسية
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s 🌌 [Sovereign-Hive-Mind] %(levelname)s: %(message)s"
)
logger = logging.getLogger("AymnGuard.UltimateSwarm")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AI_AGENT_API_KEY = os.getenv("AI_AGENT_API_KEY")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

if not all([GITHUB_TOKEN, AI_AGENT_API_KEY, GITHUB_REPOSITORY, PR_NUMBER]):
    logger.error("❌ المتغيرات البيئية مفقودة. فشل إقلاع العقل الجمعي السيادي.")
    sys.exit(1)

# =============================================================================
# 2. مستودع الوكلاء الاستراتيجيين (The Cognitive Swarm Registry)
# تم دمج دساتير "الوكيل الإدراكي" داخل تخصصات السرب الديناميكي
# =============================================================================
SWARM_AGENTS = [
    {
        "name": "👔 كبير المهندسين الماليين (Finance Core)",
        "is_core": True,
        "prompt": """أنت الوكيل المالي السيادي. ركز حصرياً على:
1. المنطق المالي وخوارزميات التداول (Spot & Futures).
2. هل هناك خطر في إدارة السيولة؟ هل دوال أوامر منصات التداول عبر مكتبات مثل (CCXT) مكتوبة بشكل آمن وتدير أخطاء الرصيد؟
3. الانزلاق السعري (Slippage) وحسابات الفاصلة العائمة.
قدم تحليلاً صارماً، وحذر من أي منطق قد يؤدي إلى تصفية مالية خاطئة."""
    },
    {
        "name": "🛡️ قائد الأمن السيبراني (CyberSec Lead)",
        "is_core": True,
        "prompt": """أنت خبير الأمن السيبراني. ركز حصرياً على:
1. ثغرات الحقن (Injections)، مفاتيح API المكشوفة، ونموذج (Zero-Trust).
2. الأتمتة واستنزاف الذاكرة (Python Async): تأكد من إغلاق جلسات الاتصال (Sessions) بشكل صحيح لمنع تسرب الذاكرة.
ابحث بصرامة عن الثغرات القاتلة وقيّم مستوى الخطورة."""
    },
    {
        "name": "⚡ مهندس كفاءة الأداء (Big-O Optimizer)",
        "is_core": True,
        "prompt": """أنت مهندس الأداء. قم بتحليل التعقيد الزمني والمكاني (Time/Space Complexity).
ارفض أي استعلام قاعدة بيانات متداخل أو استهلاك عشوائي للذاكرة في بيئات التشغيل المستمر."""
    },
    {
        "name": "📜 قاضي العقود الذكية واللامركزية (Web3 & Solidity)",
        "is_core": False,
        "trigger_keywords": [".sol", "web3", "ethers", "contract", "token", "bnb", "erc20"],
        "prompt": """أنت خبير بلوكشين (Solidity 0.8.34+). دقق في العقود الذكية:
1. تأكد من حماية دوال التحويل وتوزيع المحافظ (Marketing Wallets) من ثغرات الاختراق.
2. ابحث عن هجمات (Reentrancy)، تلاعب (Timestamp)، وثغرات (Overflow/Underflow)."""
    },
    {
        "name": "🗄️ مهندس قواعد البيانات (Database Architect)",
        "is_core": False,
        "trigger_keywords": [".sql", "sqlalchemy", "models", "schema", "migration", "alembic", "db"],
        "prompt": "أنت خبير قواعد البيانات. راجع استعلامات ORM، كفاءة الفهارس، وتأكد من عدم وجود تسريب للبيانات الحساسة."
    },
    {
        "name": "🎨 خبير تجربة المستخدم والواجهات (UI/UX Architect)",
        "is_core": False,
        "trigger_keywords": [".html", ".css", ".js", ".tsx", ".jsx", "frontend", "react", "vue"],
        "prompt": "أنت خبير الواجهات. تأكد من الأمان في الواجهة (منع XSS) وتوافقية العرض (Responsive Design)."
    },
    {
        "name": "⚙️ خبير التشغيل والبنية التحتية (DevOps & Docker)",
        "is_core": False,
        "trigger_keywords": ["docker", "yaml", "yml", "kubernetes", "ci", "cd", "nginx"],
        "prompt": "أنت مهندس DevOps. دقق في ملفات الإعدادات وتأكد من عدم تشغيل الخدمات بصلاحيات Root لضمان الأمان التشغيلي."
    }
]

# =============================================================================
# 3. محرك العقل الجمعي والإجماع السيادي (Hive-Mind & Cognitive Orchestrator)
# =============================================================================
class UltimateSovereignOrchestrator:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3.diff"}
        self.pr_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{PR_NUMBER}"
        # الاعتماد الكامل على النماذج الأقوى لضمان الدقة المطلقة
        self.ai_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={AI_AGENT_API_KEY}"

    async def fetch_pr_diff(self) -> str:
        logger.info(f"📥 سحب سياق طلب السحب #{PR_NUMBER} للتحليل الإدراكي...")
        async with httpx.AsyncClient() as client:
            response = await client.get(self.pr_url, headers=self.headers)
            if response.status_code != 200:
                logger.error("❌ فشل سحب الكود من GitHub.")
                sys.exit(1)
            return response.text[:15000] # حماية من تجاوز حدود الذاكرة (Memory Limits)

    def determine_active_agents(self, diff_content: str) -> List[Dict]:
        active_agents = []
        diff_lower = diff_content.lower()
        
        for agent in SWARM_AGENTS:
            if agent.get("is_core"):
                active_agents.append(agent)
            elif any(keyword in diff_lower for keyword in agent.get("trigger_keywords", [])):
                active_agents.append(agent)
                
        logger.info(f"🚨 تم استدعاء {len(active_agents)} وكلاء من سرب الذكاء الاصطناعي.")
        return active_agents

    async def consult_agent(self, agent: Dict, code_diff: str) -> Dict[str, str]:
        logger.info(f"🧠 استشارة {agent['name']}...")
        payload = {
            "contents": [{"parts": [{"text": agent['prompt']}, {"text": f"دقق هذا الكود (Git Diff):\n\n{code_diff}"}]}]
        }
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            try:
                response = await client.post(self.ai_endpoint, json=payload)
                response.raise_for_status()
                reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return {"name": agent['name'], "report": reply}
            except Exception as e:
                logger.error(f"⚠️ خطأ في وكيل {agent['name']}: {str(e)}")
                return {"name": agent['name'], "report": "⚠️ تعذر الفحص بسبب خطأ في الاستجابة."}

    async def supreme_judge_consensus(self, agent_reports: List[Dict[str, str]]) -> str:
        logger.info("⚖️ إحالة التقارير إلى القاضي السيادي لإصدار القرار المالي والبرمجي الصارم...")
        
        reports_text = "\n\n".join([f"### تقرير {r['name']}:\n{r['report']}" for r in agent_reports])
        
        judge_prompt = """

        أنت "القاضي السيادي (The Supreme Architect)" لنظام AymnGuard.
        مهمتك مراجعة تقارير السرب المرفقة واتخاذ قرار تنفيذي قطعي لا يقبل المساومة.
        
:قواعد القرار الإلزامي:  
        - إذا اتفقت التقارير على أن الكود نقي، مثالي، وآمن مالياً وبرمجياً 100%، يجب أن تبدأ تقريرك بالكلمة السحرية: `APPROVED_SOVEREIGN_CORE`.
        - إذا اكتشف أي وكيل خللاً (تسرب ذاكرة، ثغرة عقد ذكي، خطأ في المنطق المالي)، يجب أن تصدر حكمك بصيغة JSON واضحة ضمن التقرير تحتوي على:
          ```json
          {
            "status": "REJECTED",
            "severity": "CRITICAL/HIGH/MEDIUM",
            "reason": "الشرح الدقيق للخلل",
            "suggestion": "الكود المقترح للإصلاح"
          }
          
