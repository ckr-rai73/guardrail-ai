"""
Phase 110: Test RegulatoryMapper with skill files.
Verifies that all jurisdiction skill files are present and can be loaded,
and that required controls are correctly returned.
"""

import pytest
from app.jurisdiction.mapper import RegulatoryMapper

# Expected jurisdictions based on the skill files we created
EXPECTED_JURISDICTIONS = {
    "BR-LGPD",
    "IN-DPDPA",
    "JP-APPI",
    "EU-AI-ACT",
    "US-DISCOVERY-HOLD",
    "ZA-POPIA"
}

# For a given jurisdiction, expected controls (from the template we used)
EXPECTED_CONTROLS = {
    "Phase 1 Veto Protocol",
    "Phase 21 Compliance Traceability",
    "Phase 23 Jurisdictional Shader",
    "Phase 101 Evidentiary Bridge"
}

def test_skill_files_exist():
    """Test that all expected jurisdiction skill files are present."""
    mapper = RegulatoryMapper()
    available = set(mapper.list_jurisdictions())
    assert available == EXPECTED_JURISDICTIONS, f"Missing or extra jurisdictions: expected {EXPECTED_JURISDICTIONS}, got {available}"

def test_load_skill_and_controls():
    """Test that each jurisdiction skill can be loaded and returns expected controls."""
    mapper = RegulatoryMapper()
    for jur in EXPECTED_JURISDICTIONS:
        controls, score = mapper.assess_action(jur, {"dummy": "context"})
        # Check that the required controls set is a superset of our expected controls
        # (the skill might have additional lines/comments, but we check essential ones)
        control_set = set(controls)
        assert EXPECTED_CONTROLS.issubset(control_set), f"Jurisdiction {jur} missing expected controls. Got: {control_set}"
        # Score should be 1.0 (default) since skill exists
        assert score == 1.0, f"Score for {jur} should be 1.0, got {score}"

def test_assess_action_with_unknown_jurisdiction():
    """Test that an unknown jurisdiction returns empty controls and score 1.0."""
    mapper = RegulatoryMapper()
    controls, score = mapper.assess_action("NONEXISTENT", {})
    assert controls == [], f"Expected empty controls for unknown jurisdiction, got {controls}"
    assert score == 1.0, f"Expected score 1.0 for unknown jurisdiction, got {score}"
