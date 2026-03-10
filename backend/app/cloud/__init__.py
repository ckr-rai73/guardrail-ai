# File: app/cloud/__init__.py
"""
Phase 111: Cloud Native Governance Plugins
==========================================
Provides abstract connectors for AWS, Azure, and GCP cloud marketplaces,
with unified governance assessment and billing metering.
"""

from app.cloud.cloud_connector_base import CloudConnectorBase
from app.cloud.billing_adapter import CloudBillingAdapter

__all__ = ["CloudConnectorBase", "CloudBillingAdapter"]
