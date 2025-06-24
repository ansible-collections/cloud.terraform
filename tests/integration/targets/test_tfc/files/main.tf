terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.10.0"
  cloud {
    organization = "Ansible-BU-TFC"
    hostname = "app.terraform.io"
    workspaces { 
      name = "my_tf_project_default"
    }
  }
}
provider "aws" {
  region     = "us-west-2"
  # In real scenarios, you would use environment variables or a credentials file for security.
  # Access key and secret key are necessary only for testing locally. In GH Pipelines, these will be set using CI Keys.
  access_key = "your_access_key"
  secret_key = "your_secret_key"
}

resource "aws_instance" "app_server_tf" {
  ami           = "ami-830c94e3"
  instance_type = "t2.micro"

  tags = {
    Name = "Instance_Cloud_TF"
  }
}

output "my_output" {
  value = resource.aws_instance.app_server_tf
}