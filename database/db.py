cat << 'EOF' > database/db.py
import sqlite3
import redis
import psycopg2
from psycopg2 import pool
from pymongo import MongoClient
from urllib.parse import quote_plus
from config import settings
import logging

logger = logging.getLogger("AymnGuardEnterprise")

pg_pool = None
try:
    if "sslmode" not in settings.DATABASE_URL:
        separator = "&" if "?" in settings.DATABASE_URL else "?"
        secure_url = f"{settings.DATABASE_URL}{separator}sslmode=require"
    else:
        secure_url = settings.DATABASE_URL
    pg_pool = psycopg2.pool.SimpleConnectionPool(1, 100, secure_url)
    logger.info("✅ تم إنشاء تجمع اتصالات PostgreSQL بنجاح.")
except Exception as e:
    logger.warning(f"⚠️ فشل تجمع PostgreSQL: {e}")

def get_pg_connection():
    try:
        if pg_pool: return pg_pool.getconn()
        return psycopg2.connect(settings.DATABASE_URL)
    except: return None

redis_client = None
try:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=5)
    redis_client.ping()
    logger.info("✅ تم الاتصال بـ Redis بنجاح.")
except Exception as e:
    logger.warning(f"⚠️ تنبيه Redis: {e}")

mongo_client = None
mongo_db = None
users_col = None
wallets_col = None

try:
    password = quote_plus(settings.MONGO_PASSWORD)
    mongo_uri = f"mongodb+srv://{settings.MONGO_USER}:{password}@cluster0.joccmoz.mongodb.net/AymnGuardDB?retryWrites=true&w=majority&appName=Cluster0"
    mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command("ping")
    mongo_db = mongo_client["AymnGuardDB"]
    wallets_col = mongo_db["wallets"]
    users_col = mongo_db["paid_users"]
    users_col.create_index("user_id", unique=True)
    logger.info("✅ تم الاتصال بقاعدة بيانات MongoDB السحابية بنجاح!")
except Exception as e:
    logger.error(f"❌ خطأ MongoDB: {e}")
EOF

