output "resource_group_name" {
  description = "Name of the Azure resource group"
  value       = azurerm_resource_group.main.name
}

output "vm_name" {
  description = "Name of the Linux virtual machine"
  value       = azurerm_linux_virtual_machine.main.name
}

output "public_ip_address" {
  description = "Public IP address of the Linux virtual machine"
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "Command used to connect to the Linux virtual machine"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}