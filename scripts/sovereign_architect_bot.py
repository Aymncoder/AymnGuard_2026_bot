# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Ultimate Unified Ecosystem & Auto-Wiring Engine
==============================================================================
المهندس الإمبراطوري الشامل: يفحص النظام البيئي، يراجع ملفات التبعيات والإعدادات،
يكشف الخدمات المعزولة، ويقوم بالحقن والربط التلقائي في النواة الكبرى (main.py).
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
    format="%(asctime)s | 👑 SOVEREIGN-ULTIMATE-ENGINE-[%(levelname)-7s] | %(message)s"
)
logger = logging.getLogger("SovereignUltimateEngine")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TARGET_FOLDERS = ["core", "services", "bots", "security", "src", "app", "backend_core"]

class SovereignUltimateEngine:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.all_python_files = []
        self.config_files = []
        self.orphan_routers = []
        self.ai_api_key = os.getenv("AI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.main_py_path = self.root_path / "backend_core" / "main.py"

    def scan_ecosystem(self):
        """مسح شامل لكافة مكونات النظام البيئي، الأكواد، والإعدادات"""
        logger.info("🔍 [Ecosystem Scan]: بدء المسح الشامل للبنية التحتية والتبعيات...")
        
        # 1. مسح ملفات بايثون
        for folder in TARGET_FOLDERS:
            folder_path = self.root_path / folder
            if folder_path.exists() and folder_path.is_dir():
                for py_file in folder_path.rglob("*.py"):
                    if "__pycache__" not in py_file.parts:
                        self.all_python_files.append(py_file)

        # 2. مسح ملفات الإعدادات والتبعيات
        req_file = self.root_path / "requirements.txt"
        if req_file.exists():
            self.config_files.append(req_file)
            
        workflows_dir = self.root_path / ".github" / "workflows"
        if workflows_dir.exists():
            for yml_file in workflows_dir.rglob("*.yml"):
                self.config_files.append(yml_file)

        logger.info(f"✨ [Scan Complete]: تم رصد {len(self.all_python_files)} ملف برمجي و {len(self.config_files)} ملف إعدادات سحابي.")

    def detect_and_wire_routers(self):
        """كشف الخدمات والمسارات غير المربوطة وحقنها تلقائياً في النواة الكبرى"""
        logger.info("⚙️ [Auto-Wiring Engine]: فحص وترشيح المسارات للربط التلقائي...")
        
        main_content = ""
        if self.main_py_path.exists():
            with open(self.main_py_path, "r", encoding="utf-8") as f:
                main_content = f.read()

        for py_file in self.all_python_files:
            rel_path = py_file.relative_to(self.root_path)
            if any(exc in str(rel_path) for exc in ["run.py", "main.py", "sovereign_architect_bot.py"]):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "router = APIRouter" in content or "router = FastAPI" in content:
                        module_import_str = str(rel_path.with_suffix('')).replace(os.sep, '.')
                        if py_file.stem not in main_content:
                            self.orphan_routers.append((py_file, module_import_str))
            except Exception as e:
                logger.error(f"⚠️ خطأ أثناء فحص الملف {rel_path}: {e}")

        if not self.orphan_routers:
            logger.info("✨ [Auto-Wire]: كافة المسارات والخدمات مرتبطة ومدمجة بالكامل بالنواة.")
            return

        if not self.main_py_path.exists():
            logger.error("❌ [Error]: ملف النواة الكبرى backend_core/main.py غير موجود!")
            return

        with open(self.main_py_path, "r", encoding="utf-8") as f:
            main_lines = f.readlines()

        added_imports_count = 0
        injection_index = -1

        for idx, line in enumerate(main_lines):
            if "app = FastAPI" in line or "app = APIRouter" in line:
                injection_index = idx + 1
                break

        if injection_index == -1:
            injection_index = len(main_lines)

        new_injection_code = []
        for py_file, module_str in self.orphan_routers:
            router_name = f"{py_file.stem}_router"
            import_line = f"from {module_str} import router as {router_name}\n"
            include_line = f"app.include_router({router_name})\n"
            
            if import_line not in ''.join(main_lines):
                new_injection_code.append(import_line)
                new_injection_code.append(include_line)
                added_imports_count += 1
                logger.info(f"🔗 [Wired]: تمت إضافة وربط الخدمة تلقائياً: {module_str}")

        if added_imports_count > 0:
            main_lines[injection_index:injection_index] = ["\n# --- Auto-Wired by Sovereign Ultimate Engine ---\n"] + new_injection_code
            
            with open(self.main_py_path, "w", encoding="utf-8") as f:
                f.writelines(main_lines)
            
            logger.info(f"🎉 [Success]: تم حقن وربط {added_imports_count} خدمة جديدة بنجاح في واجهات التطبيق المركزية.")

    def run(self):
        print("="*70)
        print("👑 AYMNGUARD SOVEREIGN ULTIMATE UNIFIED ENGINE - v6.0.0")
        print("="*70)
        self.scan_ecosystem()
        self.detect_and_wire_routers()
        print("="*70)
        logger.info("🚀 [Complete]: اكتملت دورة الفحص، المراجعة، والربط الإمبراطوري الشامل.")

if __name__ == "__main__":
    engine = SovereignUltimateEngine(ROOT_DIR)
    engine.run()
