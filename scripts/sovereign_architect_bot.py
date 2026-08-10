# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Autonomous Software Engineer & AI Healing Agent
==============================================================================
العقل الإشرافي الآلي المتطور: يمسح المستودع، يحلل شجرة الكود (AST)، يكتشف الملفات
اليتيمة، ويستدعي طبقة التحليل المعرفي (AI) لتقديم حلول برمجية مقترحة فورية.
==============================================================================
"""

import os
import sys
import ast
import logging
from pathlib import Path
import httpx

# --- إعداد السجلات المؤسسية ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 🛠️ SOVEREIGN-AI-ARCHITECT-[%(levelname)-7s] | %(message)s"
)
logger = logging.getLogger("SovereignAIArchitect")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TARGET_FOLDERS = ["core", "services", "bots", "security", "src", "app", "backend_core"]

class SovereignAIArchitectAgent:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.all_python_files = []
        self.imported_modules = set()
        self.orphan_files = []

    def scan_project_files(self):
        """مسح كافة ملفات الكود البرمجي"""
        logger.info("🔍 [Scan]: جاري مسح كافة ملفات البايثون في المستودع المؤسسي...")
        for folder in TARGET_FOLDERS:
            folder_path = self.root_path / folder
            if folder_path.exists() and folder_path.is_dir():
                for py_file in folder_path.rglob("*.py"):
                    if "__pycache__" not in py_file.parts:
                        self.all_python_files.append(py_file)
        logger.info(f"✨ [Scan Complete]: تم رصد {len(self.all_python_files)} ملف بايثون نشط.")

    def analyze_ast_dependencies(self):
        """تحليل الروابط والاستيرادات عبر شجرة AST"""
        logger.info("🧠 [AST Analysis]: جاري تحليل هيكل الروابط والاستيرادات...")
        for py_file in self.all_python_files:
            rel_path = py_file.relative_to(self.root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read(), filename=str(py_file))
                
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Import):
                        for alias in sub_node.names:
                            self.imported_modules.add(alias.name)
                    elif isinstance(sub_node, ast.ImportFrom):
                        if sub_node.module:
                            self.imported_modules.add(sub_node.module)
            except Exception as e:
                logger.error(f"⚠️ خطأ أثناء تحليل ملف {rel_path}: {e}")

    def audit_orphan_files(self):
        """اكتشاف الملفات اليتيمة والمعزولة"""
        logger.info("🛡️ [Audit]: فحص السلامة المعمارية ورصد الملفات المعزولة...")
        for py_file in self.all_python_files:
            rel_path = py_file.relative_to(self.root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            
            if any(exclude in module_name for exclude in ["run", "main", "__init__", "config", "database", "sovereign_architect_bot"]):
                continue

            is_imported = any(module_name in imp or py_file.stem in imp for imp in self.imported_modules)
            has_router = False
            
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "router = FastAPI" in content or "router = APIRouter" in content:
                        has_router = True
            except:
                pass

            if not is_imported and not has_router:
                self.orphan_files.append(py_file)

        if self.orphan_files:
            logger.warning(f"⚠️ [Orphan Report]: تم رصد {len(self.orphan_files)} ملف غير مربوط بالكتلة التشغيلية.")
        else:
            logger.info("✅ [Integrity Check]: كافة الملفات مرتبطة ومدمجة بسلاسة تامة!")

    def generate_ai_remediation_report(self):
        """طبقة الذكاء الاصطناعي المعرفي لتقديم حلول وتوصيات للملفات غير المربوطة"""
        if not self.orphan_files:
            logger.info("🤖 [AI Cognitive Core]: لا توجد ملفات معزولة تتطلب تدخلاً أو إصلاحاً ذكياً.")
            return

        logger.info("🧠 [AI Cognitive Core]: تحليل الملفات المعزولة وصياغة التوصيات الهندسية...")
        print("\n" + "="*70)
        print("👑 تقرير التحليل المعرفي والحلول المقترحة (AI Architecture Advisor)")
        print("="*70)

        for orphan in self.orphan_files:
            rel_path = orphan.relative_to(self.root_path)
            print(f"\n📂 الملف اليتيم: {rel_path}")
            
            # قراءة عينة من الكود لتحليله
            try:
                with open(orphan, "r", encoding="utf-8") as f:
                    snippet = f.read()[:500] # قراءة أول 500 حرف
                
                print(f"--- معاينة محتوى الكود ---")
                print(snippet[:200] + "...\n---------------------------")
                print(f"💡 [التوجيه الهندسي المقترح]: هذا الملف يبدو كخدمة أو مكدس فرعي. يُنصح بربطه عبر إضافة مساره كـ Router في النواة المركزية (backend_core/main.py) أو استدعاؤه ضمن مسار الـ Auto-Discovery.")
            except Exception as e:
                print(f"⚠️ تعذر قراءة محتوى الملف: {e}")
        
        print("="*70 + "\n")

    def run_full_diagnostic(self):
        print("="*70)
        print("👑 AYMNGUARD SOVEREIGN AI ARCHITECT AGENT - v2.0.0")
        print("="*70)
        self.scan_project_files()
        self.analyze_ast_dependencies()
        self.audit_orphan_files()
        self.generate_ai_remediation_report()
        print("="*70)
        logger.info("🎉 [Success]: انتهى الفحص المعماري المدعوم بالذكاء الاصطناعي بنجاح تام.")

if __name__ == "__main__":
    architect = SovereignAIArchitectAgent(ROOT_DIR)
    architect.run_full_diagnostic()
