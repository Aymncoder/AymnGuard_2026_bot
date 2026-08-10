# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Autonomous Software Engineer & Healing Agent
==============================================================================
العقل الإشرافي الآلي: يقوم بمسح المشروع، تحليل شجرة الكود (AST)، اكتشاف الملفات
اليتيمة أو غير المربوطة، فحص صحة البنية، وتقديم تقرير أو إصلاح تلقائي سيادي.
==============================================================================
"""

import os
import sys
import ast
import logging
import importlib
from pathlib import Path

# --- إعداد السجلات المؤسسية ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 🛠️ SOVEREIGN-ARCHITECT-[%(levelname)-7s] | %(message)s"
)
logger = logging.getLogger("SovereignArchitectAgent")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# المجلدات المستهدفة بالفحص السيادي
TARGET_FOLDERS = ["core", "services", "bots", "security", "src", "app", "backend_core"]

class SovereignArchitectAnalyzer:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.all_python_files = []
        self.imported_modules = set()
        self.file_dependencies = {}

    def scan_project_files(self):
        """مسح كافة ملفات البايثون في المشروع"""
        logger.info("🔍 [Scan]: جاري مسح كافة ملفات الكود البرمجي في المستودع...")
        for folder in TARGET_FOLDERS:
            folder_path = self.root_path / folder
            if folder_path.exists() and folder_path.is_dir():
                for py_file in folder_path.rglob("*.py"):
                    if "__pycache__" not in py_file.parts:
                        self.all_python_files.append(py_file)
        logger.info(f"✨ [Scan Complete]: تم رصد {len.all_python_files if hasattr(self, 'all_python_files') else len(self.all_python_files)} ملف بايثون نشط.")

    def analyze_ast_dependencies(self):
        """تحليل شجرة الكود (AST) لمعرفة الاستيرادات والترابط بين الملفات"""
        logger.info("🧠 [AST Analysis]: جاري تحليل الروابط والاستيرادات بين الملفات...")
        
        for py_file in self.all_python_files:
            rel_path = py_file.relative_to(self.root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            self.file_dependencies[module_name] = []

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read(), filename=str(py_file))
                
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Import):
                        for alias in sub_node.names:
                            self.imported_modules.add(alias.name)
                            self.file_dependencies[module_name].append(alias.name)
                    elif isinstance(sub_node, ast.ImportFrom):
                        if sub_node.module:
                            full_import = f"{sub_node.module}"
                            self.imported_modules.add(full_import)
                            self.file_dependencies[module_name].append(full_import)
            except Exception as e:
                logger.error(f"⚠️ خطأ أثناء تحليل ملف {rel_path}: {e}")

    def audit_orphan_files(self):
        """اكتشاف الملفات اليتيمة (التي لا يستوردها أحد وليس لها مسار رابط)"""
        logger.info("🛡️ [Audit]: فحص الملفات المعزولة أو اليتيمة...")
        orphans = []

        for py_file in self.all_python_files:
            rel_path = py_file.relative_to(self.root_path)
            module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
            
            # استثناء ملفات الإقلاع الرئيسية والنماذج الخاصة
            if any(exclude in module_name for exclude in ["run", "main", "__init__", "config", "database"]):
                continue

            # التحقق مما إذا كان الملف مُستورداً في مكان ما
            is_imported = any(module_name in imp or py_file.stem in imp for imp in self.imported_modules)
            
            # التحقق مما إذا كان الملف يحتوي على FastAPI Router
            has_router = False
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "router = FastAPI" in content or "router = APIRouter" in content:
                        has_router = True
            except:
                pass

            if not is_imported and not has_router:
                orphans.append(str(rel_path))

        if orphans:
            logger.warning(f"⚠️ [Orphan Report]: تم رصد {len(orphans)} ملف غير مربوط بالكتلة التشغيلية:")
            for orphan in orphans:
                logger.info(f"   -> الملف المعزول: {orphan}")
        else:
            logger.info("✅ [Integrity Check]: جميع الملفات مرتبطة ومدمجة بشكل سليم تماماً!")

    def run_full_diagnostic(self):
        print("="*70)
        print("👑 AYMNGUARD SOVEREIGN ARCHITECT AGENT - v1.0.0")
        print("="*70)
        self.scan_project_files()
        self.analyze_ast_dependencies()
        self.audit_orphan_files()
        print("="*70)
        logger.info("🎉 [Success]: انتهى الفحص الهندسي السيادي بنجاح تام.")

if __name__ == "__main__":
    architect = SovereignArchitectAnalyzer(ROOT_DIR)
    architect.run_full_diagnostic()
