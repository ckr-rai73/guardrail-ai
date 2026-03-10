# File: app/cloud/cloud_connector_base.py
"""
Phase 111 – Cloud Native Governance Plugins
============================================
Abstract base class that every cloud-specific connector (AWS, Azure, GCP)
must implement.  It owns the governance-assess → forward → bill lifecycle.

The ``RealGovernanceClient`` replaces the earlier stub facade and calls
the live Guardrail governance API over HTTP.
"""

from __future__ import annotations

import json
import logging
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger("guardrail.cloud")


# ---------------------------------------------------------------------------
# Governance types
# ---------------------------------------------------------------------------

@dataclass
class Decision:
    """Result of a governance assessment."""
    action: str          # "ALLOW", "BLOCK", or "MODIFY"
    reason: str = ""
    modifications: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Real Governance Client (replaces the Phase 111 Step 1 stub)
# ---------------------------------------------------------------------------

class RealGovernanceClient:
    """
    HTTP client that calls the live Guardrail governance API.

    The connector sidecars use this to communicate with the core Guardrail
    instance.  Each call hits::

        POST {base_url}/api/v1/governance/assess

    with the context dict as JSON.  The response is parsed into a
    ``Decision`` object.

    Parameters
    ----------
    base_url : str
        Root URL of the Guardrail API (e.g. ``http://guardrail-core:8080``).
    api_key : str
        Shared secret transmitted via the ``X-API-Key`` header.
    timeout : float
        HTTP request timeout in seconds (default 10).
    """

    ASSESS_PATH = "/api/v1/governance/assess"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=timeout)
        logger.info(
            "[GovernanceClient] Initialised – base_url=%s", self.base_url,
        )

    async def assess(self, context: dict) -> Decision:
        """
        Send a governance assessment request and return the ``Decision``.

        Raises
        ------
        GovernanceAPIError
            If the API returns a non-200 status, invalid JSON, or times out.
        """
        url = f"{self.base_url}{self.ASSESS_PATH}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        try:
            response = await self._client.post(
                url, json=context, headers=headers,
            )
        except httpx.TimeoutException as exc:
            raise GovernanceAPIError(
                f"Governance API timed out: {exc}"
            ) from exc
        except httpx.HTTPError as exc:
            raise GovernanceAPIError(
                f"Governance API request failed: {exc}"
            ) from exc

        if response.status_code != 200:
            raise GovernanceAPIError(
                f"Governance API returned {response.status_code}: "
                f"{response.text}"
            )

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise GovernanceAPIError(
                f"Governance API returned invalid JSON: {exc}"
            ) from exc

        decision = Decision(
            action=data.get("action", "BLOCK"),
            reason=data.get("reason", ""),
            modifications=data.get("modifications", {}),
        )

        logger.info(
            "[GovernanceClient] Decision received: %s – %s",
            decision.action, decision.reason,
        )
        return decision

    async def close(self) -> None:
        """Shut down the internal HTTP client."""
        await self._client.aclose()


class GovernanceAPIError(Exception):
    """Raised when the governance API call fails."""


# Backward-compatible alias: connectors import ``GovernanceGateway``
GovernanceGateway = RealGovernanceClient


# ---------------------------------------------------------------------------
# Forward-reference import for billing (avoids circular imports)
# ---------------------------------------------------------------------------
from app.cloud.billing_adapter import CloudBillingAdapter  # noqa: E402


# ---------------------------------------------------------------------------
# Abstract Cloud Connector
# ---------------------------------------------------------------------------

class CloudConnectorBase(ABC):
    """
    Abstract base for cloud-specific governance connectors.

    Lifecycle per request::

        extract_context  →  governance.assess  →  (modify?)  →  forward  →  bill

    Subclasses (``AWSConnector``, ``AzureConnector``, ``GCPConnector``)
    implement the three abstract methods to handle vendor-specific
    serialisation, authentication, and forwarding.

    Parameters
    ----------
    governance_gateway : RealGovernanceClient
        HTTP client pointing at the live Guardrail governance API.
    billing_adapter : CloudBillingAdapter
        Marketplace metering adapter.
    timeout : float
        Timeout for upstream cloud requests (default 30s).
    """

    def __init__(
        self,
        governance_gateway: RealGovernanceClient,
        billing_adapter: CloudBillingAdapter,
        *,
        timeout: float = 30.0,
    ) -> None:
        self.governance = governance_gateway
        self.billing = billing_adapter
        self.client = httpx.AsyncClient(timeout=timeout)
        logger.info(
            "[CloudConnector] Initialised – marketplace=%s",
            self.billing.marketplace,
        )

    # ------------------------------------------------------------------
    # Public entry-point
    # ------------------------------------------------------------------

    async def handle(
        self,
        method: str,
        url: str,
        body: bytes,
        headers: dict,
    ) -> httpx.Response:
        """
        Full governance lifecycle for a single cloud-API request.

        1. Extract vendor-specific context from the raw request.
        2. Run governance assessment (policy engine + shadow model).
        3. If BLOCK  → return 403 immediately.
        4. If MODIFY → mutate the request body before forwarding.
        5. Forward the (possibly modified) request to the cloud.
        6. Asynchronously record marketplace billing usage.
        7. Return the upstream cloud response.
        """
        # --- Step 1: Context extraction ---
        try:
            context = await self.extract_context(method, url, body, headers)
        except Exception:
            logger.error(
                "[CloudConnector] Context extraction failed:\n%s",
                traceback.format_exc(),
            )
            return self._error_response(
                status_code=500,
                detail="Internal error during context extraction",
            )

        # --- Step 2: Governance assessment ---
        try:
            decision = await self.governance.assess(context)
        except Exception:
            logger.error(
                "[CloudConnector] Governance assessment failed:\n%s",
                traceback.format_exc(),
            )
            return self._error_response(
                status_code=500,
                detail="Governance assessment unavailable – fail-secure",
            )

        logger.info(
            "[CloudConnector] Decision: %s – %s", decision.action, decision.reason,
        )

        # --- Step 3: BLOCK ---
        if decision.action == "BLOCK":
            return self._error_response(
                status_code=403,
                detail="Blocked by Guardrail policy",
                reason=decision.reason,
            )

        # --- Step 4: MODIFY ---
        request_body = body
        if decision.action == "MODIFY" and decision.modifications:
            try:
                request_body = await self.apply_modifications(
                    body, decision.modifications,
                )
            except Exception:
                logger.error(
                    "[CloudConnector] Modification application failed:\n%s",
                    traceback.format_exc(),
                )
                return self._error_response(
                    status_code=500,
                    detail="Failed to apply policy modifications",
                )

        # --- Step 5: Forward ---
        try:
            response = await self.forward_request(
                method=method,
                url=url,
                data=request_body,
                headers=headers,
            )
        except Exception:
            logger.error(
                "[CloudConnector] Forward request failed:\n%s",
                traceback.format_exc(),
            )
            return self._error_response(
                status_code=502,
                detail="Upstream cloud request failed",
            )

        # --- Step 6: Bill ---
        try:
            tenant_id = context.get("tenant_id", "unknown")
            service = context.get("service", "unknown")
            tokens = context.get("estimated_tokens", 0)
            await self.billing.record_usage(
                tenant_id=tenant_id,
                service=service,
                tokens=tokens,
                decision=decision.action,
            )
        except Exception:
            # Billing failures are non-fatal – log and continue.
            logger.warning(
                "[CloudConnector] Billing record failed (non-fatal):\n%s",
                traceback.format_exc(),
            )

        # --- Step 7: Return ---
        return response

    # ------------------------------------------------------------------
    # Abstract methods – implemented by each cloud connector
    # ------------------------------------------------------------------

    @abstractmethod
    async def extract_context(
        self,
        method: str,
        url: str,
        body: bytes,
        headers: dict,
    ) -> dict:
        """
        Parse vendor-specific request details into a normalised context
        dictionary suitable for ``RealGovernanceClient.assess()``.
        """
        ...

    @abstractmethod
    async def forward_request(
        self,
        method: str,
        url: str,
        data: bytes,
        headers: dict,
    ) -> httpx.Response:
        """
        Forward the (possibly modified) request to the real cloud endpoint
        using ``self.client``.
        """
        ...

    @abstractmethod
    async def apply_modifications(
        self,
        body: bytes,
        modifications: dict,
    ) -> bytes:
        """
        Apply governance-mandated modifications to the request body and
        return the updated payload as bytes.
        """
        ...

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _error_response(
        status_code: int,
        detail: str,
        reason: str = "",
    ) -> httpx.Response:
        """Build a synthetic ``httpx.Response`` for local error returns."""
        payload: Dict[str, Any] = {"error": detail}
        if reason:
            payload["reason"] = reason

        return httpx.Response(
            status_code=status_code,
            json=payload,
            headers={"content-type": "application/json"},
        )

    async def close(self) -> None:
        """Gracefully shut down the underlying HTTP client."""
        await self.client.aclose()
        logger.info("[CloudConnector] HTTP client closed.")
