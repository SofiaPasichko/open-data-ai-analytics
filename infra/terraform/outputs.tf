output "public_ip_address" {
  description = "The public IP address of the newly created VM"
  value       = azurerm_public_ip.pip.ip_address
}
