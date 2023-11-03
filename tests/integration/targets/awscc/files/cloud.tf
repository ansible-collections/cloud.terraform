terraform {
  required_providers {
    awscc = {
      source  = "hashicorp/awscc"
      version = "=0.63.0"
    }
  }
}

provider "awscc" {
}

variable "cloud_terraform_integration_id" {
  type    = string
  default = "jci93"
}

variable "cidr_block" {
  type    = string
  default = "10.1.2.0/24"
}

resource "awscc_ec2_vpc" "test_vpc" {
  cidr_block = var.cidr_block
  tags = [
    {
      key   = "Name",
      value = var.cloud_terraform_integration_id,
    },
    {
      key   = "cloud_terraform_integration",
      value = "true",
    },
  ]
}
