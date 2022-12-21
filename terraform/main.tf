terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.3.0"
    }
  }
  required_version = ">= 1.0.1"
}


variable "subId" {
  type    = string
  default = ""
  description = "Enter the subscription_id you receive per mail."
}
variable "clientId" {
  type    = string
  default = ""
  description = "Enter the client_id you receive per mail."
}

variable "tenantId" {
  type    = string
  default = ""
  description = "Enter the tenant_id you receive per mail."
}

variable "clientSecret" {
  type    = string
  default = ""
  description = "Enter the client_secret you receive per mail."
}

variable "resgrp" {
  type    = string
  default = "MyRG001"
  description = "Enter the resourcegroup you receive per mail."
}




# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

subscription_id =var.subId
tenant_id=var.tenantId
client_id = var.clientId
client_secret = var.clientSecret
}

locals {
  custom_message = var.custom_message 
}

output "message" {
  value = local.custom_message 
}

resource "azurerm_resource_group" "my_rg" {
  name     = var.resgrp
  location = "uksouth"
}
