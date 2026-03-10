# Variables for Azure Container Instances module

variable "container_group_name" {
  description = "Name of the ACI container group"
  type        = string
  default     = "guardrail-cloud-connector"
}

variable "resource_group_name" {
  description = "Azure resource group name"
  type        = string
}

variable "location" {
  description = "Azure region (e.g. eastus, westeurope)"
  type        = string
  default     = "eastus"
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

variable "azure_resource_id" {
  description = "Azure Marketplace resource ID for metered billing"
  type        = string
  default     = ""
}

variable "azure_access_token" {
  description = "Fallback static token for Azure Marketplace API"
  type        = string
  sensitive   = true
  default     = ""
}

variable "cpu" {
  description = "CPU cores for the container"
  type        = number
  default     = 0.5
}

variable "memory" {
  description = "Memory in GB for the container"
  type        = number
  default     = 0.5
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
