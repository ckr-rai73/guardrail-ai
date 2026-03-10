# File: app/redteam/models.py
"""
Phase 112 – Red-Team Data Models
==================================
Pydantic models for drill configuration, results, and persistence.
For production, these would map to SQLAlchemy ORM tables; here we
use Pydantic models with JSON-file persistence for simplicity.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger("guardrail.redteam.models")


# ======================================================================
# Enums
# ======================================================================

class DrillStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"
    FAILED = "failed"


class AttackProfile(str, Enum):
    AUTO = "auto"
    PROMPT_INJECTION = "prompt_injection"
    DATA_POISONING = "data_poisoning"
    MODEL_EVASION = "model_evasion"
    SUPPLY_CHAIN = "supply_chain"
    PRIVILEGE_ESCALATION = "privilege_escalation"


# ======================================================================
# Config & Result (value objects)
# ======================================================================

class DrillConfig(BaseModel):
    """Configuration for a single drill run."""
    target_agent_ids: List[str] = Field(
        ..., description="Agent IDs that may be targeted",
    )
    attack_profile: AttackProfile = AttackProfile.AUTO
    max_duration_seconds: int = Field(
        default=600, ge=10, le=3600,
        description="Maximum drill duration in seconds",
    )
    max_rps: int = Field(
        default=50, ge=1, le=500,
        description="Maximum requests per second during the drill",
    )
    max_agents: int = Field(
        default=10, ge=1, le=100,
        description="Maximum simultaneous agents to target",
    )


class VulnerabilityFinding(BaseModel):
    """A single vulnerability discovered during a drill."""
    attack_type: str
    description: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    policy_id: Optional[str] = None
    remediation: str = ""
    compliance_impact: str = ""


class DrillResult(BaseModel):
    """Aggregate results from a completed drill."""
    total_attempts: int = 0
    blocked: int = 0
    bypassed: int = 0
    errors: int = 0
    detection_rate: float = 0.0
    mean_response_ms: float = 0.0
    p99_response_ms: float = 0.0
    vulnerabilities: List[VulnerabilityFinding] = []
    timeline: List[Dict[str, Any]] = []
    raw_logs: List[str] = []


# ======================================================================
# Persistence models
# ======================================================================

class DrillSchedule(BaseModel):
    """A recurring or one-off drill schedule."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    cron: Optional[str] = None  # cron expression, None for one-off
    config: DrillConfig
    active: bool = True
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


class DrillRun(BaseModel):
    """Record of a single drill execution."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    schedule_id: Optional[str] = None
    client_id: str
    config: DrillConfig
    status: DrillStatus = DrillStatus.PENDING
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    result_summary: Optional[DrillResult] = None
    report_path: Optional[str] = None


# ======================================================================
# Simple JSON-file persistence (swap for SQLAlchemy in production)
# ======================================================================

class DrillStore:
    """
    Lightweight JSON-backed store for drill schedules and runs.

    In production, replace with SQLAlchemy / PostgreSQL.
    """

    def __init__(self, storage_dir: str = "/var/guardrail/redteam_data"):
        self._dir = Path(storage_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._schedules_file = self._dir / "schedules.json"
        self._runs_file = self._dir / "runs.json"

    # ---------- schedules ----------

    def _load_schedules(self) -> Dict[str, dict]:
        if self._schedules_file.exists():
            return json.loads(self._schedules_file.read_text())
        return {}

    def _save_schedules(self, data: Dict[str, dict]) -> None:
        self._schedules_file.write_text(json.dumps(data, indent=2))

    def save_schedule(self, sched: DrillSchedule) -> None:
        data = self._load_schedules()
        data[sched.id] = sched.model_dump()
        self._save_schedules(data)

    def get_schedule(self, schedule_id: str) -> Optional[DrillSchedule]:
        data = self._load_schedules()
        raw = data.get(schedule_id)
        return DrillSchedule(**raw) if raw else None

    def list_schedules(self, client_id: str) -> List[DrillSchedule]:
        data = self._load_schedules()
        return [
            DrillSchedule(**v) for v in data.values()
            if v["client_id"] == client_id
        ]

    def delete_schedule(self, schedule_id: str) -> bool:
        data = self._load_schedules()
        if schedule_id in data:
            del data[schedule_id]
            self._save_schedules(data)
            return True
        return False

    # ---------- runs ----------

    def _load_runs(self) -> Dict[str, dict]:
        if self._runs_file.exists():
            return json.loads(self._runs_file.read_text())
        return {}

    def _save_runs(self, data: Dict[str, dict]) -> None:
        self._runs_file.write_text(json.dumps(data, indent=2))

    def save_run(self, run: DrillRun) -> None:
        data = self._load_runs()
        data[run.id] = run.model_dump()
        self._save_runs(data)

    def get_run(self, drill_id: str) -> Optional[DrillRun]:
        data = self._load_runs()
        raw = data.get(drill_id)
        return DrillRun(**raw) if raw else None

    def list_runs(self, client_id: str) -> List[DrillRun]:
        data = self._load_runs()
        return [
            DrillRun(**v) for v in data.values()
            if v["client_id"] == client_id
        ]
