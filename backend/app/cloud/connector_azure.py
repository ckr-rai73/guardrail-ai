# File: app/cloud/connector_azure.py
"""
Phase 111 – Azure Cloud Governance Connector
===============================================
Concrete implementation of ``CloudConnectorBase`` for Azure AI services:

  • **Azure OpenAI Service** — chat completions, completions, embeddings
  • **Azure Machine Learning** — real-time managed endpoint inference
  • **Azure Cognitive Services** — Language, Vision, Speech, etc.

Authentication is passthrough: the connector preserves whichever auth
mechanism the caller already has (``api-key`` header or ``Authorization:
Bearer …``).  No Azure-specific credential management is required.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict
from urllib.parse import urlparse

import httpx

from app.cloud.cloud_connector_base import CloudConnectorBase, GovernanceGateway
from app.cloud.billing_adapter import CloudBillingAdapter

logger = logging.getLogger("guardrail.cloud.azure")


# ---------------------------------------------------------------------------
# Service-detection helpers
# ---------------------------------------------------------------------------

# Maps hostname suffixes / keywords → canonical Azure service names.
# Checked in order; first match wins.
_SERVICE_HOST_PATTERNS = [
    ("openai.azure.com",            "openai"),
    (".inference.ml.azure.com",     "azureml"),
    (".azureml.ms",                 "azureml"),
    (".api.cognitive.microsoft.com", "cognitive"),
    (".cognitiveservices.azure.com", "cognitive"),
]

# Azure OpenAI deployment extraction:
#   /openai/deployments/{deployment-name}/chat/completions?api-version=…
_OPENAI_DEPLOYMENT_RE = re.compile(
    r"/openai/deployments/(?P<deployment>[^/]+)/", re.IGNORECASE,
)

# Cognitive Services operation extraction:
#   /text/analytics/v3.1/sentiment
#   /language/:analyze-text?api-version=…
#   /vision/v3.2/analyze
_COGNITIVE_OPERATION_RE = re.compile(
    r"/(?:text/analytics|language|vision|speech)/(?:v[\d.]+/)?(?::?)(?P<operation>[a-zA-Z_-]+)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Azure Connector
# ---------------------------------------------------------------------------

class AzureConnector(CloudConnectorBase):
    """
    Governance-aware proxy for Azure AI services.

    For every inbound request the connector:

    1. **Extracts** the target Azure service and deployment / model.
    2. **Assesses** the request through the ``GovernanceGateway``.
    3. **Forwards** it to the real Azure endpoint (auth passthrough).
    4. **Records** usage via the ``CloudBillingAdapter``.
    """

    def __init__(
        self,
        governance_gateway: GovernanceGateway,
        billing_adapter: CloudBillingAdapter,
        *,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(
            governance_gateway=governance_gateway,
            billing_adapter=billing_adapter,
            timeout=timeout,
        )
        logger.info("[AzureConnector] Initialised (auth passthrough mode)")

    # ------------------------------------------------------------------
    # Abstract-method implementations
    # ------------------------------------------------------------------

    async def extract_context(
        self,
        method: str,
        url: str,
        body: bytes,
        headers: dict,
    ) -> dict:
        """
        Build a normalised governance context from an Azure-bound request.

        Extracts:
          - **service** from the ``Host`` header.
          - **model** / deployment from the URL path or JSON body.
          - **tenant_id** from ``X-Guardrail-Tenant`` header.
          - **user** from ``X-Forwarded-User`` header.
          - **estimated_tokens** as ``len(body) // 4``.

        Raises
        ------
        ValueError
            If the host header does not match any known Azure AI service.
        """
        host = headers.get("host", headers.get("Host", ""))
        service = self._detect_service(host)

        if service == "unknown":
            raise ValueError(
                f"Unrecognised Azure AI host: '{host}' – "
                "cannot determine service for governance assessment"
            )

        model = self._extract_model(service, url, body)

        tenant_id = headers.get(
            "x-guardrail-tenant",
            headers.get("X-Guardrail-Tenant", "default"),
        )
        user = headers.get(
            "x-forwarded-user",
            headers.get("X-Forwarded-User", "unknown"),
        )

        estimated_tokens = len(body) // 4 if body else 0
        payload_str = body.decode("utf-8", errors="ignore") if body else ""

        context = {
            "tenant_id":        tenant_id,
            "user":             user,
            "agent":            "azure-connector",
            "service":          service,
            "model":            model,
            "method":           method,
            "url":              url,
            "payload":          payload_str,
            "estimated_tokens": estimated_tokens,
        }

        logger.info(
            "[AzureConnector] Context extracted – service=%s model=%s "
            "tenant=%s tokens≈%d",
            service, model, tenant_id, estimated_tokens,
        )
        return context

    async def forward_request(
        self,
        method: str,
        url: str,
        data: bytes,
        headers: dict,
    ) -> httpx.Response:
        """
        Forward the request to Azure with headers passed through unchanged.

        Azure services authenticate via ``api-key`` header or
        ``Authorization: Bearer …`` — both are preserved as-is.
        """
        # Normalise data to bytes
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            data = data.encode("utf-8")

        logger.info(
            "[AzureConnector] Forwarding %s %s (%d bytes)",
            method.upper(), url, len(data) if data else 0,
        )

        response = await self.client.request(
            method=method.upper(),
            url=url,
            content=data,
            headers=headers,
        )

        logger.info(
            "[AzureConnector] Upstream response: %d (%d bytes)",
            response.status_code, len(response.content),
        )
        return response

    async def apply_modifications(
        self,
        body: bytes,
        modifications: dict,
    ) -> bytes:
        """
        Apply governance-required modifications to the request body.

        Supports ``redact_fields``: a list of top-level JSON keys whose
        values will be replaced with ``"[REDACTED]"``.

        If the body is not valid JSON the original bytes are returned
        unchanged (with a warning logged).
        """
        try:
            payload = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning(
                "[AzureConnector] Body is not valid JSON – "
                "skipping modifications: %s", exc,
            )
            return body

        redact_fields = modifications.get("redact_fields", [])
        redacted_count = 0
        for field_name in redact_fields:
            if field_name in payload:
                logger.info(
                    "[AzureConnector] Redacting field '%s'", field_name,
                )
                payload[field_name] = "[REDACTED]"
                redacted_count += 1

        modified = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        logger.info(
            "[AzureConnector] Body modified – %d/%d fields redacted, "
            "new size=%d bytes",
            redacted_count, len(redact_fields), len(modified),
        )
        return modified

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_service(host: str) -> str:
        """
        Map an Azure hostname to a canonical service name.

        Examples::

            my-resource.openai.azure.com             →  openai
            my-endpoint.westus2.inference.ml.azure.com →  azureml
            my-resource.api.cognitive.microsoft.com   →  cognitive
        """
        host_lower = host.lower()
        for pattern, svc in _SERVICE_HOST_PATTERNS:
            if host_lower.endswith(pattern) or pattern in host_lower:
                return svc
        return "unknown"

    @staticmethod
    def _extract_model(service: str, url: str, body: bytes) -> str:
        """
        Extract the deployment / model / operation identifier.

        - **Azure OpenAI**: deployment name from URL path.
        - **Azure ML**: ``model`` field from JSON body, else ``"unknown"``.
        - **Cognitive Services**: operation name from URL path.
        """
        parsed_path = urlparse(url).path

        # --- Azure OpenAI ---
        if service == "openai":
            match = _OPENAI_DEPLOYMENT_RE.search(parsed_path)
            if match:
                return match.group("deployment")

        # --- Azure ML ---
        if service == "azureml":
            # Try to get model name from JSON body
            try:
                payload = json.loads(body)
                model = payload.get("model", "")
                if model:
                    return model
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            return "unknown"

        # --- Cognitive Services ---
        if service == "cognitive":
            match = _COGNITIVE_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")

        return "default"
