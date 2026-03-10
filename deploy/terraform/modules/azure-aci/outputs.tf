# Outputs for Azure Container Instances module

output "container_group_id" {
  description = "ID of the ACI container group"
  value       = azurerm_container_group.connector.id
}

output "ip_address" {
  description = "IP address of the container group"
  value       = azurerm_container_group.connector.ip_address
}

output "fqdn" {
  description = "FQDN of the container group (if DNS is configured)"
  value       = azurerm_container_group.connector.fqdn
}
