terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.2.3"
    }
  }
}

output "my_output" {
  value = "file generated"
}
