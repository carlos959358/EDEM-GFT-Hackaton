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

#Creamos la cuenta de servicio de cloud run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "hackatone-cloud-run-sa"
  display_name = "Service Account para ${var.service_name}"
}

resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloud_run_sa.email

    scaling {
      min_instance_count = 0 
      max_instance_count = 1
    }

    containers {
      image = var.container_image
      
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      
      ports {
        container_port = 8080
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
