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

resource "aws_vpc" "test_vpc" {
  cidr_block = "10.11.12.0/24"
  tags       = {
    Name                           = "cloud.terraform integration VPC"
    cloud_terraform_integration    = "true"
    cloud_terraform_integration_id = var.cloud_terraform_integration_id
  }
}
