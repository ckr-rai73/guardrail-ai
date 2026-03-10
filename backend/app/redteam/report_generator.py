# File: app/redteam/report_generator.py
"""
Phase 112 – Red-Team Report Generator
========================================
Produces executive-friendly HTML reports from drill results using
Jinja2 templates.  PDF generation is stubbed (uses weasyprint when
available, falls back to HTML-only).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from jinja2 import Environment, BaseLoader

from app.redteam.models import DrillResult, DrillRun

logger = logging.getLogger("guardrail.redteam.report")


# ======================================================================
# Embedded HTML template (no external files needed)
# ======================================================================

_REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Red-Team Drill Report – {{ drill_id }}</title>
<style>
  :root { --primary: #1e293b; --accent: #3b82f6; --danger: #ef4444;
          --success: #22c55e; --warning: #f59e0b; --bg: #f8fafc; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: 'Inter','Segoe UI',sans-serif; color: var(--primary);
         background: var(--bg); line-height: 1.6; padding: 2rem; }
  .container { max-width: 900px; margin: 0 auto; }
  h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
  h2 { font-size: 1.3rem; color: var(--accent); margin: 1.5rem 0 0.5rem; border-bottom: 2px solid var(--accent); padding-bottom: 4px; }
  h3 { font-size: 1.1rem; margin: 1rem 0 0.5rem; }
  .meta { color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }
  .badge { display:inline-block; padding: 2px 10px; border-radius:12px; font-size:0.8rem; font-weight:600; color:#fff; }
  .badge-pass { background: var(--success); }
  .badge-fail { background: var(--danger); }
  .badge-warn { background: var(--warning); }
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px,1fr)); gap: 1rem; margin: 1rem 0; }
  .kpi { background:#fff; border-radius:8px; padding:1rem; text-align:center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  .kpi-value { font-size: 1.8rem; font-weight: 700; color: var(--accent); }
  .kpi-label { font-size: 0.8rem; color: #64748b; }
  table { width:100%; border-collapse:collapse; margin:0.5rem 0 1rem; font-size:0.9rem; }
  th, td { padding: 8px 12px; border: 1px solid #e2e8f0; text-align: left; }
  th { background: var(--primary); color:#fff; }
  tr:nth-child(even) { background: #f1f5f9; }
  .sev-CRITICAL { color: var(--danger); font-weight:700; }
  .sev-HIGH { color: #dc2626; font-weight:600; }
  .sev-MEDIUM { color: var(--warning); }
  .sev-LOW { color: var(--success); }
  .footer { margin-top:2rem; padding-top:1rem; border-top:1px solid #e2e8f0; font-size:0.8rem; color:#94a3b8; }
</style>
</head>
<body>
<div class="container">

<h1>🔴 Red-Team Drill Report</h1>
<div class="meta">
  Drill ID: <strong>{{ drill_id }}</strong> &nbsp;|&nbsp;
  Client: <strong>{{ client_id }}</strong> &nbsp;|&nbsp;
  Status: <span class="badge {% if status == 'completed' %}badge-pass{% elif status == 'failed' %}badge-fail{% else %}badge-warn{% endif %}">{{ status | upper }}</span>
  <br/>
  Started: {{ started_at }} &nbsp;|&nbsp; Ended: {{ ended_at }}
  &nbsp;|&nbsp; Profile: {{ attack_profile }}
</div>

<h2>📊 Executive Summary</h2>
<p>
  This automated adversarial drill executed <strong>{{ result.total_attempts }}</strong> attack
  attempts against <strong>{{ target_count }}</strong> staging agent(s).
  The platform <strong>detected and blocked {{ result.blocked }}</strong> attacks
  ({{ (result.detection_rate * 100) | round(1) }}% detection rate).
  {% if result.bypassed > 0 %}
  <span class="badge badge-warn">{{ result.bypassed }} attack(s) bypassed detection</span> —
  see remediation recommendations below.
  {% else %}
  <span class="badge badge-pass">Zero bypasses — all attacks blocked</span>.
  {% endif %}
</p>

<div class="kpi-grid">
  <div class="kpi"><div class="kpi-value">{{ result.total_attempts }}</div><div class="kpi-label">Total Attempts</div></div>
  <div class="kpi"><div class="kpi-value">{{ result.blocked }}</div><div class="kpi-label">Blocked</div></div>
  <div class="kpi"><div class="kpi-value">{{ result.bypassed }}</div><div class="kpi-label">Bypassed</div></div>
  <div class="kpi"><div class="kpi-value">{{ (result.detection_rate * 100) | round(1) }}%</div><div class="kpi-label">Detection Rate</div></div>
  <div class="kpi"><div class="kpi-value">{{ result.mean_response_ms | round(1) }}ms</div><div class="kpi-label">Mean Response</div></div>
  <div class="kpi"><div class="kpi-value">{{ result.p99_response_ms | round(1) }}ms</div><div class="kpi-label">P99 Latency</div></div>
</div>

{% if result.vulnerabilities %}
<h2>🛑 Vulnerabilities Found ({{ result.vulnerabilities | length }})</h2>
<table>
  <tr><th>#</th><th>Attack Type</th><th>Severity</th><th>Description</th><th>Policy</th><th>Compliance Impact</th></tr>
  {% for v in result.vulnerabilities %}
  <tr>
    <td>{{ loop.index }}</td>
    <td>{{ v.attack_type }}</td>
    <td class="sev-{{ v.severity }}">{{ v.severity }}</td>
    <td>{{ v.description }}</td>
    <td>{{ v.policy_id or '—' }}</td>
    <td>{{ v.compliance_impact or '—' }}</td>
  </tr>
  {% endfor %}
</table>

<h2>🔧 Remediation Recommendations</h2>
<ol>
{% for v in result.vulnerabilities %}
  <li><strong>{{ v.attack_type }}</strong> ({{ v.severity }}): {{ v.remediation }}</li>
{% endfor %}
</ol>
{% endif %}

{% if result.timeline %}
<h2>📈 Attack Timeline</h2>
<table>
  <tr><th>#</th><th>Attack Type</th><th>Result</th><th>Response (ms)</th></tr>
  {% for e in result.timeline[:50] %}
  <tr>
    <td>{{ e.attempt }}</td>
    <td>{{ e.type }}</td>
    <td>
      {% if e.result == 'BLOCKED' %}<span class="badge badge-pass">BLOCKED</span>
      {% else %}<span class="badge badge-fail">BYPASSED</span>{% endif %}
    </td>
    <td>{{ e.response_ms }}</td>
  </tr>
  {% endfor %}
  {% if result.timeline | length > 50 %}
  <tr><td colspan="4"><em>… {{ result.timeline | length - 50 }} more entries omitted</em></td></tr>
  {% endif %}
</table>
{% endif %}

<div class="footer">
  Generated by Guardrail.ai RT-RTaaS · Phase 112 · {{ generated_at }}
</div>

</div>
</body>
</html>
"""


# ======================================================================
# Report Generator
# ======================================================================

class ReportGenerator:
    """
    Generate HTML (and optionally PDF) drill reports.

    Parameters
    ----------
    storage_path : str
        Directory to store generated report files.
    """

    def __init__(self, storage_path: str = "/var/guardrail/redteam_reports"):
        self._storage = Path(storage_path)
        self._storage.mkdir(parents=True, exist_ok=True)
        self._env = Environment(loader=BaseLoader())
        self._template = self._env.from_string(_REPORT_TEMPLATE)

    def generate_report(
        self,
        drill_run: DrillRun,
        fmt: str = "html",
    ) -> bytes:
        """
        Render a drill report.

        Parameters
        ----------
        drill_run : DrillRun
            Completed drill with result_summary populated.
        fmt : str
            Output format: ``"html"`` or ``"pdf"`` (PDF falls back to HTML
            if weasyprint is unavailable).

        Returns
        -------
        bytes
            The report content.
        """
        if not drill_run.result_summary:
            raise ValueError(f"Drill {drill_run.id} has no result_summary")

        html = self._render_html(drill_run)

        if fmt == "pdf":
            try:
                return self._html_to_pdf(html)
            except ImportError:
                logger.warning(
                    "[ReportGenerator] weasyprint not available – "
                    "falling back to HTML"
                )

        return html.encode("utf-8")

    def generate_and_save(
        self,
        drill_run: DrillRun,
        fmt: str = "html",
    ) -> str:
        """Generate and persist the report. Returns the file path."""
        content = self.generate_report(drill_run, fmt=fmt)
        ext = "pdf" if fmt == "pdf" else "html"
        path = self._storage / f"report_{drill_run.id}.{ext}"
        path.write_bytes(content)
        logger.info("[ReportGenerator] Report saved: %s", path)
        return str(path)

    def _render_html(self, drill_run: DrillRun) -> str:
        """Render the Jinja2 template to HTML string."""
        result = drill_run.result_summary
        return self._template.render(
            drill_id=drill_run.id,
            client_id=drill_run.client_id,
            status=drill_run.status.value if drill_run.status else "unknown",
            started_at=drill_run.started_at or "—",
            ended_at=drill_run.ended_at or "—",
            attack_profile=drill_run.config.attack_profile.value,
            target_count=len(drill_run.config.target_agent_ids),
            result=result,
            generated_at=datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            ),
        )

    @staticmethod
    def _html_to_pdf(html: str) -> bytes:
        """Convert HTML to PDF using weasyprint."""
        from weasyprint import HTML  # type: ignore[import-untyped]
        return HTML(string=html).write_pdf()
