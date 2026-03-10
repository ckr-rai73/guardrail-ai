# Variables for GCP Cloud Run module

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region (e.g. us-central1)"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "guardrail-cloud-connector"
}

variable "container_image" {
  description = "Docker image for the connector"
  type        = string
  default     = "guardrail/cloud-connector:latest"
}

variable "guardrail_api_url" {
  description = "URL of the Guardrail Core governance API"
  type        = string
}

variable "guardrail_api_key" {
  description = "API key for the Guardrail Core API"
  type        = string
  sensitive   = true
  default     = ""
}

variable "gcp_service_name" {
  description = "GCP Service Control API service name for metering"
  type        = string
  default     = ""
}

variable "service_account_email" {
  description = "Service account email for the Cloud Run service"
  type        = string
  default     = ""
}

variable "cpu" {
  description = "CPU limit (e.g. '1', '2')"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory limit (e.g. '512Mi', '1Gi')"
  type        = string
  default     = "512Mi"
}

variable "min_instances" {
  description = "Minimum number of instances (0 for scale-to-zero)"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
}

variable "allow_unauthenticated" {
  description = "Allow unauthenticated invocations (set true if behind VPC)"
  type        = bool
  default     = false
}
