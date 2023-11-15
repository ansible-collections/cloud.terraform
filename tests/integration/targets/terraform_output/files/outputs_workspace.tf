terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.2.3"
    }
  }
}

variable "workspace" {
  type = string
}

output "my_workspace" {
  value = "${var.workspace}"
}