# File: tests/adversarial_test_phase115_community.py
"""
Phase 115 - Adversarial Tests for Community Edition Feature Gating
"""
import pytest
from fastapi.testclient import TestClient
import os

# Set environment variable before importing config/app
os.environ["COMMUNITY_EDITION"] = "True"

from app.main import app
from app.core.config import settings
from app.community.feature_gate import FeatureGate

client = TestClient(app)

class TestCommunityEditionGating:
    
    def test_config_loaded_correctly(self):
        assert settings.COMMUNITY_EDITION is True
        
    def test_feature_gate_logic(self):
        # By default, enterprise features are disabled
        assert FeatureGate.is_enabled("MULTI_JURISDICTION") is False
        assert FeatureGate.is_enabled("RT_RTAAS") is False
        
        # Test overriding a feature via config
        settings.DISABLED_FEATURES = ["RT_RTAAS"]
        settings.COMMUNITY_EDITION = False # mock enterprise mode
        assert FeatureGate.is_enabled("RT_RTAAS") is False
        assert FeatureGate.is_enabled("MULTI_JURISDICTION") is True
        
        # Reset
        settings.COMMUNITY_EDITION = True
        settings.DISABLED_FEATURES = []

    def test_enterprise_endpoint_blocked(self):
        """Verify middleware blocks access to enterprise routes."""
        settings.COMMUNITY_EDITION = True
        
        endpoints_to_test = [
            "/api/v1/underwriting/proof",
            "/api/v1/insurance/risk-attestation",
            "/api/v1/chaos/age-veto-queue"
        ]
        
        for endpoint in endpoints_to_test:
            # We don't care about the payload, just the 403 rejection
            if "chaos" in endpoint or "proof" in endpoint:
                response = client.post(endpoint, json={"control_id": "test", "period_start": 0, "period_end": 1})
            else:
                response = client.get(endpoint)
            assert response.status_code == 403
            data = response.json()
            assert data["error"] == "Community Edition Limit"
            assert "upgrade Guardrail.ai" in data["message"]

    def test_core_endpoint_allowed(self):
        """Verify core features remain accessible."""
        settings.COMMUNITY_EDITION = True
        
        # Health check
        response = client.get("/health")
        assert response.status_code == 200
        
        # Veto queue dashboard
        response = client.get("/api/dashboard/veto-queue")
        assert response.status_code == 200

    def test_limits_enforced(self):
        settings.COMMUNITY_EDITION = True
        settings.MAX_AGENTS = 5
        
        # Under limit
        assert FeatureGate.check_agent_limit(4) is True
        
        # Over limit
        assert FeatureGate.check_agent_limit(5) is False
        
        # Enterprise has no limit
        settings.COMMUNITY_EDITION = False
        assert FeatureGate.check_agent_limit(999) is True
        settings.COMMUNITY_EDITION = True
