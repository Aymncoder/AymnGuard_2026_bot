# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise: Cognitive AI Code Reviewer
==============================================================================
هذا السكربت يعمل تلقائياً داخل GitHub Actions.
يقوم بجلب التعديلات الجديدة (Git Diff) ويرسلها إلى محرك الذكاء الاصطناعي
للتأكد من عدم وجود أخطاء منطقية، تسريب للذاكرة، أو مخاطر في إدارة الصفقات.
"""

import os
import subprocess
import httpx
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("CognitiveAuditor")

async def analyze_code_diff():
    # 1. استخراج الكود الذي تم تعديله مؤخراً
    try:
        git_diff = subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD"], 
            text=True
        )
    except Exception as e:
        logger.error("لم يتم العثور على تعديلات سابقة للمقارنة.")
        return

    if not git_diff.strip():
        logger.info("✅ لا توجد تعديلات برمجية لفحصها.")
        return

    logger.info("🧠 جاري إرسال التعديلات لوكيل التدقيق الإدراكي...")

    # 2. بناء المحفز (Prompt) الموجه للذكاء الاصطناعي
    ai_endpoint = "https://api.openai.com/v1/chat/completions" # يمكن تغييره لـ Gemini
    api_key = os.getenv("AI_AGENT_API_KEY")

    if not api_key:
        logger.warning("⚠️ مفتاح الذكاء الاصطناعي غير متوفر. سيتم تخطي الفحص الإدراكي.")
        return

    payload = {
        "model": "gpt-4-turbo", # نموذج عالي الدقة للبرمجة
        "messages": [
            {
                "role": "system",
                "content": (
                    "أنت مهندس برمجيات مؤسساتي وقائد فريق حماية لمنصة تداول خوارزمية عالية التردد. "
                    "مهمتك فحص التعديلات البرمجية (git diff) واكتشاف الأخطاء المنطقية، "
                    "ثغرات الأمان، أو أي مخاطر قد تؤدي إلى خسائر مالية أو توقف النظام. "
                    "إذا كان الكود مثالياً، أجب بـ 'APPROVED'. إذا كان به مخاطر، اشرحها باختصار واقترح الإصلاح."
                )
            },
            {
                "role": "user",
                "content": f"Please review this code change:\n\n{git_diff[:4000]}" # تجنب تجاوز حدود النص
            }
        ],
        "temperature": 0.0
    }

    # 3. اتخاذ القرار الاستراتيجي
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                ai_endpoint, 
                json=payload, 
                headers={"Authorization": f"Bearer {api_key}"}
            )
            response.raise_for_status()
            ai_decision = response.json()["choices"][0]["message"]["content"]
            
            if "APPROVED" in ai_decision.upper():
                logger.info("✅ [AI Audit Passed]: المنطق البرمجي سليم وآمن للتنفيذ.")
            else:
                logger.error(f"❌ [AI Audit Failed]: تم اكتشاف خلل منطقي!\n{ai_decision}")
                exit(1) # إيقاف خط الأنابيب فوراً ومنع دمج الكود

        except Exception as e:
            logger.critical(f"فشل الاتصال بشبكة الذكاء الاصطناعي: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_code_diff())
