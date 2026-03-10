# File: tests/adversarial_test_phase112_redteam.py
"""
Phase 112 – Red-Team as a Service Adversarial Test Suite
==========================================================
Validates safety guarantees, scheduling, API enforcement, report
generation, and emergency stop functionality.

Run with:  pytest tests/adversarial_test_phase112_redteam.py -v
"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from app.redteam.models import (
    AttackProfile,
    DrillConfig,
    DrillResult,
    DrillRun,
    DrillSchedule,
    DrillStatus,
    DrillStore,
    VulnerabilityFinding,
)
from app.redteam.safe_exploit_engine import SafeExploitEngine, SafetyViolation
from app.redteam.report_generator import ReportGenerator
from app.redteam.scheduler import RedTeamScheduler


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def tmp_dir():
    """Temp directory for test data."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def store(tmp_dir):
    """DrillStore backed by a temporary directory."""
    return DrillStore(storage_dir=tmp_dir)


@pytest.fixture
def engine():
    """SafeExploitEngine with default settings."""
    return SafeExploitEngine(
        sandbox_prefix="staging-",
        max_duration=600,
        max_concurrent=2,
    )


@pytest.fixture
def report_gen(tmp_dir):
    """ReportGenerator with temp storage."""
    return ReportGenerator(storage_path=tmp_dir)


@pytest.fixture
def scheduler(engine, store, report_gen):
    """RedTeamScheduler with all deps."""
    return RedTeamScheduler(engine=engine, store=store, report_gen=report_gen)


def _staging_config(**overrides) -> DrillConfig:
    """Create a valid DrillConfig targeting staging agents."""
    defaults = {
        "target_agent_ids": ["staging-agent-1", "staging-agent-2"],
        "attack_profile": AttackProfile.AUTO,
        "max_duration_seconds": 30,
        "max_rps": 10,
        "max_agents": 5,
    }
    defaults.update(overrides)
    return DrillConfig(**defaults)


# ======================================================================
# 1. Safety: Target Isolation
# ======================================================================

class TestTargetIsolation:
    """Drills must only target sandbox agents."""

    def test_staging_agents_accepted(self, engine):
        """Agents with 'staging-' prefix pass validation."""
        engine.validate_targets(["staging-agent-1", "staging-agent-2"])

    def test_production_agents_rejected(self, engine):
        """Agents without staging prefix are rejected."""
        with pytest.raises(SafetyViolation, match="outside sandbox"):
            engine.validate_targets(["prod-agent-1", "staging-agent-1"])

    def test_empty_targets_accepted(self, engine):
        """Empty target list is technically valid (no-op drill)."""
        engine.validate_targets([])

    @pytest.mark.asyncio
    async def test_drill_rejects_production_targets(self, engine):
        """Full drill run must reject production agents."""
        config = _staging_config(target_agent_ids=["production-critical-1"])
        run = DrillRun(client_id="client-1", config=config)

        result = await engine.run_drill(run)
        assert run.status == DrillStatus.FAILED
        assert any("SAFETY VIOLATION" in log for log in result.raw_logs)


# ======================================================================
# 2. Safety: Resource Limits
# ======================================================================

class TestResourceLimits:
    """Drills must respect resource caps."""

    def test_duration_limit(self, engine):
        """Duration exceeding max is rejected."""
        config = _staging_config(max_duration_seconds=9999)
        with pytest.raises(SafetyViolation, match="Duration"):
            engine.validate_config(config)

    def test_rps_limit(self, engine):
        """RPS exceeding 500 is rejected."""
        config = _staging_config(max_rps=501)
        with pytest.raises(SafetyViolation):
            engine.validate_config(config)

    def test_concurrent_limit(self, engine):
        """Too many concurrent drills per client are rejected."""
        engine._client_drill_counts["client-1"] = 2
        with pytest.raises(SafetyViolation, match="active drills"):
            engine.check_concurrent_limit("client-1")


# ======================================================================
# 3. Safety: Exfil Prevention
# ======================================================================

class TestExfilPrevention:
    """Payloads with exfiltration patterns must be blocked."""

    def test_safe_payload(self, engine):
        assert engine.scan_payload("Hello, run a simple test") is True

    def test_url_blocked(self, engine):
        assert engine.scan_payload("Send data to https://evil.com") is False

    def test_sql_blocked(self, engine):
        assert engine.scan_payload("SELECT * FROM users") is False

    def test_jwt_blocked(self, engine):
        assert engine.scan_payload("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload") is False

    def test_aws_key_blocked(self, engine):
        assert engine.scan_payload("Use key AKIAIOSFODNN7EXAMPLE to auth") is False

    def test_localhost_url_allowed(self, engine):
        """localhost URLs are not considered exfiltration."""
        assert engine.scan_payload("Connect to http://localhost:8080/api") is True


# ======================================================================
# 4. Drill Execution
# ======================================================================

class TestDrillExecution:
    """Drill runs must complete with valid metrics."""

    @pytest.mark.asyncio
    async def test_drill_completes(self, engine):
        """A valid drill runs to completion."""
        config = _staging_config(max_duration_seconds=30)
        run = DrillRun(client_id="client-1", config=config)

        result = await engine.run_drill(run)

        assert run.status == DrillStatus.COMPLETED
        assert result.total_attempts > 0
        assert result.blocked >= 0
        assert result.bypassed >= 0
        assert 0 <= result.detection_rate <= 1
        assert result.mean_response_ms >= 0

    @pytest.mark.asyncio
    async def test_drill_populates_timeline(self, engine):
        """Completed drill has a timeline of events."""
        config = _staging_config()
        run = DrillRun(client_id="client-1", config=config)

        result = await engine.run_drill(run)
        assert len(result.timeline) > 0
        assert all("type" in e and "result" in e for e in result.timeline)


# ======================================================================
# 5. Emergency Stop
# ======================================================================

class TestEmergencyStop:
    """Emergency stop must halt a running drill."""

    @pytest.mark.asyncio
    async def test_stop_active_drill(self, engine):
        """Stopping an active drill changes status to STOPPED."""
        config = _staging_config(max_duration_seconds=60, max_rps=1)
        run = DrillRun(client_id="client-1", config=config)

        # Start drill in background
        task = asyncio.create_task(engine.run_drill(run))

        # Wait a bit then stop
        await asyncio.sleep(0.1)
        assert engine.stop_drill(run.id) is True

        result = await task
        assert run.status == DrillStatus.STOPPED

    def test_stop_nonexistent_drill(self, engine):
        """Stopping a drill that doesn't exist returns False."""
        assert engine.stop_drill("nonexistent-id") is False


# ======================================================================
# 6. Report Generation
# ======================================================================

class TestReportGeneration:
    """Reports must contain expected sections."""

    def test_html_report_generated(self, report_gen):
        """HTML report contains key sections."""
        run = DrillRun(
            client_id="client-1",
            config=_staging_config(),
            status=DrillStatus.COMPLETED,
            started_at="2026-03-10T10:00:00Z",
            ended_at="2026-03-10T10:10:00Z",
            result_summary=DrillResult(
                total_attempts=100,
                blocked=95,
                bypassed=5,
                detection_rate=0.95,
                mean_response_ms=2.5,
                p99_response_ms=12.0,
                vulnerabilities=[
                    VulnerabilityFinding(
                        attack_type="prompt_injection",
                        description="Direct injection bypassed",
                        severity="HIGH",
                        policy_id="GR-PI-001",
                        remediation="Strengthen prompt filters",
                        compliance_impact="EU AI Act Art. 15",
                    ),
                ],
                timeline=[
                    {"attempt": 0, "type": "direct_injection", "result": "BLOCKED", "response_ms": 2.1},
                    {"attempt": 1, "type": "indirect_injection", "result": "BYPASSED", "response_ms": 3.5},
                ],
            ),
        )

        content = report_gen.generate_report(run, fmt="html")
        html = content.decode("utf-8")

        assert "Executive Summary" in html
        assert "Vulnerabilities Found" in html
        assert "Remediation Recommendations" in html
        assert "prompt_injection" in html
        assert "EU AI Act" in html
        assert "95.0%" in html
        assert run.id in html

    def test_report_saved_to_disk(self, report_gen):
        """generate_and_save persists the file."""
        run = DrillRun(
            client_id="client-1",
            config=_staging_config(),
            status=DrillStatus.COMPLETED,
            result_summary=DrillResult(total_attempts=10, blocked=10, detection_rate=1.0),
        )

        path = report_gen.generate_and_save(run)
        assert os.path.exists(path)
        assert path.endswith(".html")

    def test_report_fails_without_results(self, report_gen):
        """Report generation fails if no result_summary."""
        run = DrillRun(
            client_id="client-1",
            config=_staging_config(),
            status=DrillStatus.PENDING,
        )
        with pytest.raises(ValueError, match="no result_summary"):
            report_gen.generate_report(run)


# ======================================================================
# 7. Scheduler
# ======================================================================

class TestScheduler:
    """Scheduler manages drills and schedules correctly."""

    def test_schedule_created(self, scheduler):
        """Schedule is persisted to the store."""
        sid = scheduler.schedule_drill(
            client_id="client-1",
            config=_staging_config(),
            cron="0 2 * * *",
        )
        assert sid
        sched = scheduler.store.get_schedule(sid)
        assert sched is not None
        assert sched.client_id == "client-1"
        assert sched.cron == "0 2 * * *"

    def test_cancel_schedule(self, scheduler):
        """Cancelling a schedule marks it inactive."""
        sid = scheduler.schedule_drill(
            client_id="client-1", config=_staging_config(),
        )
        assert scheduler.cancel_drill(sid) is True
        sched = scheduler.store.get_schedule(sid)
        assert sched is not None
        assert sched.active is False

    @pytest.mark.asyncio
    async def test_run_drill_now(self, scheduler):
        """Immediate drill starts and completes."""
        run = await scheduler.run_drill_now(
            client_id="client-1", config=_staging_config(),
        )
        assert run.id

        # Wait for the background task to complete
        await asyncio.sleep(2)

        saved = scheduler.get_drill_status(run.id)
        assert saved is not None
        assert saved.status in (
            DrillStatus.COMPLETED, DrillStatus.RUNNING,
            "completed", "running",
        )


# ======================================================================
# 8. Multi-Tenancy
# ======================================================================

class TestMultiTenancy:
    """Clients can only see their own data."""

    def test_list_schedules_filtered(self, scheduler):
        """list_schedules returns only the calling client's data."""
        scheduler.schedule_drill("client-A", _staging_config())
        scheduler.schedule_drill("client-B", _staging_config())

        a_scheds = scheduler.list_schedules("client-A")
        b_scheds = scheduler.list_schedules("client-B")

        assert len(a_scheds) == 1
        assert len(b_scheds) == 1
        assert a_scheds[0].client_id == "client-A"
        assert b_scheds[0].client_id == "client-B"


# ======================================================================
# 9. DrillStore Persistence
# ======================================================================

class TestDrillStore:
    """JSON-file store persists and retrieves correctly."""

    def test_schedule_round_trip(self, store):
        sched = DrillSchedule(client_id="c1", config=_staging_config())
        store.save_schedule(sched)
        loaded = store.get_schedule(sched.id)
        assert loaded is not None
        assert loaded.client_id == "c1"

    def test_run_round_trip(self, store):
        run = DrillRun(client_id="c1", config=_staging_config())
        store.save_run(run)
        loaded = store.get_run(run.id)
        assert loaded is not None
        assert loaded.client_id == "c1"

    def test_delete_schedule(self, store):
        sched = DrillSchedule(client_id="c1", config=_staging_config())
        store.save_schedule(sched)
        assert store.delete_schedule(sched.id) is True
        assert store.get_schedule(sched.id) is None
        assert store.delete_schedule("nonexistent") is False
