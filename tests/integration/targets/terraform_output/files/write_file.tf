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

resource "local_file" "foo" {
    content  = "This file was written by terraform!"
    filename = "${path.module}/terraform_test.txt"
}

output "my_output" {
  value = "file generated"
}
