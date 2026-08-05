variable "subscription_id" {
  description = "Azure subscription ID used for deployment"
  type        = string
  sensitive   = true
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "Sweden Central"
}

variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "rg-system-status-dashboard"
}

variable "project_name" {
  description = "Short name used when naming Azure resources"
  type        = string
  default     = "system-status"
}

variable "vm_name" {
  description = "Name of the Azure Linux virtual machine"
  type        = string
  default     = "system-status-vm"
}

variable "admin_username" {
  description = "Admin username used to SSH into the virtual machine"
  type        = string
  default     = "azureuser"
}