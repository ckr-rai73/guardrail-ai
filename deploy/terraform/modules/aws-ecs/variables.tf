# Variables for AWS ECS Fargate module

variable "cluster_name" {
  description = "Name for the ECS cluster"
  type        = string
  default     = "guardrail-cloud-connector"
}

variable "container_image" {
  description = "Docker image for the connector (e.g. guardrail/cloud-connector:latest)"
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

variable "aws_region" {
  description = "AWS region for the deployment and marketplace metering"
  type        = string
  default     = "us-east-1"
}

variable "aws_marketplace_product_code" {
  description = "AWS Marketplace product code for metering"
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "List of VPC subnet IDs for the Fargate tasks"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security group IDs for the Fargate tasks"
  type        = list(string)
}

variable "cpu" {
  description = "Fargate task CPU units (256, 512, 1024, 2048, 4096)"
  type        = string
  default     = "256"
}

variable "memory" {
  description = "Fargate task memory in MiB (512, 1024, 2048, …)"
  type        = string
  default     = "512"
}

variable "desired_count" {
  description = "Number of Fargate task instances"
  type        = number
  default     = 2
}
