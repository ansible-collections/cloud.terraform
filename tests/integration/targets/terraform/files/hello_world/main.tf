terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "2.2.3"
    }
  }
}

provider "local" {
  # Configuration options (I have none :_)
}

output "hello_world" {
  value = "Hello, World!"
}
