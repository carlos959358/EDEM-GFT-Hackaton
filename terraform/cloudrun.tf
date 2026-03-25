resource "google_service_account" "cloud_run_sa" {
  account_id   = "hackatonesa"
  display_name = "Service Account para Cloud Run"
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "edem-gft-hackaton"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.cloud_run_sa.email

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.docker.repository_id}/frontend:latest"

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

  depends_on = [google_artifact_registry_repository.docker]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  name     = google_cloud_run_v2_service.frontend.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allAuthenticatedUsers"
}
