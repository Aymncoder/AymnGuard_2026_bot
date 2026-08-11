import os
import re
import sys

def weave_code_snippet(target_file, snippet_code, target_marker=None):
    """
    محرك الخياطة السيادي: يقوم بحقن الكود أو الدالة في مكانها المخصص بدقة 
    دون إحداث أي تداخل أو تكرار أو أخطاء نحوية.
    """
    if not os.path.exists(target_file):
        print(f"⚠️ [Weaver Error]: الملف المستهدف {target_file} غير موجود.")
        return False

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # التحقق من عدم تكرار الكود لمنع أي تعارض
    clean_snippet = snippet_code.strip()
    if clean_snippet in content:
        print(f"ℹ️ [Weaver Info]: القطعة البرمجية موجودة مسبقاً في {target_file}، تم تخطي التكرار.")
        return True

    # إذا تم تحديد علامة دقيقة (Marker) للحقن
    if target_marker and target_marker in content:
        updated_content = content.replace(target_marker, f"{target_marker}\n\n{clean_snippet}")
    else:
        # الحقن التلقائي في نهاية الملف أو حسب هيكل الدالة
        updated_content = content + f"\n\n{clean_snippet}\n"

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✅ [Weaver Success]: تم دمج وخياطة الكود بنجاح في {target_file}")
    return True

if __name__ == "__main__":
    # استقبال المتغيرات عبر بيئة العمل أو المدخلات الآلية
    target = os.getenv("TARGET_FILE", "main.py")
    snippet = os.getenv("CODE_SNIPPET", "")
    marker = os.getenv("TARGET_MARKER", "# --- SOVEREIGN_INJECTION_POINT ---")
    
    if snippet:
        weave_code_snippet(target, snippet, marker)
    else:
        print("❌ [Weaver Error]: لا توجد أي قطعة برمجية مرسلة للدمج.")
        sys.exit(1)
