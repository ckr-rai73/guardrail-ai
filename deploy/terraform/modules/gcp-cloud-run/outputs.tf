# Outputs for GCP Cloud Run module

output "service_url" {
  description = "URL of the Cloud Run service"
  value       = google_cloud_run_v2_service.connector.uri
}

output "service_name" {
  description = "Name of the Cloud Run service"
  value       = google_cloud_run_v2_service.connector.name
}

output "service_id" {
  description = "Full resource path of the service"
  value       = google_cloud_run_v2_service.connector.id
}
