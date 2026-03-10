# File: app/cloud/connector_gcp.py
"""
Phase 111 – GCP Cloud Governance Connector
============================================
Concrete implementation of ``CloudConnectorBase`` for Google Cloud AI
services:

  • **Vertex AI** — predict, explain, generateContent, streamGenerateContent
  • **Cloud Vision API** — image annotation, object detection
  • **Cloud Natural Language API** — entity analysis, sentiment, classification
  • **Cloud Translation API** — text translation, language detection
  • **Cloud Speech-to-Text / Text-to-Speech** — transcription, synthesis

Authentication is passthrough: the connector preserves the caller's
``Authorization: Bearer …`` token.  Optional service-account signing
can be layered on in a future step via ``google-auth``.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

import httpx

from app.cloud.cloud_connector_base import CloudConnectorBase, GovernanceGateway
from app.cloud.billing_adapter import CloudBillingAdapter

logger = logging.getLogger("guardrail.cloud.gcp")


# ---------------------------------------------------------------------------
# Service-detection helpers
# ---------------------------------------------------------------------------

# Maps hostname suffixes / keywords → canonical GCP service names.
# Checked in order; first match wins.
_SERVICE_HOST_PATTERNS: List[Tuple[str, str]] = [
    ("aiplatform.googleapis.com",  "vertex-ai"),
    ("vision.googleapis.com",      "vision"),
    ("language.googleapis.com",    "language"),
    ("translate.googleapis.com",   "translate"),
    ("speech.googleapis.com",      "speech"),
    ("texttospeech.googleapis.com", "speech"),
]

# Vertex AI endpoint extraction:
#   /v1/projects/{project}/locations/{loc}/endpoints/{endpoint}:predict
#   /v1/projects/{project}/locations/{loc}/publishers/{pub}/models/{model}:generateContent
_VERTEX_ENDPOINT_RE = re.compile(
    r"/endpoints/(?P<endpoint>[^/:]+)", re.IGNORECASE,
)
_VERTEX_MODEL_RE = re.compile(
    r"/models/(?P<model>[^/:]+)", re.IGNORECASE,
)
_VERTEX_PUBLISHER_MODEL_RE = re.compile(
    r"/publishers/(?P<publisher>[^/]+)/models/(?P<model>[^/:]+)", re.IGNORECASE,
)

# Vision API operation extraction:
#   /v1/images:annotate  →  "annotate"
#   /v1/files:asyncBatchAnnotate  →  "asyncBatchAnnotate"
_VISION_OPERATION_RE = re.compile(
    r"/(?:images|files):(?P<operation>[a-zA-Z]+)", re.IGNORECASE,
)

# Language API operation extraction:
#   /v1/documents:analyzeSentiment  →  "analyzeSentiment"
#   /v2/documents:analyzeEntities   →  "analyzeEntities"
_LANGUAGE_OPERATION_RE = re.compile(
    r"/documents:(?P<operation>[a-zA-Z]+)", re.IGNORECASE,
)

# Translate API operation extraction:
#   /v3/projects/{project}/locations/{loc}:translateText  →  "translateText"
#   /v2/detect  →  "detect"
_TRANSLATE_OPERATION_RE = re.compile(
    r":(?P<operation>translateText|detectLanguage|batchTranslateText)",
    re.IGNORECASE,
)
_TRANSLATE_V2_OPERATION_RE = re.compile(
    r"/(?P<operation>detect|translate|languages)$", re.IGNORECASE,
)

# Speech API operation extraction:
#   /v1/speech:recognize  →  "recognize"
#   /v1/text:synthesize   →  "synthesize"
_SPEECH_OPERATION_RE = re.compile(
    r"/(?:speech|text):(?P<operation>[a-zA-Z]+)", re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# GCP Connector
# ---------------------------------------------------------------------------

class GCPConnector(CloudConnectorBase):
    """
    Governance-aware proxy for Google Cloud AI services.

    For every inbound request the connector:

    1. **Extracts** the target GCP service and model / endpoint / operation.
    2. **Assesses** the request through the ``GovernanceGateway``.
    3. **Forwards** it to the real GCP endpoint (auth passthrough).
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
        logger.info("[GCPConnector] Initialised (auth passthrough mode)")

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
        Build a normalised governance context from a GCP-bound request.

        Extracts:
          - **service** from the ``Host`` header.
          - **model** / endpoint / operation from the URL path.
          - **tenant_id** from ``X-Guardrail-Tenant`` header.
          - **user** from ``X-Forwarded-User`` header.
          - **estimated_tokens** as ``len(body) // 4``.

        Raises
        ------
        ValueError
            If the host header does not match any known GCP AI service.
        """
        host = headers.get("host", headers.get("Host", ""))
        service = self._detect_service(host)

        if service == "unknown":
            raise ValueError(
                f"Unrecognised GCP AI host: '{host}' – "
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
            "agent":            "gcp-connector",
            "service":          service,
            "model":            model,
            "method":           method,
            "url":              url,
            "payload":          payload_str,
            "estimated_tokens": estimated_tokens,
        }

        logger.info(
            "[GCPConnector] Context extracted – service=%s model=%s "
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
        Forward the request to GCP with headers passed through unchanged.

        GCP services authenticate via ``Authorization: Bearer …`` or
        API key query parameter — both are preserved as-is.
        """
        # Normalise data to bytes
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            data = data.encode("utf-8")

        logger.info(
            "[GCPConnector] Forwarding %s %s (%d bytes)",
            method.upper(), url, len(data) if data else 0,
        )

        response = await self.client.request(
            method=method.upper(),
            url=url,
            content=data,
            headers=headers,
        )

        logger.info(
            "[GCPConnector] Upstream response: %d (%d bytes)",
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
                "[GCPConnector] Body is not valid JSON – "
                "skipping modifications: %s", exc,
            )
            return body

        redact_fields = modifications.get("redact_fields", [])
        redacted_count = 0
        for field_name in redact_fields:
            if field_name in payload:
                logger.info(
                    "[GCPConnector] Redacting field '%s'", field_name,
                )
                payload[field_name] = "[REDACTED]"
                redacted_count += 1

        modified = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        logger.info(
            "[GCPConnector] Body modified – %d/%d fields redacted, "
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
        Map a GCP hostname to a canonical service name.

        Examples::

            us-central1-aiplatform.googleapis.com  →  vertex-ai
            vision.googleapis.com                  →  vision
            language.googleapis.com                →  language
            translate.googleapis.com               →  translate
            speech.googleapis.com                  →  speech
        """
        host_lower = host.lower()
        for pattern, svc in _SERVICE_HOST_PATTERNS:
            if host_lower.endswith(pattern) or pattern in host_lower:
                return svc
        return "unknown"

    @staticmethod
    def _extract_model(service: str, url: str, body: bytes) -> str:
        """
        Extract the model / endpoint / operation identifier.

        - **Vertex AI**: endpoint ID or publisher/model from URL path.
        - **Vision**: operation name (e.g. ``annotate``).
        - **Language**: operation name (e.g. ``analyzeSentiment``).
        - **Translate**: operation name (e.g. ``translateText``).
        - **Speech**: operation name (e.g. ``recognize``, ``synthesize``).
        """
        parsed_path = urlparse(url).path

        # --- Vertex AI ---
        if service == "vertex-ai":
            # Check for publisher/model pattern first (Gemini, PaLM, etc.)
            match = _VERTEX_PUBLISHER_MODEL_RE.search(parsed_path)
            if match:
                return f"{match.group('publisher')}/{match.group('model')}"
            # Then check for endpoint ID
            match = _VERTEX_ENDPOINT_RE.search(parsed_path)
            if match:
                return match.group("endpoint")
            # Then check for a generic model reference
            match = _VERTEX_MODEL_RE.search(parsed_path)
            if match:
                return match.group("model")
            # Fall back to body inspection
            try:
                payload = json.loads(body)
                model = payload.get("model", "")
                if model:
                    return model
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            return "unknown"

        # --- Vision ---
        if service == "vision":
            match = _VISION_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")

        # --- Language ---
        if service == "language":
            match = _LANGUAGE_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")

        # --- Translate ---
        if service == "translate":
            match = _TRANSLATE_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")
            match = _TRANSLATE_V2_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")

        # --- Speech ---
        if service == "speech":
            match = _SPEECH_OPERATION_RE.search(parsed_path)
            if match:
                return match.group("operation")

        return "default"
