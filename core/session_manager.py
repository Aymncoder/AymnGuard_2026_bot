# -*- coding: utf-8 -*-
"""
==============================================================================
AymnGuard Sovereign Session Manager (v18.0.0-Master Enterprise Integrated)
==============================================================================
مدير الجلسات السيادي المتكامل: إدارة الأسطول، الفحص الحي للاتصال،
توزيع الأحمال الديناميكي (Load Balancing)، المراقبة الذاتية (Self-Healing)، 
والتحليلات المؤسسية اللحظية.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from pyrogram import Client
from pyrogram.errors import UserDeactivated, SessionRevoked

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
    is_dead: bool = False  # مؤشر الموت السريري (الحظر النهائي)
    hourly_reset_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class SovereignSessionManager:
    """
    المدير السيادي للجلسات (Enterprise Session Orchestrator).
    يجمع بين السرعة اللحظية، توزيع الأحمال، والصرامة الأمنية لقاعدة البيانات.
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
            exported_string = await client.export_session_string()
            await client.disconnect()
        except Exception as e:
            logger.error(f"❌ [Session Error]: Verification failed for {session_name}: {e}")
            return {"status": "error", "message": str(e)}

        # 2. التسجيل في السجل المركزي (In-Memory) مع الاحتفاظ بطاقة الجلسة
        cls._active_sessions[session_id] = {
            "session_name": session_name,
            "client_type": client_type.lower(),
            "status": "ACTIVE_AND_SECURED",
            "session_string": exported_string,
            "metrics": SessionMetrics(),
            "created_at": datetime.now(timezone.utc)
        }

        # تفعيل المراقب الذاتي (مفاعل الطاقة) إذا لم يكن يعمل
        if not cls._ai_monitor_running:
            asyncio.create_task(cls._autonomous_health_monitor())
            cls._ai_monitor_running = True

        return {"status": "success", "message": f"تم تهيئة وعزل الجلسة {session_name} بنجاح."}

    # -------------------------------------------------------------------------
    # موزع الأحمال الذكي (Enterprise Load Balancer) - [إضافة نوعية]
    # -------------------------------------------------------------------------
    @classmethod
    async def get_optimal_session(cls, license_key: str) -> Optional[Dict[str, Any]]:
        """
        خوارزمية الذكاء الاصطناعي لاختيار أفضل جلسة:
        يستبعد الجلسات المحظورة، ويختار الجلسة الأعلى صحة والأقل ضغطاً في الساعة الحالية.
        """
        candidates = []
        for s_id, data in cls._active_sessions.items():
            if s_id.startswith(license_key) and data["status"] == "ACTIVE_AND_SECURED" and not data["metrics"].is_dead:
                candidates.append(data)
                
        if not candidates:
            logger.warning(f"⚠️ [Load Balancer]: لا توجد جلسات نشطة أو صحية للمفتاح {license_key}! النظام في خطر.")
            return None
            
        # الفرز المزدوج: الأولوية للصحة العالية، ثم الأقل استخداماً في الساعة الأخيرة
        candidates.sort(key=lambda x: (x["metrics"].health_score, -x["metrics"].transfers_this_hour), reverse=True)
        
        best_session = candidates[0]
        logger.debug(f"⚖️ [Load Balancer]: تم اختيار الجلسة {best_session['session_name']} (الصحة: {best_session['metrics'].health_score})")
        return best_session

    # -------------------------------------------------------------------------
    # إدارة العمليات (Operations Recording & Analytics)
    # -------------------------------------------------------------------------
    @classmethod
    async def record_transfer_action(cls, session_name: str, license_key: str, success: bool, is_rate_limit: bool = False):
        """تسجيل العمليات وتحديث الصحة الأمنية للحساب."""
        session_id = f"{license_key}_{session_name}"
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
            # مكافأة النجاح: زيادة الصحة تدريجياً
            metrics.health_score = min(100.0, metrics.health_score + 0.5)
        else:
            metrics.failed_transfers += 1
            # عقاب قاسي عند الحظر لتجنب حرق الرقم
            metrics.health_score -= 20.0 if is_rate_limit else 5.0
            if is_rate_limit:
                metrics.rate_limit_hits += 1

        # العزل التلقائي لحماية الرقم من الحظر النهائي
        if metrics.health_score <= 40.0:
            cls._active_sessions[session_id]["status"] = "QUARANTINED"
            logger.critical(f"🚨 [Security Alert]: تم عزل الجلسة {session_name} لحمايتها من الحظر النهائي (الصحة: {metrics.health_score}).")

    # -------------------------------------------------------------------------
    # تقارير الأداء (Enterprise Analytics)
    # -------------------------------------------------------------------------
    @classmethod
    async def get_enterprise_analytics_report(cls, license_key: str) -> Dict[str, Any]:
        """توليد تقرير استخباراتي يدمج بين الذاكرة وقاعدة البيانات."""
        total_active, total_quarantined, total_dead = 0, 0, 0
        session_details = []

        try:
            from backend_core.main import async_session, EnterpriseSessionModel
            from sqlalchemy.future import select
            
            async with async_session() as db:
                result = await db.execute(select(EnterpriseSessionModel))
                db_sessions = result.scalars().all()
                
            for s in db_sessions:
                s_id = f"{license_key}_{s.session_name}"
                data = cls._active_sessions.get(s_id, {"status": s.status, "metrics": SessionMetrics()})
                
                status = data["status"]
                metrics: SessionMetrics = data["metrics"]
                
                if metrics.is_dead:
                    total_dead += 1
                    status = "DEAD"
                elif status == "ACTIVE_AND_SECURED": 
                    total_active += 1
                elif status == "QUARANTINED": 
                    total_quarantined += 1

                session_details.append({
                    "name": s.session_name,
                    "status": status,
                    "health_score": round(metrics.health_score, 2),
                    "total_success": metrics.successful_transfers,
                    "rate_limits": metrics.rate_limit_hits
                })
        except Exception as e:
            logger.error(f"⚠️ Analytics Merge Error: {e}")

        return {
            "status": "success",
            "analytics": {
                "active": total_active,
                "quarantined": total_quarantined,
                "dead_sessions": total_dead,
                "details": sorted(session_details, key=lambda x: x["health_score"], reverse=True)
            }
        }

    # -------------------------------------------------------------------------
    # المراقبة الذاتية (Autonomous Health Monitor) - [النقلة النوعية]
    # -------------------------------------------------------------------------
    @classmethod
    async def _autonomous_health_monitor(cls):
        """وكيل ذكاء اصطناعي يعمل 24/7 للمراقبة والإصلاح الذاتي العميق."""
        logger.info("🛡️ [Auto-Healer]: تم تفعيل درع المراقبة والإنعاش الذاتي للجلسات.")
        while True:
            await asyncio.sleep(300) # فحص كل 5 دقائق
            now = datetime.now(timezone.utc)
            
            for s_id, data in cls._active_sessions.items():
                metrics: SessionMetrics = data["metrics"]
                status = data["status"]
                session_name = data["session_name"]
                
                if metrics.is_dead:
                    continue # لا نضيع الموارد على الجلسات الميتة تماماً
                
                # 1. التعافي الذاتي (Rehabilitation) للجلسات المعزولة
                if status == "QUARANTINED" and metrics.last_action_time:
                    # إذا مرت ساعتان على العزل دون نشاط، نعتبر أن الحظر قد زال
                    if (now - metrics.last_action_time) > timedelta(hours=2):
                        metrics.health_score = 80.0
                        metrics.rate_limit_hits = 0
                        data["status"] = "ACTIVE_AND_SECURED"
                        logger.info(f"✨ [Self-Healing]: تم إنعاش الجلسة {session_name} بنجاح وإعادتها للخدمة.")
                        
                # 2. تبريد تدريجي للصحة (Healing) للجلسات النشطة المجهدة
                if status == "ACTIVE_AND_SECURED" and metrics.health_score < 100.0:
                     metrics.health_score = min(100.0, metrics.health_score + 2.0)
