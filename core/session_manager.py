# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Session Manager (v18.0.0-Master Enterprise Integrated)
==============================================================================
مدير الجلسات السيادي المتكامل: إدارة الأسطول، الفحص الحي للاتصال،
المراقبة الذاتية (Self-Healing)، والتحليلات المؤسسية اللحظية.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from pyrogram import Client

# إعداد السجلات الأمنية والتحليلية
logger = logging.getLogger("SovereignSessionManager")

@dataclass
class SessionMetrics:
    """وحدة تخزين البيانات التحليلية اللحظية لكل جلسة."""
    total_transfers: int = 0
    successful_transfers: int = 0
    failed_transfers: int = 0
    last_action_time: Optional[datetime] = None
    rate_limit_hits: int = 0
    health_score: float = 100.0
    transfers_this_hour: int = 0
    hourly_reset_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class SovereignSessionManager:
    """
    المدير السيادي للجلسات (Enterprise Session Orchestrator).
    يجمع بين السرعة اللحظية لإدارة الذاكرة والصرامة الأمنية لقاعدة البيانات.
    """
    
    # السجل المركزي المعزول للجلسات النشطة
    _active_sessions: Dict[str, Dict[str, Any]] = {}
    _ai_monitor_running: bool = False

    # -------------------------------------------------------------------------
    # تهيئة الجلسات (Initialization & Verification)
    # -------------------------------------------------------------------------
    @classmethod
    async def initialize_session(
        cls,
        license_key: str,
        session_name: str,
        api_id: int,
        api_hash: str,
        phone_number: str,
        session_string: Optional[str] = None,
        client_type: str = "pyrogram"
    ) -> Dict[str, Any]:
        """تهيئة جلسة جديدة واختبار صلاحيتها حقيقياً قبل تسجيلها في الخزنة."""
        session_id = f"{license_key}_{session_name}"
        
        # 1. اختبار الاتصال الحقيقي عبر Pyrogram
        client = Client(name=session_name, api_id=api_id, api_hash=api_hash, session_string=session_string, in_memory=True)
        try:
            await client.connect()
            me = await client.get_me()
            logger.info(f"✅ [Session Verified]: Connected as {me.first_name} (ID: {me.id})")
            await client.disconnect()
        except Exception as e:
            logger.error(f"❌ [Session Error]: Verification failed: {e}")
            return {"status": "error", "message": str(e)}

        # 2. التسجيل في السجل المركزي (In-Memory)
        cls._active_sessions[session_id] = {
            "session_name": session_name,
            "client_type": client_type.lower(),
            "status": "ACTIVE_AND_SECURED",
            "metrics": SessionMetrics(),
            "created_at": datetime.now(timezone.utc)
        }

        # تفعيل المراقب الذاتي إذا لم يعمل
        if not cls._ai_monitor_running:
            asyncio.create_task(cls._autonomous_health_monitor())
            cls._ai_monitor_running = True

        return {"status": "success", "message": f"تم تهيئة وعزل الجلسة {session_name} بنجاح."}

    # -------------------------------------------------------------------------
    # إدارة العمليات (Operations Recording & Analytics)
    # -------------------------------------------------------------------------
    @classmethod
    async def record_transfer_action(cls, session_id: str, success: bool, is_rate_limit: bool = False):
        """تسجيل العمليات وتحديث الصحة الأمنية للحساب."""
        if session_id not in cls._active_sessions:
            return

        metrics: SessionMetrics = cls._active_sessions[session_id]["metrics"]
        now = datetime.now(timezone.utc)

        if (now - metrics.hourly_reset_time) > timedelta(hours=1):
            metrics.transfers_this_hour = 0
            metrics.hourly_reset_time = now

        metrics.total_transfers += 1
        metrics.last_action_time = now

        if success:
            metrics.successful_transfers += 1
            metrics.transfers_this_hour += 1
            metrics.health_score = min(100.0, metrics.health_score + 0.1)
        else:
            metrics.failed_transfers += 1
            metrics.health_score -= 15.0 if is_rate_limit else 2.0

        if metrics.health_score <= 40.0:
            cls._active_sessions[session_id]["status"] = "QUARANTINED"
            logger.warning(f"[Security Alert] Session {session_id} quarantined.")

    # -------------------------------------------------------------------------
    # تقارير الأداء (Enterprise Analytics)
    # -------------------------------------------------------------------------
    @classmethod
    async def get_enterprise_analytics_report(cls, license_key: str) -> Dict[str, Any]:
        """توليد تقرير استخباراتي يدمج بين الذاكرة وقاعدة البيانات."""
        total_active, total_quarantined = 0, 0
        session_details = []

        try:
            # دمج بيانات الذاكرة مع سجلات قاعدة البيانات (إن وجدت)
            from backend_core.main import async_session, EnterpriseSessionModel
            from sqlalchemy.future import select
            
            async with async_session() as db:
                result = await db.execute(select(EnterpriseSessionModel))
                db_sessions = result.scalars().all()
                
            for s in db_sessions:
                s_id = f"{license_key}_{s.session_name}"
                data = cls._active_sessions.get(s_id, {"status": s.status, "metrics": SessionMetrics()})
                
                status = data["status"]
                metrics = data["metrics"]
                
                if status == "ACTIVE_AND_SECURED": total_active += 1
                elif status == "QUARANTINED": total_quarantined += 1

                session_details.append({
                    "name": s.session_name,
                    "status": status,
                    "health_score": round(metrics.health_score, 2),
                    "total_success": metrics.successful_transfers
                })
        except Exception as e:
            logger.error(f"Analytics Merge Error: {e}")

        return {
            "status": "success",
            "analytics": {
                "active": total_active,
                "quarantined": total_quarantined,
                "details": sorted(session_details, key=lambda x: x["health_score"], reverse=True)
            }
        }

    # -------------------------------------------------------------------------
    # المراقبة الذاتية (Autonomous Health Monitor)
    # -------------------------------------------------------------------------
    @classmethod
    async def _autonomous_health_monitor(cls):
        """وكيل ذكاء اصطناعي يعمل 24/7 للمراقبة والإصلاح الذاتي."""
        while True:
            await asyncio.sleep(300) # فحص كل 5 دقائق
            now = datetime.now(timezone.utc)
            
            for s_id, data in cls._active_sessions.items():
                metrics: SessionMetrics = data["metrics"]
                status = data["status"]
                
                # التعافي الذاتي (Rehabilitation)
                if status == "QUARANTINED" and metrics.last_action_time:
                    if (now - metrics.last_action_time) > timedelta(hours=2):
                        metrics.health_score = 75.0
                        data["status"] = "ACTIVE_AND_SECURED"
                        logger.info(f"[Self-Healing] Session {data['session_name']} rehabilitated.")
                        
                # تبريد تدريجي للصحة
                if status == "ACTIVE_AND_SECURED" and metrics.health_score < 100.0:
                     metrics.health_score = min(100.0, metrics.health_score + 1.5)
