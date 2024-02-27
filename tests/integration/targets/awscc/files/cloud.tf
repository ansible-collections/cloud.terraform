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

variable "vpc_id" {
  type    = string
}

variable "cidr_block" {
  type    = string
}

resource "awscc_ec2_subnet" "main" {
  vpc_id     = var.vpc_id
  cidr_block = var.cidr_block
}
