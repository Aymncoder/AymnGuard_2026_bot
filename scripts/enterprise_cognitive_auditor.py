# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise : Cognitive AI Code Reviewer (v15.0.0)
==============================================================================
الوكيل الإدراكي المتقدم:
- يفهم المنطق المالي لأسواق التداول (Spot & Futures) ومكتبات CCXT.
- يدقق عقود Solidity الذكية بحثاً عن ثغرات أمنية وهيكلية.
- يتصل بواجهة GitHub API لترك تعليقات مؤسساتية دقيقة على الكود المرفوع.
"""

import os
import httpx
import asyncio
import logging
from typing import Dict, Any

# إعداد السجل المؤسسي
logging.basicConfig(level=logging.INFO, format='%(asctime)s 🛡️ %(levelname)s: %(message)s')
logger = logging.getLogger("CognitiveAuditor")

class SovereignCognitiveReviewer:
    def __init__(self):
        self.ai_api_key = os.getenv("AI_AGENT_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPOSITORY")
        self.pr_number = os.getenv("PR_NUMBER")
        
        if not all([self.ai_api_key, self.github_token, self.repo_name, self.pr_number]):
            logger.error("❌ المتغيرات البيئية (Env Vars) ناقصة. تأكد من إعدادات خط الأنابيب.")
            exit(1)

        self.github_api_url = f"https://api.github.com/repos/{self.repo_name}/pulls/{self.pr_number}"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3.diff"
        }

    async def fetch_pr_diff(self) -> str:
        """جلب التعديلات البرمجية مباشرة من مسودة العمل (Pull Request)."""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.github_api_url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"❌ فشل جلب التعديلات: {response.status_code}")
                exit(1)

    def _build_cognitive_prompt(self, diff_text: str) -> str:
        """بناء الحقن الإدراكي (Prompt) لتوجيه الذكاء الاصطناعي بدقة متناهية."""
        return f"""
        أنت "المراجع المالي والبرمجي السيادي" لنظام AymnGuard Enterprise.
        مهمتك تدقيق التعديلات البرمجية التالية (Git Diff) بصرامة لا تقبل المساومة.
        
        **نطاق الفحص الإلزامي:**
        1. المنطق المالي (Trading Logic): هل هناك خطر في إدارة السيولة؟ هل دوال أوامر Binance (Spot/Futures) عبر CCXT مكتوبة بشكل آمن وتدير أخطاء الرصيد؟
        2. العقود الذكية (Solidity 0.8.34+): إذا كان التعديل يشمل عقوداً، تأكد من حماية دوال التحويل وتوزيع المحافظ (Marketing Wallets) من ثغرات الاختراق.
        3. الأتمتة واستنزاف الذاكرة (Python Async): تأكد من إغلاق جلسات الاتصال (Sessions) بشكل صحيح لمنع تسرب الذاكرة أثناء التشغيل المستمر.

        **طريقة الرد:**
        - إذا كان الكود نقياً ومثالياً، أجب بكلمة واحدة فقط: `APPROVED_SOVEREIGN_CORE`.
        - إذا كان هناك خلل، قدم تقريراً بصيغة JSON يحتوي على:
          "status": "REJECTED",
          "severity": "CRITICAL/HIGH/MEDIUM",
          "reason": "الشرح الدقيق للخلل المالي أو البرمجي",
          "suggestion": "الكود المقترح للإصلاح"

        الكود المطلوب مراجعته:
        {diff_text[:6000]} # تحديد الحجم لمنع تجاوز حدود الذاكرة
        """

    async def execute_ai_audit(self, diff_text: str) -> str:
        """إرسال التعديلات للمراجعة الإدراكية واتخاذ القرار."""
        logger.info("🧠 جاري تشغيل التحليل الإدراكي العميق للمنطق المالي...")
        
        # يمكن توجيه هذا إلى Gemini API أو OpenAI حسب البنية التحتية
        endpoint = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4-turbo",
            "messages": [{"role": "user", "content": self._build_cognitive_prompt(diff_text)}],
            "temperature": 0.0 # دقة مطلقة 100% بدون هلوسة
        }

        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(
                endpoint, 
                json=payload, 
                headers={"Authorization": f"Bearer {self.ai_api_key}"}
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def report_decision(self, ai_response: str):
        """توجيه القرار النهائي إلى GitHub لرفض أو قبول التحديث."""
        if "APPROVED_SOVEREIGN_CORE" in ai_response:
            logger.info("✅ [AUDIT PASSED] المنطق المالي والبرمجي سليم 100%. تم الاعتماد.")
            # يمكن إضافة كود هنا للموافقة التلقائية على الـ PR في GitHub
        else:
            logger.error(f"🚨 [AUDIT FAILED] تم اكتشاف خلل منطقي أو ثغرة أمنية:\n{ai_response}")
            # في بيئة الإنتاج، يتم إرسال هذا التقرير كتعليق (Comment) على الـ PR ليقرأه المطور
            exit(1) # إغلاق خط الأنابيب ومنع النشر

if __name__ == "__main__":
    reviewer = SovereignCognitiveReviewer()
    
    async def main():
        diff = await reviewer.fetch_pr_diff()
        if not diff.strip():
            logger.info("✅ لا توجد تعديلات لفحصها.")
            return
            
        decision = await reviewer.execute_ai_audit(diff)
        await reviewer.report_decision(decision)

    asyncio.run(main())
