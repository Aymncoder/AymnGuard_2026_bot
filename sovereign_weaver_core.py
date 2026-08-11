import os
import sys

def weave_code_snippet(target_file, snippet_code):
    print(f"⚙️ جاري فحص الملف: {target_file}")
    if not os.path.exists(target_file):
        print(f"❌ خطأ: الملف غير موجود!")
        return False

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # تنظيف الكود وإزالة أي علامات غريبة
    clean_snippet = snippet_code.strip()
    if clean_snippet.startswith("```"):
        lines = clean_snippet.splitlines()
        if len(lines) > 2:
            clean_snippet = "\n".join(lines[1:-1]).strip()

    if clean_snippet in content:
        print("ℹ️ ملاحظة: الكود موجود مسبقاً، لا داعي للتكرار.")
        return True

    # الإضافة الآمنة في نهاية الملف
    updated_content = content + f"\n\n// --- تم الحقن الآلي بواسطة المحرك السيادي ---\n{clean_snippet}\n"

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("🎯 نجاح: تم دمج الكود البرمجي في الملف بدقة.")
    return True

if __name__ == "__main__":
    target = os.getenv("TARGET_FILE", "")
    snippet = os.getenv("CODE_SNIPPET", "")
    
    if target and snippet:
        success = weave_code_snippet(target, snippet)
        if not success:
            sys.exit(1)
    else:
        print("❌ خطأ: بيانات مفقودة، تأكد من المسار والكود.")
        sys.exit(1)
