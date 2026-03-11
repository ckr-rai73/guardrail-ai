# File: app/compliance/continuous_compliance_dashboard.py
"""
Phase 114: Continuous Compliance Dashboard
============================================
Internal FastAPI endpoints providing real-time visibility into
the organisation's compliance posture across all supported frameworks.

These endpoints sit behind admin authentication (simulated) and are
intended for internal SOC / GRC teams.
"""

import hashlib
import time
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.compliance.control_mapper import ControlMapper
from app.compliance.evidence_collector import EvidenceCollector

logger = logging.getLogger(__name__)

# ======================================================================
# Router
# ======================================================================
router = APIRouter(prefix="/dashboard", tags=["Compliance Dashboard – Phase 114"])

# ======================================================================
# Shared state
# ======================================================================
_mapper = ControlMapper()
_collector = EvidenceCollector(control_mapper=_mapper)

# In-memory compliance history (production: time-series DB)
_compliance_history: List[Dict[str, Any]] = []


# ======================================================================
# Admin auth dependency
# ======================================================================
def _require_admin(x_admin_key: str = Header(default="")) -> str:
    """Simple admin key check.  In production, integrate with OIDC / RBAC."""
    valid_keys = {"ADMIN-KEY-INTERNAL-001", "ADMIN-KEY-DEV"}
    if x_admin_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin authentication required.",
        )
    return x_admin_key


# ======================================================================
# Endpoints
# ======================================================================

@router.get("/status")
async def dashboard_status(
    _admin: str = Depends(_require_admin),
):
    """
    Return a high-level compliance summary per framework.

    Each framework shows ``compliant``, ``non_compliant``, or
    ``under_review`` based on the latest evidence collection run.
    """
    summaries: List[Dict[str, Any]] = []
    now = time.time()

    for fw_id in _mapper.list_frameworks():
        # Quick evidence snapshot (last 24 hours)
        try:
            evidence = await _collector.collect_evidence(
                framework=fw_id,
                time_range=(now - 86400, now),
            )
            items = evidence.get("evidence_items", [])
            compliant = sum(
                1 for i in items
                if any(e.get("record_count", 0) > 0 for e in i.get("evidence", []))
            )
            total = len(items)
            pct = (compliant / total * 100) if total else 0

            if pct >= 100:
                overall_status = "compliant"
            elif pct >= 80:
                overall_status = "under_review"
            else:
                overall_status = "non_compliant"

            summaries.append({
                "framework": fw_id,
                "status": overall_status,
                "compliant_controls": compliant,
                "total_controls": total,
                "compliance_percentage": round(pct, 1),
                "last_checked": now,
            })
        except Exception as exc:
            logger.exception("Error evaluating %s", fw_id)
            summaries.append({
                "framework": fw_id,
                "status": "error",
                "error": str(exc),
            })

    # Record history snapshot
    _compliance_history.append({
        "timestamp": now,
        "summaries": summaries,
    })
    # Keep bounded
    if len(_compliance_history) > 1000:
        _compliance_history.pop(0)

    return {"timestamp": now, "frameworks": summaries}


@router.get("/controls")
async def dashboard_controls(
    framework: str = "ISO_42001",
    _admin: str = Depends(_require_admin),
):
    """
    Return a detailed list of controls for *framework* with the latest
    evidence timestamps and collection status.
    """
    now = time.time()
    evidence = await _collector.collect_evidence(
        framework=framework,
        time_range=(now - 86400, now),
    )
    controls: List[Dict[str, Any]] = []

    for item in evidence.get("evidence_items", []):
        has_evidence = any(
            e.get("record_count", 0) > 0 for e in item.get("evidence", [])
        )
        controls.append({
            "control_id": item["control_id"],
            "title": item.get("title", ""),
            "status": "compliant" if has_evidence else "non_compliant",
            "evidence_hash": item.get("evidence_hash", ""),
            "evidence_sources": len(item.get("evidence", [])),
            "last_evidence_timestamp": now,
        })

    return {
        "framework": framework,
        "timestamp": now,
        "controls": controls,
    }


@router.get("/history")
async def dashboard_history(
    limit: int = 50,
    _admin: str = Depends(_require_admin),
):
    """
    Return a time-series of compliance scores from recent evaluation runs.
    """
    recent = _compliance_history[-limit:]

    series: List[Dict[str, Any]] = []
    for snap in recent:
        for summary in snap.get("summaries", []):
            series.append({
                "timestamp": snap["timestamp"],
                "framework": summary.get("framework"),
                "compliance_percentage": summary.get("compliance_percentage", 0),
                "status": summary.get("status", "unknown"),
            })

    return {
        "total_snapshots": len(recent),
        "series": series,
    }
