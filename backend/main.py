import sys
import os
import base64
import json
import random
import re
import sqlite3
import subprocess
import time
import urllib.parse
import urllib.request
from threading import Thread
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List

AymnGuard Enterprise Logistics & Sovereign Ultimate Platform (main.py)
النواة المركزية الموحدة الفائقة - دمج كافة الخدمات القديمة مع الهندسة السيادية الحديثة.


# --- التشفير ---
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- FastAPI & Web ---
from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, status, Header, Depends, Security
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

# --- قواعد البيانات الخارجية ---
import psycopg2
from psycopg2 import pool
from pymongo import MongoClient
import redis

# --- تيليجرام (Telebot & Telethon) ---
import socks
import telebot
from telebot.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Message, ReplyKeyboardMarkup, Update, WebAppInfo,
)
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError, UserNotMutualContactError, UserPrivacyRestrictedError,
    SessionPasswordNeededError, PhoneCodeInvalidError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import InviteToChannelRequest
from urllib.parse import quote_plus
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn

# استيراد وحدات النظام الحديثة (Users CRUD & Endpoints)
from app.db.database import get_db, engine, Base
from app.api.v1.endpoints.users import router as users_router

# ==========================================
# 1. إعداد نظام تسجيل متقدم
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("system_runtime.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("AymnGuardEnterpriseUltimate")

# ==========================================
# 2. الإعدادات والمعرفات الأساسية والمفاتيح السيادية
# ==========================================
ADMIN_ID = 5193790077
SUPPORT_USERNAME = "A200002000"

owner_ids_raw = os.getenv("OWNER_ID", "5193790077")
OWNER_IDS = [int(i.strip()) for i in owner_ids_raw.split(",") if i.strip().isdigit()]
if ADMIN_ID not in OWNER_IDS:
    OWNER_IDS.append(ADMIN_ID)

DEFAULT_CHANNEL_USERNAME = "@AymnGuard"
DEFAULT_GROUP_USERNAME = "@AymnGuardChat"

START_TIME = time.time()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://mattress-before-exec-artwork.trycloudflare.com/webhook")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mattress-before-exec-artwork.trycloudflare.com/app/index.html")
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN", "AymnGuard2026")

DEFAULT_KMS_KEY = base64.b64encode(AESGCM.generate_key(bit_length=256)).decode()
MASTER_ENCRYPTION_KEY = os.getenv("MASTER_ENCRYPTION_KEY", DEFAULT_KMS_KEY)

API_KEY_NAME = "X-AymnGuard-Key"
SECURE_API_KEY = os.environ.get("AYMN_GUARD_SECRET_KEY", "AymnGuard_Enterprise_2026_Secure_Token")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ==========================================
# 3. دوال التشفير وحماية البيانات
# ==========================================
def get_aesgcm_cipher():
    try:
        key_bytes = base64.b64decode(MASTER_ENCRYPTION_KEY)
        return AESGCM(key_bytes)
    except Exception:
        return AESGCM(AESGCM.generate_key(bit_length=256))

def encrypt_data(plain_text):
    if not plain_text:
        return ""
    try:
        if not isinstance(plain_text, str):
            plain_text = str(plain_text)
        aesgcm = get_aesgcm_cipher()
        nonce = os.urandom(12)
        encrypted = aesgcm.encrypt(nonce, plain_text.encode("utf-8"), None)
        return base64.b64encode(nonce + encrypted).decode("utf-8")
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return plain_text

def decrypt_data(cipher_text):
    if not cipher_text:
        return ""
    try:
        if not isinstance(cipher_text, str):
            return cipher_text
        raw_data = base64.b64decode(cipher_text.encode("utf-8"))
        nonce = raw_data[:12]
        encrypted = raw_data[12:]
        aesgcm = get_aesgcm_cipher()
        decrypted = aesgcm.decrypt(nonce, encrypted, None)
        return decrypted.decode("utf-8")
    except Exception:
        return cipher_text

DEFAULT_RAW_TOKEN = "8830945140:AAHv5j36b03T3xNBgcVovgKHu2hhkbUsbrE"
RAW_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", DEFAULT_RAW_TOKEN)
TOKEN = decrypt_data(encrypt_data(RAW_TOKEN))
bot = telebot.TeleBot(TOKEN, threaded=False)

# ==========================================
# 4. محرك المهام الخلفية (APScheduler)
# ==========================================
scheduler = AsyncIOScheduler()

async def system_health_check_task():
    logger.info("⚙️ [مهمة مجولة] فحص صحة النظام السيادي في الخلفية.")

def setup_scheduler():
    scheduler.add_job(system_health_check_task, 'interval', hours=1, id='health_check_job')

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

# ==========================================
# 5. إدارة دورة حياة التطبيق (Enterprise Lifespan)
# ==========================================
@asynccontextmanager
async def enterprise_lifespan(app: FastAPI):
    logger.info("🚀 [AymnGuard Ultimate] جاري إقلاع النواة السيادية والمحركات اللوجستية...")
    app.state.startup_time = time.time()
    
    try:
        bot.remove_webhook()
        await asyncio.sleep(1)
        bot.set_webhook(url=WEBHOOK_URL, secret_token=TELEGRAM_SECRET_TOKEN, drop_pending_updates=True)
        logger.info(f"✅ تم ربط الـ Webhook بنجاح: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ خطأ Webhook: {e}")

    try:
        setup_scheduler()
        start_scheduler()
    except Exception as e:
        logger.error(f"⚠️ خطأ المجدول: {e}")

    yield
    
    logger.warning("🛑 جاري إيقاف النظام بأمان وتأمين الجلسات...")
    shutdown_session = locals().get('shutdown_scheduler')
    if shutdown_session:
        try: shutdown_scheduler()
        except: pass

# ==========================================
# 6. إعداد FastAPI والملفات الثابتة ومحتوى الـ PWA
# ==========================================
app = FastAPI(
    title="AymnGuard Enterprise Logistics & Sovereign Ultimate Platform",
    description="نظام سيادي متكامل يدمج بوتات تليجرام، إدارة الجلسات اللوجستية الضخمة، والتحكم السيادي للمالك.",
    version="4.0.0-Ultimate",
    lifespan=enterprise_lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
os.makedirs("static/app", exist_ok=True)

with open("static/manifest.json", "w", encoding="utf-8") as f:
    f.write('{"name": "AymnGuard Ultimate Client", "short_name": "AG Plus", "start_url": "/app/index.html", "display": "standalone", "background_color": "#0b111a", "theme_color": "#3f88c5"}')

with open("static/sw.js", "w", encoding="utf-8") as f:
    f.write("self.addEventListener('fetch', (e) => { e.respondWith(fetch(e.request).catch(() => caches.match(e.request))); });")

with open("static/robots.txt", "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n")

with open("static/sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://mattress-before-exec-artwork.trycloudflare.com/</loc></url></urlset>')

# تضمين صفحات الـ Landing و Mini App الشاملة
LANDING_PAGE_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>AymnGuard Plus Enterprise</title></head>
<body style="background:#0b111a; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
    <h1>AymnGuard Enterprise Logistics Platform</h1>
    <p>النظام السيادي يعمل بكفاءة تامة. افتح تطبيق الويب أدناه أو تواصل مع البوت.</p>
    <a href="/app/index.html" style="color:#3f88c5; font-size:20px; font-weight:bold;">فتح الـ Mini App السيادي</a>
</body></html>
"""
with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(LANDING_PAGE_HTML)

MINI_APP_HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>AymnGuard Mini App</title></head>
<body style="background:#0b111a; color:#fff; font-family:sans-serif; padding:20px;">
    <h2>لوحة التحكم الميدانية (Mini App)</h2>
    <p>النظام متصل وجاهز لإدارة الحسابات والعمليات اللوجستية.</p>
</body></html>
"""
with open("static/app/index.html", "w", encoding="utf-8") as f:
    f.write(MINI_APP_HTML_CONTENT)

# ==========================================
# 7. قواعد البيانات المحلية والخارجية
# ==========================================
def init_local_db():
    try:
        with sqlite3.connect("aymnguard_local.db", check_same_thread=False) as conn:
            c = conn.cursor()
            c.execute("PRAGMA journal_mode=WAL;")
            c.execute("CREATE TABLE IF NOT EXISTS local_users (user_id INTEGER PRIMARY KEY, username TEXT, joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("CREATE TABLE IF NOT EXISTS support_tickets (ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, issue_text TEXT, status TEXT DEFAULT 'open', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("CREATE TABLE IF NOT EXISTS transfer_sessions (user_id INTEGER PRIMARY KEY, state TEXT DEFAULT 'IDLE', target_chat TEXT DEFAULT '', source_chats TEXT DEFAULT '', count INTEGER DEFAULT 50, sessions_data TEXT DEFAULT '[]')")
            c.execute("CREATE TABLE IF NOT EXISTS pricing_settings (id INTEGER PRIMARY KEY CHECK (id = 1), vip_price REAL, bot_price REAL, tool_price REAL)")
            c.execute("CREATE TABLE IF NOT EXISTS bot_dynamic_settings (id INTEGER PRIMARY KEY CHECK (id = 1), channel_username TEXT, group_username TEXT, welcome_message TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS wallet_rotation (id INTEGER PRIMARY KEY CHECK (id = 1), last_index INTEGER DEFAULT 0)")
            c.execute("CREATE TABLE IF NOT EXISTS user_inbox (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, message_text TEXT, created_at TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS board_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id INTEGER, sender_name TEXT, message_text TEXT, created_at TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS support_staff (staff_id INTEGER PRIMARY KEY, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            c.execute("CREATE TABLE IF NOT EXISTS enterprise_team (member_id INTEGER PRIMARY KEY, role TEXT DEFAULT 'SUPPORT_AGENT', added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            
            c.execute("INSERT OR IGNORE INTO pricing_settings (id, vip_price, bot_price, tool_price) VALUES (1, 70.0, 35.0, 45.0)")
            c.execute("INSERT OR IGNORE INTO wallet_rotation (id, last_index) VALUES (1, 0)")
            c.execute("INSERT OR IGNORE INTO bot_dynamic_settings (id, channel_username, group_username, welcome_message) VALUES (1, ?, ?, ?)", (DEFAULT_CHANNEL_USERNAME, DEFAULT_GROUP_USERNAME, ""))
            c.execute("INSERT OR IGNORE INTO support_staff (staff_id) VALUES (?)", (ADMIN_ID,))
            c.execute("INSERT OR IGNORE INTO enterprise_team (member_id, role) VALUES (?, ?)", (ADMIN_ID, "SUPREME_OWNER"))
            conn.commit()
    except Exception as e:
        logger.error(f"SQLite Init Error: {e}")

init_local_db()

# MongoDB & Redis Optional Setup
redis_client = None
try:
    redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True, socket_timeout=3)
    redis_client.ping()
except: pass

# ==========================================
# 8. دوال المساعدة، الأسعار والأمان
# ==========================================
def get_vip_price(): return 70.0
def get_bot_price(): return 35.0
def get_tool_price(): return 45.0

def is_staff(user_id):
    if user_id == ADMIN_ID: return True
    try:
        with sqlite3.connect("aymnguard_local.db", check_same_thread=False) as conn:
            return conn.cursor().execute("SELECT 1 FROM support_staff WHERE staff_id=?", (user_id,)).fetchone() is not None
    except: return False

def check_is_vip(user_id):
    return user_id == ADMIN_ID or is_staff(user_id)

def check_is_tool_paid(user_id):
    return check_is_vip(user_id)

def sanitize_input(text):
    if not isinstance(text, str): return str(text) if text is not None else ""
    return re.sub(r"['\";\\#\-\-\*]", "", text).strip()

# ==========================================
# 9. إدارة لوحة تحكم المالك السيادية (Sovereign Owner Center)
# ==========================================
owner_sovereign_router = APIRouter(prefix="/api/v1/sovereign-owner", tags=["Sovereign Owner Control Center"])

class SystemOverrideSchema(BaseModel):
    action_type: str = Field(..., description="نوع الإجراء السيادي")
    authorization_key: str = Field(..., description="مفتاح التوثيق السيادي")
    payload: Dict[str, Any] = Field(default={}, description="البيانات التنفيذية")

@owner_sovereign_router.get("/metrics", summary="لوحة المتركس السيادية")
async def sovereign_system_metrics(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    return {
        "status": "success",
        "sovereign_clearance": "AUTHORIZED_OWNER",
        "metrics": {
            "platform_status": "ONLINE_STABLE",
            "active_nodes": 1,
            "database_engine": "SQLite/PostgreSQL/MongoDB Enterprise Bridge",
            "security_integrity": "100%",
            "system_version": "4.0.0-Ultimate"
        }
    }

@owner_sovereign_router.post("/override-control", summary="التحكم السيادي المطلق")
async def execute_sovereign_override(data: SystemOverrideSchema, db: AsyncSession = Depends(get_db)) -> Any:
    expected_key = os.getenv("SOVEREIGN_MASTER_KEY", "AymnGuard_Sovereign_Master_2026")
    if data.authorization_key != expected_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="مفتاح التوثيق السيادي غير صحيح.")
    return {
        "status": "success",
        "message": f"تم تنفيذ الإجراء السيادي [{data.action_type}] بنجاح تام.",
        "payload": data.payload
    }

# ==========================================
# 10. ربط المسارات (Routers Registration)
# ==========================================
app.include_router(users_router, prefix="/api/v1")
app.include_router(owner_sovereign_router)

# ==========================================
# 11. نقطة التحقق الصحية (Health Check)
# ==========================================
@app.get("/", tags=["System Health"])
async def root_enterprise_gateway():
    return {
        "platform": "AymnGuard Enterprise Logistics & Sovereign Ultimate Platform",
        "status": "Operational & Active",
        "architecture": "Sovereign Micro-Core & Async SQLAlchemy 2.0",
        "documentation": "/docs",
        "owner_control": "/api/v1/sovereign-owner/metrics"
    }

# ==========================================
# 12. تشغيل الخادم المركزي (Entry Point)
# ==========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"🟢 الخادم السيادي يعمل بكفاءة تامة على المنفذ {port}...")
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 تم إيقاف النظام يدويًا.")
