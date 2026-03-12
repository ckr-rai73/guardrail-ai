# File: app/community/feature_gate.py
"""
Phase 115 - Open Source Community Edition
Feature Gate Service
"""
from typing import List
from app.core.config import settings

class FeatureGate:
    """
    Centralised feature flag service for the Community Edition.
    Loads configuration from environment variables or a config file to gate enterprise features.
    """
    # Enterprise features that are disabled by default in community mode
    ENTERPRISE_FEATURES = {
        "MULTI_JURISDICTION",
        "INSURANCE_ORACLE",
        "UNDERWRITING_GATEWAY",
        "RT_RTAAS",
        "CLOUD_CONNECTORS",
    }
    
    @classmethod
    def is_enabled(cls, feature: str) -> bool:
        """Check if a specific feature is enabled."""
        if not settings.COMMUNITY_EDITION:
            # All features enabled in enterprise mode by default
            return feature not in settings.DISABLED_FEATURES
            
        # Allow enabling specific features even in community edition via config overrides
        # But by default, if it's an enterprise feature, it's disabled.
        if feature in settings.DISABLED_FEATURES:
            return False
            
        return feature not in cls.ENTERPRISE_FEATURES

    @classmethod
    def check_agent_limit(cls, current_count: int) -> bool:
        """Enforces limits on the number of active agents."""
        if not settings.COMMUNITY_EDITION:
            return True
        return current_count < settings.MAX_AGENTS

    @classmethod
    def check_tenant_limit(cls, current_count: int) -> bool:
        """Enforces limits on the number of tenants."""
        if not settings.COMMUNITY_EDITION:
            return True
        return current_count < settings.MAX_TENANTS

    @classmethod
    def check_drill_limit(cls, current_count: int) -> bool:
        """Enforces limits on RT-RTaaS drills."""
        if not settings.COMMUNITY_EDITION:
            return True
        return current_count < settings.MAX_DRILLS_PER_MONTH
