# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v17.0.0 : Sovereign Cognitive AI Auditor
==============================================================================
المُراجع الإدراكي الآلي: وكيل ذكاء اصطناعي يعمل ككبير مهندسين لتدقيق التحديثات
البرمجية، تحليل المنطق المالي، فحص الثغرات الأمنية (العقود الذكية/المنصات)، 
ومنع أي ترقيع برمجي يضعف البنية التحتية للنظام السيادي.
==============================================================================
"""

import os
import sys
import asyncio
import httpx
import logging
from typing import Optional

# =============================================================================
# 1. إعداد السجلات المؤسسية
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Sovereign-AI-Auditor] %(levelname)s: %(message)s"
)
logger = logging.getLogger("AymnGuard.CognitiveAuditor")

# =============================================================================
# 2. تكوين المتغيرات البيئية (Environment Variables)
# =============================================================================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AI_AGENT_API_KEY = os.getenv("AI_AGENT_API_KEY")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

if not all([GITHUB_TOKEN, AI_AGENT_API_KEY, GITHUB_REPOSITORY, PR_NUMBER]):
    logger.error(" المتغيرات البيئية غير مكتملة. لا يمكن إقلاع الوكيل الإدراكي.")
    sys.exit(1)

# =============================================================================
# 3. الدستور السيادي الصارم للذكاء الاصطناعي (The Sovereign AI Constitution)
# =============================================================================
SOVEREIGN_SYSTEM_PROMPT = """
أنت الآن كبير مهندسي النظم ومدقق الأمن السيبراني (Principal Architect & Security Lead) لنظام AymnGuard Enterprise.
مهمتك هي مراجعة التحديثات البرمجية (Pull Requests) بصرامة لا تقبل المساومة.

يجب عليك تطبيق القواعد السيادية التالية أثناء التدقيق:

1. الحظر التام للترقيع الأعمى (No Monkey-Patching):
   - إذا وجدت كوداً ضعيفاً أو يعالج مشكلة سطحياً، ارفضه تماماً واطلب إعادة هيكلة (Refactoring) جذرية. لا تقترح حلولاً مؤقتة.

2. كفاءة الأداء المفرطة (Algorithmic & Big-O Efficiency):
   - دقق في الحلقات التكرارية (Loops) واستعلامات قواعد البيانات. ارفض أي كود تتجاوز تعقيداته الزمانية O(n log n) في معالجة البيانات الضخمة. ابحث بصرامة عن تسرب الذاكرة (Memory Leaks).

3. النزاهة المالية والتداول (Financial & Trading Logic Integrity):
   - عند مراجعة خوارزميات استدعاء الأسعار، أو محركات إدارة المخاطر، تأكد من عدم وجود أخطاء في حسابات الفاصلة العائمة (Floating-point math). 
   - حذر من أي منطق قد يؤدي إلى تصفية خاطئة للمراكز المالية (Liquidation Logic Flaws) أو تأخير في التنفيذ.

4. أمان العقود الذكية واللامركزية (Smart Contract & Web3 Security):
   - إذا تضمن الكود لغة Solidity أو تكامل مع شبكات (مثل BNB Chain)، ابحث فوراً عن ثغرات هجوم إعادة الدخول (Reentrancy)، التلاعب بالزمن، وتجاوز حدود الغاز.

5. الأمان ذو الثقة المعدومة (Zero-Trust Security):
   - ابحث عن مفاتيح الـ API المشفرة أو المكشوفة.
   - تأكد من وجود فحص صارم لتدفق البيانات وتنقيتها (Data Sanitization) قبل تخزينها أو تنفيذها.

صيغة الرد المطلوبة (بصيغة Markdown ليتم نشرها كتعليق في GitHub):
- **القرار الهندسي (Verdict):** [قبول مبدئي / يتطلب تغييرات جوهرية / مرفوض أمنياً]
- **الثغرات الأمنية والمالية (Critical Vulnerabilities):** (إن وجدت)
- **كفاءة الأداء (Performance & Big-O):** (تحليل استهلاك الذاكرة والمعالجة)
- **مقترحات إعادة الهيكلة (Architectural Refactoring):** (قدم الكود البديل الخارق هنا)
"""

# =============================================================================
# 4. محرك الاستدعاء والاتصال اللوجستي
# =============================================================================
class CognitiveAuditorAgent:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3.diff"
        }
        self.pr_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{PR_NUMBER}"

    async def fetch_pr_diff(self) -> str:
        """جلب الكود المُحدث من GitHub بصيغة Diff لمعرفته وتحليله"""
        logger.info(f"جاري سحب بيانات الكود لطلب السحب رقم #{PR_NUMBER}...")
        async with httpx.AsyncClient() as client:
            response = await client.get(self.pr_url, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"فشل جلب الكود من GitHub: {response.text}")
                sys.exit(1)
            return response.text

    async def analyze_with_ai(self, diff_content: str) -> str:
        """إرسال الكود للوكيل الإدراكي لتحليله بناءً على الدستور السيادي"""
        logger.info("جاري ضخ الكود إلى العقل الإدراكي للتحليل المؤسسي...")
        
        ai_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={AI_AGENT_API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": SOVEREIGN_SYSTEM_PROMPT},
                    {"text": f"قم بمراجعة هذا الكود المحدث (Diff) بصرامة:\n\n{diff_content}"}
                ]
            }]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(ai_api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except KeyError:
                    return "خطأ في قراءة رد الذكاء الاصطناعي."
            else:
                logger.error(f"فشل الاتصال بمحرك الذكاء الاصطناعي: {response.text}")
                return "تعذر إكمال المراجعة الإدراكية بسبب خطأ في الخادم."

    async def post_review_comment(self, review_text: str):
        """نشر التقرير السيادي كتعليق رسمي داخل طلب السحب في GitHub"""
        logger.info("جاري تدوين القرار الهندسي في مستودع GitHub...")
        comment_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{PR_NUMBER}/comments"
        
        payload = {"body": f"### مراجعة العقل الإدراكي السيادي (AI Cognitive Audit)\n\n{review_text}"}
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(comment_url, headers=headers, json=payload)
            if response.status_code == 201:
                logger.info("تم نشر التقرير الإدراكي بنجاح تام.")
            else:
                logger.error(f"فشل نشر التعليق: {response.text}")

async def main():
    auditor = CognitiveAuditorAgent()
    diff_content = await auditor.fetch_pr_diff()
    
    if not diff_content.strip():
        logger.info("لا توجد تغييرات جوهرية في الكود لتدقيقها.")
        return

    ai_review = await auditor.analyze_with_ai(diff_content)
    await auditor.post_review_comment(ai_review)

if __name__ == "__main__":
    asyncio.run(main())
