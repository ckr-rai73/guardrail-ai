# File: app/compliance/control_mapper.py
"""
Phase 114: Control Mapper
==========================
Maps Guardrail.ai internal controls to external compliance framework
requirements by loading framework definitions from YAML files.

Supports: ISO 42001, SOC 2, FedRAMP, EU AI Act, NIST AI RMF.
"""

import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Try to import yaml; fall back to a simple parser if unavailable.
try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    yaml = None  # type: ignore[assignment]


def _load_yaml_file(path: str) -> Dict[str, Any]:
    """Load a YAML file, falling back to json if PyYAML is absent."""
    with open(path, "r", encoding="utf-8") as fh:
        if yaml is not None:
            return yaml.safe_load(fh)  # type: ignore[union-attr]
        # Minimal fallback – not full YAML, but enough for tests
        import json
        return json.load(fh)


# Default directory for framework definitions
_DEFAULT_FRAMEWORKS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "frameworks",
)


class ControlMapper:
    """
    Loads compliance framework definitions and maps each external
    control to the internal Guardrail.ai evidence sources that
    demonstrate conformity.

    Usage::

        mapper = ControlMapper()
        frameworks = mapper.list_frameworks()
        reqs = mapper.get_requirements("ISO_42001")
        mapping = mapper.map_control("ISO42001-6.1")
    """

    def __init__(self, frameworks_dir: Optional[str] = None):
        """
        Load all framework YAML files from *frameworks_dir*.

        Args:
            frameworks_dir: Path to the directory containing ``*.yaml``
                framework definitions.  Defaults to ``<project>/frameworks/``.
        """
        self._frameworks_dir = frameworks_dir or _DEFAULT_FRAMEWORKS_DIR
        self._frameworks: Dict[str, Dict[str, Any]] = {}
        self._control_index: Dict[str, Dict[str, Any]] = {}
        self._load_frameworks()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_frameworks(self) -> List[str]:
        """Return the list of supported framework IDs."""
        return list(self._frameworks.keys())

    def get_framework_meta(self, framework: str) -> Dict[str, Any]:
        """Return metadata (id, name, title, version, description) for a framework."""
        fw = self._frameworks.get(framework)
        if fw is None:
            raise ValueError(f"Unknown framework: {framework}")
        meta = dict(fw["framework"])
        meta.pop("controls", None)  # strip bulky controls list from meta
        return meta

    def get_requirements(self, framework: str) -> List[Dict[str, Any]]:
        """
        Return the list of control requirements for *framework*.

        Each item is a dict with keys ``id``, ``title``, ``description``,
        and ``evidence_sources``.
        """
        fw = self._frameworks.get(framework)
        if fw is None:
            raise ValueError(f"Unknown framework: {framework}")
        return fw.get("controls", [])

    def map_control(self, control_id: str) -> Dict[str, Any]:
        """
        Return a mapping dict for a single *control_id*.

        The returned dict contains:
        - ``control_id``
        - ``framework`` – the owning framework ID
        - ``title``
        - ``description``
        - ``evidence_sources`` – list of internal evidence queries
        """
        entry = self._control_index.get(control_id)
        if entry is None:
            raise ValueError(f"Unknown control ID: {control_id}")
        return entry

    def get_all_controls(self) -> Dict[str, Dict[str, Any]]:
        """Return the full control index mapping control_id -> mapping dict."""
        return dict(self._control_index)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_frameworks(self) -> None:
        """Scan the frameworks directory and parse every YAML file."""
        fw_dir = Path(self._frameworks_dir)
        if not fw_dir.is_dir():
            logger.warning("Frameworks directory not found: %s", fw_dir)
            return

        for yaml_path in sorted(fw_dir.glob("*.yaml")):
            try:
                data = _load_yaml_file(str(yaml_path))
                fw_meta = data.get("framework", {})
                fw_id = fw_meta.get("id")
                if not fw_id:
                    logger.warning("Skipping %s – no framework.id", yaml_path.name)
                    continue

                controls = data.get("controls", [])
                self._frameworks[fw_id] = {
                    "framework": fw_meta,
                    "controls": controls,
                    "source_file": str(yaml_path),
                }

                # Build per-control index
                for ctrl in controls:
                    cid = ctrl.get("id")
                    if cid:
                        self._control_index[cid] = {
                            "control_id": cid,
                            "framework": fw_id,
                            "title": ctrl.get("title", ""),
                            "description": ctrl.get("description", ""),
                            "evidence_sources": ctrl.get("evidence_sources", []),
                        }

                logger.info(
                    "Loaded framework %s with %d controls from %s",
                    fw_id,
                    len(controls),
                    yaml_path.name,
                )
            except Exception:
                logger.exception("Failed to load framework file %s", yaml_path.name)

    def __repr__(self) -> str:
        return (
            f"<ControlMapper frameworks={list(self._frameworks.keys())} "
            f"controls={len(self._control_index)}>"
        )
