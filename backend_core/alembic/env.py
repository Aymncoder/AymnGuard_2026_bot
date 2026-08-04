import os
import sys
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.insert(0, '/data/data/com.termux/files/home/AymnGuard_Platform/backend')
load_dotenv()

from app.db.database import Base
from app.models.user import User

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("CRITICAL ERROR: DATABASE_URL is not set in the environment.")

# تحويل الرابط تلقائياً ليدعم المحرك غير المتزامن الأسرع (asyncpg)
if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://")

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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

def do_run_migrations(connection):
    """Sync target for the async engine."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine and associate a connection with the context."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
