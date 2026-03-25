
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