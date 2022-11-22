terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "=4.43.0"
    }
  }
}

# the provider can't function with an implicit project from application-default credentials
variable "cloud_terraform_integration_project" {
  type = string
}

provider "google" {
  project = var.cloud_terraform_integration_project
}

variable "cloud_terraform_integration_id" {
  type = string
}

resource "google_compute_network" "test_vpc" {
  name = var.cloud_terraform_integration_id
}
