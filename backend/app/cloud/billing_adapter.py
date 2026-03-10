# File: app/cloud/billing_adapter.py
"""
Phase 111 – Cloud Billing Adapter
===================================
Unified metering interface for AWS Marketplace, Azure Marketplace, and
GCP Marketplace.  Each ``record_usage`` call is dispatched to the
appropriate vendor stub.  Actual API integrations will be fleshed out in
a later step; for now every call logs the event and returns.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

logger = logging.getLogger("guardrail.cloud.billing")


class CloudBillingAdapter:
    """
    Marketplace billing / metering adapter.

    Parameters
    ----------
    marketplace : str
        One of ``"aws"``, ``"azure"``, or ``"gcp"``.
    """

    SUPPORTED_MARKETPLACES = {"aws", "azure", "gcp"}

    def __init__(self, marketplace: str) -> None:
        marketplace = marketplace.lower().strip()
        if marketplace not in self.SUPPORTED_MARKETPLACES:
            raise ValueError(
                f"Unsupported marketplace '{marketplace}'. "
                f"Choose from: {', '.join(sorted(self.SUPPORTED_MARKETPLACES))}"
            )
        self.marketplace = marketplace
        self._usage_log: List[Dict[str, Any]] = []
        logger.info(
            "[BillingAdapter] Initialised for marketplace=%s", self.marketplace,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def record_usage(
        self,
        tenant_id: str,
        service: str,
        tokens: int,
        decision: str,
    ) -> None:
        """
        Record a single metering event and dispatch to the vendor-specific
        handler.

        Parameters
        ----------
        tenant_id : str
            Customer / subscription identifier.
        service : str
            Cloud service being governed (e.g. ``"bedrock"``, ``"openai"``).
        tokens : int
            Estimated token count consumed.
        decision : str
            Governance decision: ``"ALLOW"``, ``"BLOCK"``, or ``"MODIFY"``.
        """
        record = {
            "tenant_id": tenant_id,
            "service": service,
            "tokens": tokens,
            "decision": decision,
            "marketplace": self.marketplace,
            "timestamp": time.time(),
        }
        self._usage_log.append(record)

        logger.info(
            "[BillingAdapter] Usage recorded – tenant=%s service=%s "
            "tokens=%d decision=%s marketplace=%s",
            tenant_id, service, tokens, decision, self.marketplace,
        )

        # Dispatch to vendor-specific stub
        dispatch = {
            "aws": self._record_aws,
            "azure": self._record_azure,
            "gcp": self._record_gcp,
        }
        handler = dispatch[self.marketplace]
        await handler(record)

    # ------------------------------------------------------------------
    # Vendor stubs (to be wired to real APIs in later steps)
    # ------------------------------------------------------------------

    async def _record_aws(self, record: Dict[str, Any]) -> None:
        """
        AWS Marketplace metering stub.

        In production this will call the AWS Marketplace Metering API
        (``meter_usage``) via ``httpx`` with SigV4-signed requests using
        ``AWS_MARKETPLACE_PRODUCT_CODE`` from config.
        """
        logger.debug(
            "[BillingAdapter:AWS] Would call MeterUsage – "
            "tenant=%s tokens=%d (stub, no-op)",
            record["tenant_id"], record["tokens"],
        )

    async def _record_azure(self, record: Dict[str, Any]) -> None:
        """
        Azure Marketplace metering stub.

        In production this will POST to the Azure Marketplace Metering API
        using ``AZURE_MARKETPLACE_ACCESS_TOKEN`` and ``AZURE_RESOURCE_ID``
        from config.
        """
        logger.debug(
            "[BillingAdapter:Azure] Would call UsageEvent API – "
            "tenant=%s tokens=%d (stub, no-op)",
            record["tenant_id"], record["tokens"],
        )

    async def _record_gcp(self, record: Dict[str, Any]) -> None:
        """
        GCP Marketplace metering stub.

        In production this will call the GCP Service Control API or
        Cloud Commerce Procurement API using
        ``GCP_MARKETPLACE_CREDENTIALS`` from config.
        """
        logger.debug(
            "[BillingAdapter:GCP] Would call ServiceControl.report – "
            "tenant=%s tokens=%d (stub, no-op)",
            record["tenant_id"], record["tokens"],
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_usage_log(self) -> List[Dict[str, Any]]:
        """Return a copy of all recorded usage events (for testing/audit)."""
        return list(self._usage_log)

    def clear_usage_log(self) -> None:
        """Clear the in-memory usage log."""
        self._usage_log.clear()
