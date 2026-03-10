# Phase 111 – Azure Container Instances Module for Guardrail Cloud Connector
# Deploys the governance proxy as an ACI container group.

terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.80"
    }
  }
}

provider "azurerm" {
  features {}
}

# ---------------------------------------------------------------------------
# Container Group
# ---------------------------------------------------------------------------

resource "azurerm_container_group" "connector" {
  name                = var.container_group_name
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  restart_policy      = "Always"

  container {
    name   = "connector"
    image  = var.container_image
    cpu    = var.cpu
    memory = var.memory

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      CLOUD_PROVIDER   = "azure"
      GUARDRAIL_API_URL = var.guardrail_api_url
      PORT             = "8000"
      AZURE_RESOURCE_ID = var.azure_resource_id
      GCP_SERVICE_NAME  = ""
    }

    secure_environment_variables = {
      GUARDRAIL_API_KEY              = var.guardrail_api_key
      AZURE_MARKETPLACE_ACCESS_TOKEN = var.azure_access_token
    }

    liveness_probe {
      http_get {
        path   = "/healthz"
        port   = 8000
        scheme = "Http"
      }
      initial_delay_seconds = 5
      period_seconds        = 15
    }

    readiness_probe {
      http_get {
        path   = "/healthz"
        port   = 8000
        scheme = "Http"
      }
      initial_delay_seconds = 3
      period_seconds        = 10
    }
  }

  tags = var.tags
}
