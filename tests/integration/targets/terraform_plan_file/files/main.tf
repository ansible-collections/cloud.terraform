terraform {
  required_providers {
    ansible = {
      source  = "ansible/ansible"
    }
  }
}

variable "new_group" {
    type = string
    description = "additional host group"
}

resource "ansible_host" "my_host" {
  name   = "localhost"
  groups = ["ansible", var.new_group]
  variables = {
    ansible_user  = "ansible"
    ansible_host  = "127.0.0.1"
  }
}

output "host_groups" {
  value = ansible_host.my_host.groups
}