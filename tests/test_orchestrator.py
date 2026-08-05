
#-*- coding: utf-8 -*-
"""
AymnGuard Enterprise v5.0 : Sovereign Unit & Integration Tests
اختبارات وحدة النظام والتحقق من صحة الاتصال بقاعدة البيانات ومحركات التشغيل.
"""

import pytest
import asyncio
from database.db import check_database_health, init_db

@pytest.mark.asyncio
async def test_database_initialization():
    """اختبار تهيئة وإنشاء جداول قاعدة البيانات بنجاح تام."""
    await init_db()
    assert True

@pytest.mark.asyncio
async def test_database_health_check():
    """اختبار فحص نبض وسلامة الاتصال بقاعدة البيانات (Health Check Probe)."""
    health_status = await check_database_health()
    assert health_status["status"] == "healthy"
    assert "latency_ms" in health_status
