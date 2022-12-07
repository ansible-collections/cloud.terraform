terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.2.3"
    }
  }
}

provider "local" {
  # Configuration options (I have none :_)
}

resource "local_sensitive_file" "sensitive_foo" {
  content  = "sensitive_content"
  filename = "${path.module}/not_sensitive_file_name.txt"
}

output "my_output" {
  value = var.my_output
}

variable "my_output" {
  type = string
}

output "my_another_output" {
  value = "not_sensitive_value"
}
