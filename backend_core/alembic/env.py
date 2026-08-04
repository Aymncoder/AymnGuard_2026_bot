# -*- coding: utf-8 -*-
"""
==============================================================================
AymnCoder Plus : Aegis AI Core - Enterprise Alembic Migration Environment
==============================================================================
بيئة ترحيل قواعد البيانات (Alembic Async Migrations) المهندسة بمعايير المؤسسات الكبرى،
مع المسارات الديناميكية القابلة للنقل والدعم التلقائي لاكتشاف جداول النماذج.
"""

import os
import sys
import asyncio
import logging
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from dotenv import load_dotenv

# ==============================================================================
# 1. التكوين الديناميكي للمسارات (Cross-Platform Path Resolution)
# ==============================================================================
# تحديد جذر المشروع تلقائياً بغض النظر عن النظام (Termux, VPS, Docker, Windows, Linux)
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent  # الوصول لجذر backend_core
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات المؤسسية الخاصة بـ Alembic
logger = logging.getLogger("AegisAICore.AlembicMigration")

# ==============================================================================
# 2. استيراد النماذج وقاعدة البيانات للتتبع التلقائي (Metadata Discovery)
# ==============================================================================
try:
    from app.db.database import Base
    # استيراد كافة نماذج الجداول لضمان رصد Alembic لأي تعديل جديد تلقائياً
    from app.models import user, transaction, coupon
except ImportError as e:
    logger.warning(f"⚠️ [Alembic Warning]: تعذر استيراد بعض النماذج تلقائياً: {str(e)}")

# إعدادات Alembic الأساسية
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ==============================================================================
# 3. إعداد رابط قاعدة البيانات وتوافقيته مع asyncpg
# ==============================================================================
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("❌ [Critical Error]: متغير البيئة DATABASE_URL غير مُعرّف.")

# التحويل التلقائي للرابط ليدعم محرك asyncpg غير المتزامن
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

# ==============================================================================
# 4. محرك الترحيلات غير المتصلة (Offline Mode)
# ==============================================================================
def run_migrations_offline() -> None:
    """تشغيل الترحيلات في الوضع غير المتصل (توليد ملفات SQL مباشرة)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """تنفيذ الترحيلات عبر الاتصال النشط."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ==============================================================================
# 5. محرك الترحيلات غير المتزامن (Online Async Engine)
# ==============================================================================
async def run_async_migrations() -> None:
    """إنشاء المحرك غير المتزامن وتنفيذ عمليات الترحيل بأعلى كفاءة مؤسسية."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """تشغيل الترحيلات في الوضع المتصل على قاعدة البيانات الحية."""
    try:
        asyncio.run(run_async_migrations())
        logger.info("✅ [Alembic Engine]: تم تنفيذ وتطبيق ترحيلات قاعدة البيانات بنجاح تام.")
    except Exception as e:
        logger.error(f"❌ [Alembic Critical Error]: فشل تنفيذ الترحيلات: {str(e)}")
        raise e


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
