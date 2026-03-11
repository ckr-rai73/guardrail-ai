# File: app/core/config.py
"""
Phase 111 – Centralised Configuration
=======================================
Pydantic-based settings with environment variable overrides.
Cloud marketplace credentials are kept as empty defaults so the
application boots cleanly in dev/test without marketplace secrets.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application-wide configuration.

    All values can be overridden via environment variables or a ``.env``
    file (Pydantic will read it automatically when ``env_file`` is set).
    """

    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------
    APP_NAME: str = "Guardrail.ai"
    DEBUG: bool = False

    # ------------------------------------------------------------------
    # Guardrail Core API (connector sidecar → governance engine)
    # ------------------------------------------------------------------
    GUARDRAIL_API_URL: str = "http://guardrail-core:8080"
    GUARDRAIL_API_KEY: str = ""

    # ------------------------------------------------------------------
    # AWS Marketplace
    # ------------------------------------------------------------------
    AWS_MARKETPLACE_PRODUCT_CODE: str = ""
    AWS_REGION: str = "us-east-1"

    # ------------------------------------------------------------------
    # Azure Marketplace
    # ------------------------------------------------------------------
    AZURE_MARKETPLACE_ACCESS_TOKEN: str = ""   # fallback if DefaultAzureCredential unavailable
    AZURE_RESOURCE_ID: str = ""

    # ------------------------------------------------------------------
    # GCP Marketplace
    # ------------------------------------------------------------------
    GCP_MARKETPLACE_CREDENTIALS: str = ""      # deprecated, use GCP_SERVICE_ACCOUNT_JSON
    GCP_SERVICE_ACCOUNT_JSON: str = ""         # raw JSON string of service-account key
    GCP_SERVICE_NAME: str = ""                 # GCP Service Control API service name

    # ------------------------------------------------------------------
    # Red-Team as a Service (Phase 112)
    # ------------------------------------------------------------------
    REDTEAM_MAX_DRILL_DURATION: int = 3600           # seconds
    REDTEAM_MAX_CONCURRENT_DRILLS_PER_CLIENT: int = 2
    REDTEAM_REPORT_STORAGE_PATH: str = "/var/guardrail/redteam_reports"
    REDTEAM_SANDBOX_AGENT_PREFIX: str = "staging-"

    # ------------------------------------------------------------------
    # Quantum-Safe Cryptography (Phase 113)
    # ------------------------------------------------------------------
    PQC_DEFAULT_SIGNING_ALG: str = "ML-KEM-1024"
    PQC_DEFAULT_HASH_ALG: str = "SHA3-512"
    PQC_KEY_ROTATION_GRACE_DAYS: int = 90          # days before old key retired
    PQC_REANCHOR_BATCH_SIZE: int = 1000            # blocks per batch
    PQC_COMPLIANCE_CHECK_INTERVAL: int = 86400     # seconds (daily)

    # ------------------------------------------------------------------
    # Autonomous Compliance Certification (Phase 114)
    # ------------------------------------------------------------------
    COMPLIANCE_EVIDENCE_RETENTION_DAYS: int = 2555          # 7 years
    COMPLIANCE_CERTIFICATE_STORAGE_PATH: str = "/var/guardrail/certificates"
    COMPLIANCE_SUPPORTED_FRAMEWORKS: list = [
        "ISO_42001", "SOC2", "FedRAMP", "EU_AI_ACT", "NIST_AI_RMF",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton – import ``settings`` anywhere in the app.
settings = Settings()
