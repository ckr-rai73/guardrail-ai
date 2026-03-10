# File: app/cloud/cloud_connector_base.py
"""
Phase 111 – Cloud Native Governance Plugins
============================================
Abstract base class that every cloud-specific connector (AWS, Azure, GCP)
must implement.  It owns the governance-assess → forward → bill lifecycle.
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
# Minimal governance types (adaptable to the real GovernanceGateway later)
# ---------------------------------------------------------------------------

@dataclass
class Decision:
    """Result of a governance assessment."""
    action: str          # "ALLOW", "BLOCK", or "MODIFY"
    reason: str = ""
    modifications: Dict[str, Any] = field(default_factory=dict)


class GovernanceGateway:
    """
    Lightweight facade around the Phase-8 PolicyEngine and Phase-1 Veto
    Protocol.  Cloud connectors call ``assess()``; internally this fans
    out to policy evaluation, shadow-model verification, and constitution
    checks exactly as the existing orchestration layer does.

    NOTE: In production this delegates to
    ``app.orchestration.governance_gateway.GovernanceGatewayAPI`` and
    ``app.mcp.policy_engine.PolicyEngine``.  The thin wrapper exists so
    that cloud connectors never import heavy internal modules directly.
    """

    async def assess(self, context: dict) -> Decision:
        """
        Evaluate an incoming cloud-API request against Guardrail policies.

        Parameters
        ----------
        context : dict
            Must include at least ``method``, ``url``, ``service``, and
            optionally ``body``, ``headers``, ``tenant_id``.

        Returns
        -------
        Decision
            One of ALLOW / BLOCK / MODIFY with an explanation and optional
            modification payload.
        """
        # Phase 111 stub – always ALLOW until real wiring is done in Step 2.
        # In the real implementation this calls:
        #   PolicyEngine.evaluate(context)
        #   ShadowModel.verify(context)
        #   ConstitutionEngine.check(context)
        logger.info(
            "[GovernanceGateway] assess – service=%s method=%s url=%s",
            context.get("service", "unknown"),
            context.get("method", "?"),
            context.get("url", "?"),
        )
        return Decision(action="ALLOW", reason="Default permit (Phase 111 stub)")


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

    Subclasses (``AwsConnector``, ``AzureConnector``, ``GcpConnector``)
    implement the three abstract methods to handle vendor-specific
    serialisation, authentication, and forwarding.
    """

    def __init__(
        self,
        governance_gateway: GovernanceGateway,
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
        dictionary suitable for ``GovernanceGateway.assess()``.
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
