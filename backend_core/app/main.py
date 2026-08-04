"""
=============================================================================
AymnGuard Enterprise - Main Execution File
القلب النابض للمنصة: تجميع النواة الخلفية مع الواجهة الأمامية في بيئة تشغيل واحدة
=============================================================================
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# استدعاء مجمع المسارات المركزي الذي يحتوي على التحقق من تيليجرام
from app.api.v1.api import api_router

# تهيئة تطبيق FastAPI بمعايير مؤسسية
app = FastAPI(
    title="AymnGuard Enterprise Logistics",
    description="النواة الخلفية الآمنة للمنصة اللوجستية وتطبيق تيليجرام المصغر",
    version="1.0.0",
    docs_url="/api/docs", # واجهة اختبار المطورين
    redoc_url="/api/redoc"
)

# 1. إعدادات CORS: السماح لتطبيق تيليجرام بالتواصل المباشر مع الخادم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # سيتم تقييدها بنطاق التشفير في بيئة الإنتاج القصوى
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. ربط مجمع المسارات (الـ API) بالنظام
app.include_router(api_router, prefix="/api/v1")

# 3. دمج الواجهة الأمامية (Frontend Mini App) لتعمل من نفس الخادم
# تحديد مسار مجلد الواجهة الأمامية الذي قمنا ببنائه
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../frontend_core/mini_app")

# استضافة الواجهة كملفات ثابتة (Static Files) لتعمل بمجرد فتح الرابط الأساسي
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    print(f"⚠️ تحذير: مجلد الواجهة الأمامية غير موجود في المسار {FRONTEND_DIR}")

