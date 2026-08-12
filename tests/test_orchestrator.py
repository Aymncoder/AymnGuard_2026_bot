# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Enterprise v5.0 : Advanced Sovereign Unit & Integration Test Suite
==============================================================================
النسخة الماسية المتقدمة: اختبارات وحدة النظام الشاملة.
تم عزل بيئة الاختبار تماماً (Sandbox) لمنع المساس بقاعدة البيانات السحابية 
الإنتاجية أثناء عمليات الفحص الآلي (CI/CD).
==============================================================================
"""

import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

# --- حماية سيادية صارمة (Zero-Trust) ---
# إجبار النظام بالكامل على استخدام قاعدة بيانات وهمية في الذاكرة أثناء الاختبار
# لمنع الدوال المستوردة من الاتصال بالسيرفر السحابي الحقيقي (135.181.86.199)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

# استيراد النماذج ووظائف المحرك السيادي (بعد تأمين متغيرات البيئة)
from database.models import Base, SovereignUser, SovereignAuditLog
from database.db import check_database_health, init_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """إنشاء محرك قاعدة بيانات افتراضي مؤقت خاص باختبارات الوحدة لضمان العزل التام."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """إمداد جلسات اختبار غير متزامنة معزولة وآمنة لكل اختبار على حدة مع التراجع التلقائي."""
    async_session_maker = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )
    async with async_session_maker() as session:
        yield session
        await session.rollback()

@pytest.mark.asyncio
async def test_sovereign_database_initialization():
    """اختبار تهيئة وإنشاء جداول قاعدة البيانات السيادية بكفاءة مطلقة."""
    try:
        await init_db()
        assert True
    except Exception as e:
        pytest.fail(f"فشل تهيئة قاعدة البيانات أثناء الاختبار: {e}")

@pytest.mark.asyncio
async def test_sovereign_health_probe():
    """اختبار نبض وسلامة الاتصال (Health Check Probe) مع التحقق من المقاييس."""
    try:
        health = await check_database_health()
        assert "status" in health
        assert "latency_ms" in health
        assert isinstance(health["latency_ms"], (int, float))
    except Exception as e:
        pytest.fail(f"فشل فحص نبض قاعدة البيانات: {e}")

@pytest.mark.asyncio
async def test_sovereign_user_creation_model(db_session: AsyncSession):
    """اختبار إدراج والتحقق من نموذج مستخدمي النظام السيادي (SovereignUser)."""
    new_user = SovereignUser(
        telegram_id=987654321,
        username="AymnEnterpriseTester",
        is_active=True
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    assert new_user.id is not None
    assert new_user.telegram_id == 987654321
    assert new_user.username == "AymnEnterpriseTester"
    assert new_user.is_active is True

@pytest.mark.asyncio
async def test_sovereign_audit_log_model(db_session: AsyncSession):
    """اختبار إنشاء والتحقق من سجلات التدقيق الأمني السيادي (SovereignAuditLog)."""
    audit_log = SovereignAuditLog(
        telegram_id=987654321,
        action="ENTERPRISE_SECURITY_SCAN",
        details="AST, Meta-Engine, and Dependency verification tests passed successfully."
    )
    db_session.add(audit_log)
    await db_session.commit()
    await db_session.refresh(audit_log)

    assert audit_log.id is not None
    assert audit_log.action == "ENTERPRISE_SECURITY_SCAN"
    assert audit_log.timestamp is not None
