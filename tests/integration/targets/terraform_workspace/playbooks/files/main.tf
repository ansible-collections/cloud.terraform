terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
    }
  }
}

resource "local_file" "foo" {
  content  = "This file has been generated using Terraform on Ansible."
  filename = "${path.module}/foo.txt"
}
