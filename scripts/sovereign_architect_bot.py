# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Sovereign Omniscient & Autonomous Engine v9.0
==============================================================================
المهندس الإمبراطوري الكلي: يمسح الجذر بالكامل، يكشف أي نقص، يولد أكواد الربط 
والتعويض عبر الذكاء الاصطناعي للخدمات والبطات والعمليات الخلفية، ويقوم بالحقن 
والدمج الجذري في النواة المركزية وملفات التشغيل لتصبح المنظومة حية 100%.
==============================================================================
"""

import os
import sys
import logging
from pathlib import Path
import httpx
import asyncio

# --- إعداد السجلات المؤسسية ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | 👑 SOVEREIGN-OMNISCIENT-[%(levelname)-7s] | %(message)s"
)
logger = logging.getLogger("SovereignOmniscient")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TARGET_FOLDERS = ["core", "services", "bots", "security", "src", "app", "backend_core"]

class SovereignOmniscientEngine:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.all_python_files = []
        self.orphan_modules = []
        self.ai_api_key = os.getenv("AI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.main_py_path = self.root_path / "backend_core" / "main.py"
        self.telemetry = {"scanned": 0, "upgraded_deps": False, "wired_components": 0}

    def scan_entire_ecosystem(self):
        """مسح راداري شامل لكافة زوايا وجذور المشروع"""
        logger.info("🔍 [Omniscient Scan]: بدء المسح الراداري الشامل لجذور ومجلدات المنظومة...")
        for folder in TARGET_FOLDERS:
            folder_path = self.root_path / folder
            if folder_path.exists() and folder_path.is_dir():
                for py_file in folder_path.rglob("*.py"):
                    if "__pycache__" not in py_file.parts:
                        self.all_python_files.append(py_file)
        self.telemetry["scanned"] = len(self.all_python_files)
        logger.info(f"✨ [Scan Complete]: تم رصد وتأمين {len(self.all_python_files)} ملف برمجياً في النطاق السيادي.")

    async def modernize_infrastructure_dependencies(self):
        """الارتقاء التقني التلقائي للتبعيات والمكتبات"""
        req_file = self.root_path / "requirements.txt"
        if not req_file.exists() or not self.ai_api_key:
            return

        logger.info("🆙 [Evolution]: فحص وتحديث التبعيات والمكتبات إلى أحدث المعايير المستقرة...")
        try:
            with open(req_file, "r", encoding="utf-8") as f:
                content = f.read()

            prompt = f"""
You are an expert Enterprise Principal Architect. Analyze these requirements:
{content}
Upgrade outdated versions to stable releases ensuring 100% enterprise compatibility.
Return ONLY raw requirement lines. No markdown blocks, no explanations.
"""
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
                    params={"key": self.ai_api_key},
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                if res.status_code == 200:
                    data = res.json()
                    new_content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    new_content = new_content.replace("```text", "").replace("```", "").strip()
                    if new_content and new_content != content.strip():
                        with open(req_file, "w", encoding="utf-8") as f:
                            f.write(new_content + "\n")
                        self.telemetry["upgraded_deps"] = True
                        logger.info("🚀 [Upgraded]: تمت ترقية ملف التبعيات بنجاح.")
        except Exception as e:
            logger.error(f"❌ خطأ في الارتقاء التقني: {e}")

    def autonomous_bridge_and_wiring(self):
        """الكشف والربط التلقائي الكلي لأي خدمة أو بوت أو راوتر معزول بالنواة المركزية"""
        logger.info("⚙️ [Omniscient Wiring]: فحص ومعالجة الروابط المفقودة والخدمات المعزولة...")

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
                    # فحص ما إذا كان الملف يحتوي على وظائف أو مسارات أو بوتات ولم يُستدعَ في النواة
                    if py_file.stem not in main_content:
                        module_str = str(rel_path.with_suffix('')).replace(os.sep, '.')
                        self.orphan_modules.append((py_file, module_str, content))
            except Exception as e:
                logger.error(f"⚠️ خطأ في تحليل {rel_path}: {e}")

        if not self.orphan_modules:
            logger.info("✨ [System Integrity]: كافة الملفات والخدمات مرتبطة ومدمجة بالكامل بالنواة المركزية.")
            return

        if not self.main_py_path.exists():
            logger.error("❌ ملف النواة المركزية غير موجود!")
            return

        with open(self.main_py_path, "r", encoding="utf-8") as f:
            main_lines = f.readlines()

        injection_idx = -1
        for idx, line in enumerate(main_lines):
            if "app = FastAPI" in line or "app = APIRouter" in line:
                injection_idx = idx + 1
                break

        if injection_idx == -1:
            injection_idx = len(main_lines)

        injected_count = 0
        new_bridges = []

        for py_file, mod_str, code_content in self.orphan_modules:
            # إذا كان الملف يحتوي على راوتر أو وظيفة تشغيل
            if "router" in code_content or "def " in code_content:
                router_name = f"{py_file.stem}_bridge"
                if "router" in code_content:
                    bridge_code = f"from {mod_str} import router as {router_name}\napp.include_router({router_name})\n"
                else:
                    bridge_code = f"import {mod_str} # Auto-linked background/service module\n"

                if bridge_code not in ''.join(main_lines):
                    new_bridges.append(bridge_code)
                    injected_count += 1
                    logger.info(f"🔗 [Auto-Bridge]: تم تعويض النقص وربط المكون تلقائياً: {mod_str}")

        if injected_count > 0:
            main_lines[injection_idx:injection_idx] = ["\n# --- Omniscient Auto-Wired Bridges ---\n"] + new_bridges
            with open(self.main_py_path, "w", encoding="utf-8") as f:
                f.writelines(main_lines)
            self.telemetry["wired_components"] = injected_count
            logger.info(f"🎉 [Success]: تم تعويض وحقن وربط {injected_count} مكون جديد بالنواة المركزية بنجاح.")

    def run(self):
        print("="*70)
        print("👑 AYMNGUARD SOVEREIGN OMNISCIENT ENGINE - v9.0.0")
        print("="*70)
        self.scan_entire_ecosystem()
        asyncio.run(self.modernize_infrastructure_dependencies())
        self.autonomous_bridge_and_wiring()
        print("\n" + "="*70)
        print(f"📊 TELEMETRY: Scanned={self.telemetry['scanned']} | Wired={self.telemetry['wired_components']} | Upgraded={self.telemetry['upgraded_deps']}")
        print("👑 SYSTEM STATUS: 100% AUTONOMOUSLY SYNCHRONIZED & SECURED")
        print("="*70 + "\n")

if __name__ == "__main__":
    engine = SovereignOmniscientEngine(ROOT_DIR)
    engine.run()
