# Phase 111 – GCP Cloud Run Module for Guardrail Cloud Connector
# Deploys the governance proxy as a fully managed Cloud Run service.

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

# ---------------------------------------------------------------------------
# Cloud Run Service
# ---------------------------------------------------------------------------

resource "google_cloud_run_v2_service" "connector" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.container_image

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = var.cpu
          memory = var.memory
        }
      }

      # Core settings
      env {
        name  = "CLOUD_PROVIDER"
        value = "gcp"
      }
      env {
        name  = "GUARDRAIL_API_URL"
        value = var.guardrail_api_url
      }
      env {
        name  = "GUARDRAIL_API_KEY"
        value = var.guardrail_api_key
      }
      env {
        name  = "PORT"
        value = "8000"
      }
      env {
        name  = "GCP_SERVICE_NAME"
        value = var.gcp_service_name
      }

      # Health check
      startup_probe {
        http_get {
          path = "/healthz"
          port = 8000
        }
        initial_delay_seconds = 3
        period_seconds        = 10
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/healthz"
          port = 8000
        }
        period_seconds = 15
      }
    }

    # Service account for marketplace metering
    service_account = var.service_account_email
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# ---------------------------------------------------------------------------
# IAM: Allow unauthenticated access (if the proxy is behind a mesh/VPC)
# ---------------------------------------------------------------------------

resource "google_cloud_run_v2_service_iam_member" "invoker" {
  count    = var.allow_unauthenticated ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.connector.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
