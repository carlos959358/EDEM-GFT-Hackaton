terraform {
  required_version = ">= 1.0"

  backend "gcs" {
    bucket      = "gft-hackaton-tfstate"
    prefix      = "terraform/state"
    credentials = "../spa-datajuniorsprogram-sdb-001-899009cc32ac.json"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}

