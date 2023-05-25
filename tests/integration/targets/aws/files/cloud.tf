terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "=4.38.0"
    }
  }
}

provider "aws" {
}

variable "cloud_terraform_integration_id" {
  type = string
}

variable "cidr_block" {
  type = string
}

resource "aws_vpc" "test_vpc" {
  cidr_block = var.cidr_block
  tags       = {
    Name                           = var.cloud_terraform_integration_id
    cloud_terraform_integration    = "true"
  }
}
