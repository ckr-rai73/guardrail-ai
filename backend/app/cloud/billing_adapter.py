# File: app/cloud/billing_adapter.py
"""
Phase 111 – Cloud Billing Adapter (Real Marketplace Metering)
================================================================
Unified metering interface for AWS Marketplace, Azure Marketplace, and
GCP Marketplace.  Each ``record_usage`` call dispatches to a vendor-
specific handler that makes real HTTP calls to the marketplace metering
API.  Failures are **non-fatal**: they are logged but never propagate
to the caller, so a billing glitch cannot block a governance decision.

Vendor implementations:
  • **AWS**   – Metering API via SigV4-signed POST to
                ``metering.marketplace.{region}.amazonaws.com``
  • **Azure** – Metered billing via Bearer-token POST to
                ``marketplaceapi.microsoft.com``
  • **GCP**   – Service Control API via Bearer-token POST to
                ``servicecontrol.googleapis.com``
"""

from __future__ import annotations

import json
import logging
import time
import traceback
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

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
        self._http_client: Optional[httpx.AsyncClient] = None

        # Lazy-loaded credentials (vendor-specific)
        self._aws_credentials = None
        self._azure_credential = None
        self._gcp_credentials = None

        logger.info(
            "[BillingAdapter] Initialised for marketplace=%s", self.marketplace,
        )

    # ------------------------------------------------------------------
    # HTTP client (lazy init)
    # ------------------------------------------------------------------

    def _get_http_client(self) -> httpx.AsyncClient:
        """Return (and lazily create) the shared async HTTP client."""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=15.0)
        return self._http_client

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
        handler.  Exceptions are caught and logged — never raised.
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

        dispatch = {
            "aws": self._record_aws,
            "azure": self._record_azure,
            "gcp": self._record_gcp,
        }
        handler = dispatch[self.marketplace]

        try:
            await handler(record)
        except Exception:
            # Non-fatal: billing errors must never block the request.
            logger.error(
                "[BillingAdapter] Marketplace metering call failed "
                "(non-fatal):\n%s", traceback.format_exc(),
            )

    # ------------------------------------------------------------------
    # AWS Marketplace Metering
    # ------------------------------------------------------------------

    def _get_aws_credentials(self):
        """Lazy-load AWS credentials from default credential chain."""
        if self._aws_credentials is None:
            import boto3
            session = boto3.Session()
            creds = session.get_credentials()
            if creds:
                self._aws_credentials = creds.get_frozen_credentials()
        return self._aws_credentials

    async def _record_aws(self, record: Dict[str, Any]) -> None:
        """
        Call the AWS Marketplace Metering API (MeterUsage).

        Signs the request with SigV4 using credentials from the default
        boto3 credential chain.  Requires ``AWS_MARKETPLACE_PRODUCT_CODE``
        and ``AWS_REGION`` to be set in config.
        """
        from app.core.config import settings

        product_code = settings.AWS_MARKETPLACE_PRODUCT_CODE
        region = settings.AWS_REGION

        if not product_code:
            logger.debug(
                "[BillingAdapter:AWS] AWS_MARKETPLACE_PRODUCT_CODE not set "
                "– skipping metering"
            )
            return

        import botocore.auth
        import botocore.awsrequest

        credentials = self._get_aws_credentials()
        if not credentials:
            logger.warning("[BillingAdapter:AWS] No AWS credentials available")
            return

        # Build the MeterUsage payload
        now = datetime.now(timezone.utc)
        usage_quantity = max(1, record["tokens"] // 1000)
        payload = {
            "ProductCode": product_code,
            "Timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "UsageDimension": f"guardrail-{record['service']}",
            "UsageQuantity": usage_quantity,
            "DryRun": False,
        }

        url = (
            f"https://metering.marketplace.{region}.amazonaws.com"
        )

        # Create and sign the request
        aws_request = botocore.awsrequest.AWSRequest(
            method="POST",
            url=url,
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/x-amz-json-1.1",
                "X-Amz-Target": "AWSMPMeteringService.MeterUsage",
            },
        )
        signer = botocore.auth.SigV4Auth(
            credentials, "aws-marketplace", region,
        )
        signer.add_auth(aws_request)

        # Forward via httpx
        client = self._get_http_client()
        response = await client.post(
            url,
            content=json.dumps(payload).encode(),
            headers=dict(aws_request.headers),
        )

        if response.status_code == 200:
            logger.info(
                "[BillingAdapter:AWS] MeterUsage success – "
                "product=%s dimension=guardrail-%s qty=%d",
                product_code, record["service"], usage_quantity,
            )
        else:
            logger.warning(
                "[BillingAdapter:AWS] MeterUsage returned %d: %s",
                response.status_code, response.text[:500],
            )

    # ------------------------------------------------------------------
    # Azure Marketplace Metered Billing
    # ------------------------------------------------------------------

    async def _get_azure_token(self) -> str:
        """
        Obtain a Bearer token for the Azure Marketplace API.

        Tries ``azure.identity.DefaultAzureCredential`` first; falls back
        to ``AZURE_MARKETPLACE_ACCESS_TOKEN`` from config.
        """
        # Try DefaultAzureCredential
        try:
            from azure.identity import DefaultAzureCredential
            if self._azure_credential is None:
                self._azure_credential = DefaultAzureCredential()
            token = self._azure_credential.get_token(
                "https://marketplaceapi.microsoft.com/.default"
            )
            return token.token
        except Exception:
            pass

        # Fallback to static token from config
        from app.core.config import settings
        if settings.AZURE_MARKETPLACE_ACCESS_TOKEN:
            return settings.AZURE_MARKETPLACE_ACCESS_TOKEN

        raise RuntimeError(
            "No Azure credentials available: DefaultAzureCredential "
            "failed and AZURE_MARKETPLACE_ACCESS_TOKEN is empty"
        )

    async def _record_azure(self, record: Dict[str, Any]) -> None:
        """
        Call the Azure Marketplace Metered Billing API (UsageEvent).

        Requires ``AZURE_RESOURCE_ID`` in config and either
        ``DefaultAzureCredential`` environment or a static
        ``AZURE_MARKETPLACE_ACCESS_TOKEN``.
        """
        from app.core.config import settings

        resource_id = settings.AZURE_RESOURCE_ID
        if not resource_id:
            logger.debug(
                "[BillingAdapter:Azure] AZURE_RESOURCE_ID not set "
                "– skipping metering"
            )
            return

        token = await self._get_azure_token()
        now = datetime.now(timezone.utc)
        usage_quantity = max(1, record["tokens"] // 1000)

        payload = {
            "resourceId": resource_id,
            "quantity": usage_quantity,
            "dimension": f"guardrail-{record['service']}",
            "effectiveStartTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "planId": "guardrail-governance",
        }

        url = (
            "https://marketplaceapi.microsoft.com"
            "/api/usageEvent?api-version=2018-08-31"
        )

        client = self._get_http_client()
        response = await client.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code in (200, 201):
            logger.info(
                "[BillingAdapter:Azure] UsageEvent success – "
                "resource=%s dimension=guardrail-%s qty=%d",
                resource_id[:20], record["service"], usage_quantity,
            )
        else:
            logger.warning(
                "[BillingAdapter:Azure] UsageEvent returned %d: %s",
                response.status_code, response.text[:500],
            )

    # ------------------------------------------------------------------
    # GCP Service Control (Marketplace Metering)
    # ------------------------------------------------------------------

    async def _get_gcp_token(self) -> str:
        """
        Obtain a Bearer token for the GCP Service Control API.

        Tries service-account JSON from config first, then falls back to
        Application Default Credentials (ADC).
        """
        import google.auth
        import google.auth.transport.requests

        SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

        # Try service-account JSON from config
        from app.core.config import settings
        if settings.GCP_SERVICE_ACCOUNT_JSON:
            from google.oauth2 import service_account
            info = json.loads(settings.GCP_SERVICE_ACCOUNT_JSON)
            creds = service_account.Credentials.from_service_account_info(
                info, scopes=SCOPES,
            )
            creds.refresh(google.auth.transport.requests.Request())
            return creds.token

        # Fallback to ADC
        if self._gcp_credentials is None:
            self._gcp_credentials, _ = google.auth.default(scopes=SCOPES)
        self._gcp_credentials.refresh(
            google.auth.transport.requests.Request()
        )
        return self._gcp_credentials.token

    async def _record_gcp(self, record: Dict[str, Any]) -> None:
        """
        Call the GCP Service Control API to report marketplace usage.

        Requires ``GCP_SERVICE_NAME`` in config and either
        ``GCP_SERVICE_ACCOUNT_JSON`` or Application Default Credentials.
        """
        from app.core.config import settings

        service_name = settings.GCP_SERVICE_NAME
        if not service_name:
            logger.debug(
                "[BillingAdapter:GCP] GCP_SERVICE_NAME not set "
                "– skipping metering"
            )
            return

        token = await self._get_gcp_token()
        now = datetime.now(timezone.utc)
        iso_now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        usage_quantity = max(1, record["tokens"] // 1000)
        operation_id = str(uuid.uuid4())

        payload = {
            "operations": [
                {
                    "operationId": operation_id,
                    "operationName": "guardrail-usage",
                    "consumerId": f"project_number:{record['tenant_id']}",
                    "startTime": iso_now,
                    "endTime": iso_now,
                    "metricValueSets": [
                        {
                            "metricName": f"{service_name}/guardrail_tokens",
                            "metricValues": [
                                {"int64Value": str(usage_quantity)},
                            ],
                        },
                    ],
                    "labels": {
                        "guardrail/service": record["service"],
                        "guardrail/decision": record["decision"],
                    },
                },
            ],
        }

        url = (
            f"https://servicecontrol.googleapis.com"
            f"/v1/services/{service_name}:report"
        )

        client = self._get_http_client()
        response = await client.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code == 200:
            logger.info(
                "[BillingAdapter:GCP] ServiceControl.report success – "
                "service=%s op=%s qty=%d",
                service_name, operation_id[:8], usage_quantity,
            )
        else:
            logger.warning(
                "[BillingAdapter:GCP] ServiceControl.report returned %d: %s",
                response.status_code, response.text[:500],
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

    async def close(self) -> None:
        """Shut down the HTTP client."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
