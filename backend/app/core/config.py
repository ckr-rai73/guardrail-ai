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
    # AWS Marketplace
    # ------------------------------------------------------------------
    AWS_MARKETPLACE_PRODUCT_CODE: str = ""
    AWS_REGION: str = "us-east-1"

    # ------------------------------------------------------------------
    # Azure Marketplace
    # ------------------------------------------------------------------
    AZURE_MARKETPLACE_ACCESS_TOKEN: str = ""
    AZURE_RESOURCE_ID: str = ""

    # ------------------------------------------------------------------
    # GCP Marketplace
    # ------------------------------------------------------------------
    GCP_MARKETPLACE_CREDENTIALS: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton – import ``settings`` anywhere in the app.
settings = Settings()
