terraform {
  required_providers {
    ansible = {
      version = ">=1.0"
      source  = "ansible/ansible"
    }
  }
}

resource "ansible_host" "host" {
  name   = "somehost"
  groups = ["somegroup", "anothergroup"]
  variables = {
    host_hello    = "from host!"
    host_variable = 7
  }
}

resource "ansible_host" "anotherhost" {
  name   = "anotherhost"
  groups = ["somechild"]
  variables = {
    host_hello    = "from anotherhost!"
    host_variable = 5
  }
}

resource "ansible_host" "ungrupedhost" {
  name = "ungrupedhost"
}

resource "ansible_group" "group" {
  name     = "somegroup"
  children = ["somechild", "anotherchild"]
  variables = {
    group_hello    = "from group!",
    group_variable = 11
  }
}

resource "ansible_group" "childlessgroup" {
  name = "childlessgroup"
}

module "example" {
  source = "./modules/example"

  name = "childhost"
}

module "nested_module" {
  source = "./modules/nested_module"

  name = "nested_module"
}
