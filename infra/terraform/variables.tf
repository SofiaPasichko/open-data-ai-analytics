variable "resource_group_name" {
  description = "Name of the resource group"
  default     = "sofia-lab4-rg"
}

variable "location" {
  description = "Azure region"
  default     = "East US"
}

variable "vm_size" {
  description = "Size of the virtual machine"
  default     = "Standard_B1s"
}
