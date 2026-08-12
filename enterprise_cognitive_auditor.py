# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v17.1.0 : Sovereign Cognitive AI Auditor (Cloud CI/CD)
==============================================================================
المُراجع الإدراكي الآلي: وكيل ذكاء اصطناعي يعمل ككبير مهندسين لتدقيق التحديثات
البرمجية، تحليل المنطق المالي، فحص الثغرات الأمنية (العقود الذكية/المنصات)، 
ومنع أي ترقيع برمجي يضعف البنية التحتية للنظام السيادي.
تم التحديث: بيئة سحابية خالية من الرموز، معالجة استثناءات صارمة، وإيقاف الأنابيب.
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
    format="%(asctime)s [%(levelname)s] Sovereign-AI-Auditor: %(message)s",
    stream=sys.stdout
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
    logger.error("[Fatal]: المتغيرات البيئية غير مكتملة. لا يمكن إقلاع الوكيل الإدراكي.")
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
   - إذا تضمن الكود لغة Solidity أو تكامل مع شبكات، ابحث فوراً عن ثغرات هجوم إعادة الدخول (Reentrancy)، التلاعب بالزمن، وتجاوز حدود الغاز.

5. الأمان ذو الثقة المعدومة (Zero-Trust Security):
   - ابحث عن مفاتيح الـ API المشفرة أو المكشوفة.
   - تأكد من وجود فحص صارم لتدفق البيانات وتنقيتها (Data Sanitization) قبل تخزينها أو تنفيذها.

صيغة الرد المطلوبة (بصيغة Markdown ليتم نشرها كتعليق في GitHub):
- Decision: [APPROVED / REQUIRES_CHANGES / REJECTED_SECURITY_RISK]
- Critical Vulnerabilities: (إن وجدت)
- Performance & Big-O: (تحليل استهلاك الذاكرة والمعالجة)
- Architectural Refactoring: (قدم الكود البديل الخارق هنا)
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
        logger.info(f"[Fetch]: جاري سحب بيانات الكود لطلب السحب رقم #{PR_NUMBER}...")
        try:
            # إضافة Timeout صارم لـ 30 ثانية
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.pr_url, headers=self.headers)
                response.raise_for_status()
                # حماية من تجاوز الذاكرة في طلبات السحب الضخمة جداً
                return response.text[:20000]
        except Exception as e:
            logger.error(f"[Error]: فشل جلب الكود من GitHub: {e}")
            sys.exit(1)

    async def analyze_with_ai(self, diff_content: str) -> str:
        """إرسال الكود للوكيل الإدراكي لتحليله بناءً على الدستور السيادي"""
        logger.info("[Analyze]: جاري ضخ الكود إلى العقل الإدراكي للتحليل المؤسسي...")
        
        ai_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={AI_AGENT_API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": SOVEREIGN_SYSTEM_PROMPT},
                    {"text": f"قم بمراجعة هذا الكود المحدث (Diff) بصرامة:\n\n{diff_content}"}
                ]
            }]
        }

        try:
            # مهلة أطول للذكاء الاصطناعي ليفكر براحة
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(ai_api_url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error(f"[Error]: فشل الاتصال بمحرك الذكاء الاصطناعي: {e}")
            return "[Error]: تعذر إكمال المراجعة الإدراكية بسبب خطأ في الخادم."

    async def post_review_comment(self, review_text: str):
        """نشر التقرير السيادي كتعليق رسمي داخل طلب السحب في GitHub"""
        logger.info("[Post]: جاري تدوين القرار الهندسي في مستودع GitHub...")
        comment_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{PR_NUMBER}/comments"
        
        payload = {"body": f"### مراجعة العقل الإدراكي السيادي (AI Cognitive Audit)\n\n{review_text}"}
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(comment_url, headers=headers, json=payload)
                response.raise_for_status()
                logger.info("[Success]: تم نشر التقرير الإدراكي بنجاح تام.")
        except Exception as e:
            logger.error(f"[Error]: فشل نشر التعليق: {e}")

        # إجراء سيادي: إيقاف الأنابيب (CI/CD) إذا تم اكتشاف ثغرة لمنع دمج الكود
        if "REJECTED_SECURITY_RISK" in review_text or "REQUIRES_CHANGES" in review_text:
            logger.error("[Action]: تم رفض الكود أمنياً أو هندسياً! إيقاف عملية البناء فوراً (Exit 1).")
            sys.exit(1)

async def main():
    auditor = CognitiveAuditorAgent()
    diff_content = await auditor.fetch_pr_diff()
    
    if not diff_content or not diff_content.strip():
        logger.info("[Info]: لا توجد تغييرات جوهرية في الكود لتدقيقها.")
        return

    ai_review = await auditor.analyze_with_ai(diff_content)
    await auditor.post_review_comment(ai_review)

if __name__ == "__main__":
    asyncio.run(main())
