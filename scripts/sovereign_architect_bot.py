# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Enterprise : Sovereign Living Omniscient Engine v34.3.0
==============================================================================
المهندس الإمبراطوري الأسمى (الجيل 34.3 - فحص صحة المفاتيح والتنفيذ عبر مشاريع متعددة):
- دالة فحص صحة المفاتيح التلقائية (Automatic Key Health Validator).
- ترتيب المفاتيح واستبعاد المعطلة أو المستنفدة قبل بدء فريق الوكلاء.
- نظام النوايا السيادية مع الحصانة المطلقة ضد قيود الـ API.
==============================================================================
"""

import sys
import os
import json
import re
import logging
from pathlib import Path
import asyncio
import ast
import hashlib
import time

try:
    from google import genai
    AI_MODULE_AVAILABLE = True
except ImportError:
    AI_MODULE_AVAILABLE = False

class StructuredJsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "engine": "SovereignSupremeEngine-v34.3",
            "message": record.getMessage()
        }
        return json.dumps(log_record, ensure_ascii=False)

logger = logging.getLogger("SovereignSupremeEngine343")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(StructuredJsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TARGET_FOLDERS = ["core", "services", "bots", "security", "src", "app", "backend_core"]
STATE_FILE_PATH = ROOT_DIR / ".sovereign_state.json"
INTENT_FILE_PATH = ROOT_DIR / "sovereign_intent.txt"

class SovereignSupremeEngineV343:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.all_python_files = []
        self.delta_files = []
        self.main_py_path = self.root_path / "backend_core" / "main.py"
        self.state_data = self.load_sovereign_state()
        
        # تجميع كافة المفاتيح المحتملة من جميع المشاريع المنفصلة
        raw_keys = [
            os.getenv("GEMINI_API_KEY", ""),
            os.getenv("GEMINI_API_KEY_SECONDARY", ""),
            os.getenv("GEMINI_API_KEY_PROJECT2", ""),
            os.getenv("AI_API_KEY", "")
        ]
        # إزالة الفراغات والتكرارات
        self.raw_keys = list(dict.fromkeys([k.strip() for k in raw_keys if k and k.strip() != ""]))
        self.valid_keys = []
        self.current_key_index = 0
        
        # تشغيل دالة فحص صحة المفاتيح فور الانطلاق
        self.validate_and_rank_api_keys()
        self.client = self._get_active_client()

        self.telemetry = {
            "intents_processed": 0,
            "scanned_files": 0,
            "delta_processed": 0,
            "routers_wired": 0,
            "valid_keys_count": len(self.valid_keys)
        }

    def validate_and_rank_api_keys(self):
        """🔒 دالة فحص صحة المفاتيح التلقائية (Automatic Key Health Validator)"""
        logger.info("🔍 [SECURITY]: بدء فحص صحة المفاتيح التلقائي وتقييم الجاهزية...")
        if not AI_MODULE_AVAILABLE or not self.raw_keys:
            logger.warning("⚠️ لا توجد مفاتيح مدخلة أو مكتبة google-genai غير مجهزة.")
            return

        verified_keys = []
        for index, key in enumerate(self.raw_keys):
            masked_key = f"{key[:6]}...{key[-4:]}"
            try:
                test_client = genai.Client(api_key=key)
                # اختبار استجابة سريع وخفيف لضمان عمل المفتاح وعدم تجاوزه للحصة
                test_response = test_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents="Ping"
                )
                if test_response and test_response.text:
                    verified_keys.append(key)
                    logger.info(f"✅ [KEY VALID]: المفتاح رقم {index+1} ({masked_key}) سليم وجاهز 100%.")
            except Exception as e:
                logger.warning(f"❌ [KEY INVALID/EXHAUSTED]: المفتاح رقم {index+1} ({masked_key}) محظور أو مستنفد: {e}")

        self.valid_keys = verified_keys
        logger.info(f"🛡️ [SECURITY REPORT]: إجمالي المفاتيح الشغالة بنجاح: {len(self.valid_keys)} من أصل {len(self.raw_keys)}")

    def _get_active_client(self):
        if not AI_MODULE_AVAILABLE or not self.valid_keys:
            return None
        key = self.valid_keys[self.current_key_index % len(self.valid_keys)]
        return genai.Client(api_key=key)

    def _rotate_key(self):
        if len(self.valid_keys) > 1:
            self.current_key_index += 1
            logger.info(f"🔄 [AUTO ROTATION]: التبديل تلقائياً إلى المفتاح الشغال رقم {self.current_key_index + 1}")
            self.client = self._get_active_client()

    def load_sovereign_state(self) -> dict:
        if STATE_FILE_PATH.exists():
            try:
                with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_sovereign_state(self):
        try:
            with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.state_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ تعذر حفظ الذاكرة السيادية: {e}")

    def compute_file_hash(self, file_path: Path) -> str:
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                hasher.update(f.read())
            return hasher.hexdigest()
        except Exception:
            return ""

    async def orchestrate_multi_agent_swarm(self):
        """غرفة عمليات الوكلاء الذكية المعتمدة على المفاتيح المفحوصة والمحصنة"""
        if not INTENT_FILE_PATH.exists():
            return

        with open(INTENT_FILE_PATH, "r", encoding="utf-8") as f:
            intent_text = f.read().strip()

        if not intent_text or intent_text.lower() in ["", "none", "done", "تم الإنجاز بنجاح بواسطة فريق الوكلاء الذكي."]:
            return

        logger.info(f"🌐 [AI SWARM v34.3]: استلام الفكرة والمباشرة بالتصنيع: '{intent_text[:50]}...'")
        
        if not self.client:
            logger.error("❌ لا توجد مفاتيح API صالحة حالياً لتشغيل فريق العمل.")
            return

        prompt = f"""
أنت تمثل شركة برمجيات عالمية عملاقة تعمل كفريق واحد متكامل (مهندس معماري، مطور واجهات/هياكل، مطور خلفي متقدم).
المشروع هو نظام FastAPI سيادي ومتقدم.
رغبة العميل والفكرة المطلوبة: "{intent_text}"

قم بتوليد الأكواد اللازمة لتحقيق هذه الفكرة بالكامل. 
مخرجاتك يجب أن تكون بصيغة JSON فقط، حيث يكون المفتاح هو مسار الملف (مثلاً services/omega_fabric.py) والقيمة هي الكود البرمجي الكامل بلغة بايثون. لا تكتب أي نصوص خارج الـ JSON.
يجب أن تحتوي الملفات على `APIRouter` إذا كانت تقدم خدمة ويب، وأن تكون متزامنة وخالية من الأخطاء النحوية المطلقة.
"""
        max_attempts = max(len(self.valid_keys) * 2, 2)
        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                response_text = response.text
                
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = response_text
                    
                generated_files = json.loads(json_str)
                
                for file_path_str, code_content in generated_files.items():
                    target_path = self.root_path / file_path_str
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(code_content)
                    logger.info(f"🏗️ [AI Architect]: فريق العمل أتم بناء الملف وتصميمه -> {file_path_str}")
                    self.telemetry["intents_processed"] += 1
                
                with open(INTENT_FILE_PATH, "w", encoding="utf-8") as f:
                    f.write("تم الإنجاز بنجاح بواسطة فريق الوكلاء الذكي.")
                break
                
            except Exception as e:
                logger.warning(f"⚠️ تنبيه في محاولة الاستدعاء {attempt + 1}: {e}")
                if "429" in str(e) or "Resource Exhausted" in str(e):
                    self._rotate_key()
                    time.sleep(2)
                else:
                    if attempt < max_attempts - 1:
                        time.sleep(4)
                    else:
                        logger.error("❌ فشل استدعاء الذكاء الاصطناعي بعد تجربة كافة المفاتيح المفحوصة.")

    def scan_ecosystem_with_delta(self):
        logger.info("🔍 بدء المسح الراداري التفاضلي (Delta Engine Scan)...")
        for folder in TARGET_FOLDERS:
            folder_path = self.root_path / folder
            if folder_path.exists() and folder_path.is_dir():
                for py_file in folder_path.rglob("*.py"):
                    if "__pycache__" not in py_file.parts:
                        self.all_python_files.append(py_file)
                        rel_path_str = str(py_file.relative_to(self.root_path))
                        current_hash = self.compute_file_hash(py_file)
                        
                        if rel_path_str not in self.state_data or self.state_data[rel_path_str] != current_hash:
                            self.delta_files.append(py_file)
                            self.state_data[rel_path_str] = current_hash

        self.telemetry["scanned_files"] = len(self.all_python_files)
        self.telemetry["delta_processed"] = len(self.delta_files)

    def delta_enterprise_wiring(self):
        logger.info("🔗 تشغيل محرك الربط العصبي التفاضلي بالنواة المركزية (main.py)...")
        if not self.main_py_path.exists():
            return

        with open(self.main_py_path, "r", encoding="utf-8") as f:
            main_code = f.read()

        try:
            tree = ast.parse(main_code)
        except Exception:
            tree = None

        registered_modules = set()
        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    registered_modules.add(node.module)

        new_imports = []
        new_inclusions = []

        for py_file in self.delta_files:
            rel_path = py_file.relative_to(self.root_path)
            if any(exc in str(rel_path) for exc in ["run.py", "main.py", "sovereign_architect_bot.py"]):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content)
                
                if "router =" in content:
                    mod_str = str(rel_path.with_suffix('')).replace(os.sep, '.')
                    if mod_str not in registered_modules:
                        router_alias = f"{py_file.stem}_router"
                        new_imports.append(f"from {mod_str} import router as {router_alias}")
                        new_inclusions.append(f"app.include_router({router_alias})")
                        self.telemetry["routers_wired"] += 1
                        logger.info(f"⚡ ربط تفاضلي آمن للملف المستحدث بالنواة -> {mod_str}")
            except Exception as e:
                logger.error(f"⚠️ خطأ أثناء المعالجة لـ {rel_path}: {e}")

        if new_imports or new_inclusions:
            injection_block = "\n# --- Sovereign Enterprise AI-Generated Bridges v34.3 ---\n" + "\n".join(new_imports) + "\n" + "\n".join(new_inclusions) + "\n"
            updated_main_code = injection_block + "\n" + main_code
            with open(self.main_py_path, "w", encoding="utf-8") as f:
                f.write(updated_main_code)
            logger.info("🎉 تم حقن وربط مسارات الذكاء الاصطناعي بنجاح مؤسسي مطلق.")
        
        self.save_sovereign_state()

    async def async_run(self):
        await self.orchestrate_multi_agent_swarm()
        self.scan_ecosystem_with_delta()
        self.delta_enterprise_wiring()

    def run(self):
        print("="*85)
        print("👑 AYMNGUARD SOVEREIGN ENTERPRISE : SUPREME ENGINE - v34.3.0 (KEY HEALTH VALIDATED)")
        print("="*85)
        asyncio.run(self.async_run())
        print("\n" + "="*85)
        print(f"📊 IMPERIAL AI SWARM REPORT (v34.3):")
        print(f"   * Verified Valid API Keys: {self.telemetry['valid_keys_count']}")
        print(f"   * AI Intents Executed:     {self.telemetry['intents_processed']}")
        print(f"   * Total Ecosystem Files:   {self.telemetry['scanned_files']}")
        print(f"   * Delta Files Audited:     {self.telemetry['delta_processed']}")
        print(f"   * AI Routers Safely Wired: {self.telemetry['routers_wired']}")
        print("👑 SYSTEM STATUS: 100% AUTONOMOUS AI FACTORY SYNCHRONIZED")
        print("="*85 + "\n")

if __name__ == "__main__":
    engine = SovereignSupremeEngineV343(ROOT_DIR)
    engine.run()
