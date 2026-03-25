variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "spa-datajuniorsprogram-sdb-001"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "credentials_file" {
  description = "Path to the GCP service account key file"
  type        = string
  default     = "../spa-datajuniorsprogram-sdb-001-899009cc32ac.json"
}

variable "service_name" {
  description = "Nombre del recurso en Cloud Run"
  type        = string
  default     = "cloudrun-service"
}

variable "container_image" {
  description = "La imagen de Docker que se va a desplegar"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello" #cambiar cuando sea necesario
}

