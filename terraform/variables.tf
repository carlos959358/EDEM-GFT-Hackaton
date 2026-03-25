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

variable "db_user" {
  description = "Usuario administrador de la base de datos"
  type        = string
}

variable "db_password" {
  description = "Contraseña del administrador de la base de datos"
  type        = string
  sensitive   = true
}