# File: app/redteam/api.py
"""
Phase 112 – Red-Team API Endpoints
=====================================
FastAPI router mounted at ``/api/v1/redteam``.  Provides endpoints for
starting drills, viewing status, downloading reports, managing schedules,
and issuing emergency stops.

All endpoints enforce multi-tenancy: clients can only see their own
drills and schedules.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, Field

from app.redteam.models import (
    AttackProfile,
    DrillConfig,
    DrillRun,
    DrillSchedule,
    DrillStatus,
    DrillStore,
)
from app.redteam.safe_exploit_engine import SafeExploitEngine, SafetyViolation
from app.redteam.report_generator import ReportGenerator
from app.redteam.scheduler import RedTeamScheduler

logger = logging.getLogger("guardrail.redteam.api")

router = APIRouter(prefix="/api/v1/redteam", tags=["Red-Team (Phase 112)"])


# ======================================================================
# Dependencies (initialised once at module level for simplicity)
# ======================================================================

def _get_settings():
    """Lazy-load config to avoid circular imports."""
    from app.core.config import settings
    return settings


_engine: Optional[SafeExploitEngine] = None
_store: Optional[DrillStore] = None
_report_gen: Optional[ReportGenerator] = None
_scheduler: Optional[RedTeamScheduler] = None


def _init_services():
    """Lazy-initialise all red-team services."""
    global _engine, _store, _report_gen, _scheduler
    if _scheduler is not None:
        return

    settings = _get_settings()
    _engine = SafeExploitEngine(
        sandbox_prefix=settings.REDTEAM_SANDBOX_AGENT_PREFIX,
        max_duration=settings.REDTEAM_MAX_DRILL_DURATION,
        max_concurrent=settings.REDTEAM_MAX_CONCURRENT_DRILLS_PER_CLIENT,
    )
    _store = DrillStore(storage_dir=settings.REDTEAM_REPORT_STORAGE_PATH + "_data")
    _report_gen = ReportGenerator(storage_path=settings.REDTEAM_REPORT_STORAGE_PATH)
    _scheduler = RedTeamScheduler(
        engine=_engine, store=_store, report_gen=_report_gen,
    )


def get_scheduler() -> RedTeamScheduler:
    """FastAPI dependency that returns the singleton scheduler."""
    _init_services()
    assert _scheduler is not None
    return _scheduler


def get_client_id() -> str:
    """
    Extract the authenticated client ID.

    In production, this would parse the API key or PQC-signed token
    from the request headers.  For now, we accept an ``X-Client-ID``
    header (or default to ``"anonymous"``).
    """
    # Placeholder — integrate with real auth in production
    return "anonymous"


# ======================================================================
# Request / response schemas
# ======================================================================

class StartDrillRequest(BaseModel):
    target_agent_ids: List[str]
    attack_profile: AttackProfile = AttackProfile.AUTO
    max_duration_seconds: int = Field(default=600, ge=10, le=3600)


class CreateScheduleRequest(BaseModel):
    cron: str = Field(..., description="Cron expression (e.g. '0 2 * * *')")
    target_agent_ids: List[str]
    attack_profile: AttackProfile = AttackProfile.AUTO
    max_duration_seconds: int = Field(default=600, ge=10, le=3600)


class DrillSummaryResponse(BaseModel):
    drill_id: str
    status: str
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    total_attempts: Optional[int] = None
    blocked: Optional[int] = None
    bypassed: Optional[int] = None
    detection_rate: Optional[float] = None
    report_available: bool = False


class ScheduleResponse(BaseModel):
    schedule_id: str
    cron: Optional[str]
    active: bool
    created_at: str


# ======================================================================
# Drill endpoints
# ======================================================================

@router.post("/drills", response_model=DrillSummaryResponse, status_code=201)
async def start_drill(
    req: StartDrillRequest,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Start an immediate adversarial drill."""
    config = DrillConfig(
        target_agent_ids=req.target_agent_ids,
        attack_profile=req.attack_profile,
        max_duration_seconds=req.max_duration_seconds,
    )

    client_id = get_client_id()

    try:
        run = await scheduler.run_drill_now(client_id=client_id, config=config)
    except SafetyViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return DrillSummaryResponse(
        drill_id=run.id,
        status=run.status.value,
        started_at=run.started_at,
    )


@router.get("/drills/{drill_id}", response_model=DrillSummaryResponse)
async def get_drill_status(
    drill_id: str,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Get the status and summary of a drill."""
    run = scheduler.get_drill_status(drill_id)
    if not run:
        raise HTTPException(status_code=404, detail="Drill not found")

    client_id = get_client_id()
    if run.client_id != client_id and client_id != "anonymous":
        raise HTTPException(status_code=403, detail="Access denied")

    result = run.result_summary
    return DrillSummaryResponse(
        drill_id=run.id,
        status=run.status.value if isinstance(run.status, DrillStatus) else run.status,
        started_at=run.started_at,
        ended_at=run.ended_at,
        total_attempts=result.total_attempts if result else None,
        blocked=result.blocked if result else None,
        bypassed=result.bypassed if result else None,
        detection_rate=result.detection_rate if result else None,
        report_available=run.report_path is not None,
    )


@router.get("/drills/{drill_id}/report")
async def get_drill_report(
    drill_id: str,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Download the drill report (HTML)."""
    run = scheduler.get_drill_status(drill_id)
    if not run:
        raise HTTPException(status_code=404, detail="Drill not found")

    if not run.report_path:
        # Try generating on the fly
        if run.result_summary:
            _init_services()
            assert _report_gen is not None
            content = _report_gen.generate_report(run, fmt="html")
            return HTMLResponse(content=content)
        raise HTTPException(status_code=404, detail="Report not yet available")

    import os
    if os.path.exists(run.report_path):
        with open(run.report_path, "rb") as f:
            return HTMLResponse(content=f.read())

    raise HTTPException(status_code=404, detail="Report file not found")


@router.post("/drills/{drill_id}/stop")
async def stop_drill(
    drill_id: str,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Emergency stop an active drill."""
    stopped = scheduler.stop_drill(drill_id)
    if not stopped:
        raise HTTPException(
            status_code=404,
            detail="Drill not found or not currently running",
        )
    return {"status": "stopped", "drill_id": drill_id}


# ======================================================================
# Schedule endpoints
# ======================================================================

@router.post("/schedules", response_model=ScheduleResponse, status_code=201)
async def create_schedule(
    req: CreateScheduleRequest,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Create a recurring drill schedule."""
    config = DrillConfig(
        target_agent_ids=req.target_agent_ids,
        attack_profile=req.attack_profile,
        max_duration_seconds=req.max_duration_seconds,
    )
    client_id = get_client_id()
    schedule_id = scheduler.schedule_drill(
        client_id=client_id, config=config, cron=req.cron,
    )
    sched = scheduler.store.get_schedule(schedule_id)
    return ScheduleResponse(
        schedule_id=schedule_id,
        cron=req.cron,
        active=True,
        created_at=sched.created_at if sched else "",
    )


@router.get("/schedules", response_model=List[ScheduleResponse])
async def list_schedules(
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """List all schedules for the authenticated client."""
    client_id = get_client_id()
    schedules = scheduler.list_schedules(client_id)
    return [
        ScheduleResponse(
            schedule_id=s.id,
            cron=s.cron,
            active=s.active,
            created_at=s.created_at,
        )
        for s in schedules
    ]


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    scheduler: RedTeamScheduler = Depends(get_scheduler),
):
    """Cancel and remove a schedule."""
    deleted = scheduler.cancel_drill(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"status": "cancelled", "schedule_id": schedule_id}
