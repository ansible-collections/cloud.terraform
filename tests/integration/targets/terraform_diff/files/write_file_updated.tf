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
  content  = "new_sensitive_content"
  filename = sensitive("${path.module}/new_sensitive_file_name.txt")
}

output "my_output" {
  value = var.my_output
  sensitive = true
}

variable "my_output" {
  type = string
}

output "my_another_output" {
  value = "sensitive_value"
  sensitive = true
}
