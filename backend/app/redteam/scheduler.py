# File: app/redteam/scheduler.py
"""
Phase 112 – Red-Team Drill Scheduler
=======================================
Manages recurring and one-off drill schedules using APScheduler (or
asyncio fallback).  Integrates with SafeExploitEngine and DrillStore.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from app.redteam.models import (
    DrillConfig,
    DrillRun,
    DrillSchedule,
    DrillStatus,
    DrillStore,
)
from app.redteam.safe_exploit_engine import SafeExploitEngine
from app.redteam.report_generator import ReportGenerator

logger = logging.getLogger("guardrail.redteam.scheduler")


class RedTeamScheduler:
    """
    Manages drill scheduling, execution, and report generation.

    Parameters
    ----------
    engine : SafeExploitEngine
        The safety-wrapped exploit engine.
    store : DrillStore
        Persistence layer for schedules and runs.
    report_gen : ReportGenerator
        Report generator for completed drills.
    """

    def __init__(
        self,
        engine: SafeExploitEngine,
        store: DrillStore,
        report_gen: ReportGenerator,
    ) -> None:
        self.engine = engine
        self.store = store
        self.report_gen = report_gen
        self._scheduler = None  # APScheduler instance (lazy init)
        self._background_tasks: dict[str, asyncio.Task] = {}

    # ------------------------------------------------------------------
    # Schedule management
    # ------------------------------------------------------------------

    def schedule_drill(
        self,
        client_id: str,
        config: DrillConfig,
        cron: Optional[str] = None,
    ) -> str:
        """
        Create a new drill schedule.

        Parameters
        ----------
        client_id : str
            Owning client.
        config : DrillConfig
            Drill configuration.
        cron : str, optional
            Cron expression for recurring drills (None = one-off).

        Returns
        -------
        str
            The schedule ID.
        """
        schedule = DrillSchedule(
            client_id=client_id,
            cron=cron,
            config=config,
        )
        self.store.save_schedule(schedule)

        logger.info(
            "[Scheduler] Drill scheduled – id=%s client=%s cron=%s",
            schedule.id, client_id, cron or "one-off",
        )

        # If cron is set, register with APScheduler
        if cron:
            self._register_cron_job(schedule)

        return schedule.id

    def cancel_drill(self, schedule_id: str) -> bool:
        """Cancel (deactivate) a schedule."""
        schedule = self.store.get_schedule(schedule_id)
        if not schedule:
            return False

        schedule.active = False
        self.store.save_schedule(schedule)

        # Remove from APScheduler if present
        self._unregister_cron_job(schedule_id)

        logger.info("[Scheduler] Schedule cancelled: %s", schedule_id)
        return True

    # ------------------------------------------------------------------
    # Immediate execution
    # ------------------------------------------------------------------

    async def run_drill_now(
        self,
        client_id: str,
        config: DrillConfig,
        schedule_id: Optional[str] = None,
    ) -> DrillRun:
        """
        Start an immediate drill as a background task.

        Returns the DrillRun (status = PENDING initially).
        """
        run = DrillRun(
            client_id=client_id,
            schedule_id=schedule_id,
            config=config,
            status=DrillStatus.PENDING,
        )
        self.store.save_run(run)

        # Launch as background task
        task = asyncio.create_task(self._execute_drill(run))
        self._background_tasks[run.id] = task

        logger.info(
            "[Scheduler] Drill started – id=%s client=%s",
            run.id, client_id,
        )
        return run

    async def _execute_drill(self, run: DrillRun) -> None:
        """Execute a drill and generate a report on completion."""
        try:
            result = await self.engine.run_drill(run)
            run.result_summary = result

            # Generate report
            try:
                report_path = self.report_gen.generate_and_save(run)
                run.report_path = report_path
            except Exception:
                logger.exception(
                    "[Scheduler] Report generation failed for drill %s", run.id,
                )

            self.store.save_run(run)
        except Exception:
            logger.exception("[Scheduler] Drill execution failed: %s", run.id)
            run.status = DrillStatus.FAILED
            run.ended_at = datetime.now(timezone.utc).isoformat()
            self.store.save_run(run)
        finally:
            self._background_tasks.pop(run.id, None)

    # ------------------------------------------------------------------
    # Emergency stop
    # ------------------------------------------------------------------

    def stop_drill(self, drill_id: str) -> bool:
        """Emergency stop an active drill."""
        stopped = self.engine.stop_drill(drill_id)
        if stopped:
            logger.warning("[Scheduler] Emergency stop issued: %s", drill_id)
        return stopped

    # ------------------------------------------------------------------
    # Status queries
    # ------------------------------------------------------------------

    def get_drill_status(self, drill_id: str) -> Optional[DrillRun]:
        """Get the current state of a drill run."""
        return self.store.get_run(drill_id)

    def list_schedules(self, client_id: str):
        """List all schedules for a client."""
        return self.store.list_schedules(client_id)

    def list_runs(self, client_id: str):
        """List all drill runs for a client."""
        return self.store.list_runs(client_id)

    # ------------------------------------------------------------------
    # APScheduler integration (cron jobs)
    # ------------------------------------------------------------------

    def _register_cron_job(self, schedule: DrillSchedule) -> None:
        """Register a cron-triggered job with APScheduler."""
        try:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler
            from apscheduler.triggers.cron import CronTrigger

            if self._scheduler is None:
                self._scheduler = AsyncIOScheduler()
                self._scheduler.start()

            trigger = CronTrigger.from_crontab(schedule.cron)
            self._scheduler.add_job(
                self._cron_trigger_drill,
                trigger=trigger,
                id=schedule.id,
                args=[schedule],
                replace_existing=True,
            )
            logger.info(
                "[Scheduler] Cron job registered: %s → %s",
                schedule.id, schedule.cron,
            )
        except ImportError:
            logger.warning(
                "[Scheduler] apscheduler not installed – "
                "cron scheduling disabled. Install with: "
                "pip install apscheduler"
            )

    def _unregister_cron_job(self, schedule_id: str) -> None:
        """Remove a cron job from APScheduler."""
        if self._scheduler:
            try:
                self._scheduler.remove_job(schedule_id)
            except Exception:
                pass

    async def _cron_trigger_drill(self, schedule: DrillSchedule) -> None:
        """Called by APScheduler when a cron trigger fires."""
        if not schedule.active:
            return
        await self.run_drill_now(
            client_id=schedule.client_id,
            config=schedule.config,
            schedule_id=schedule.id,
        )
