variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "edem-hackathon-2026"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
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

variable "firestore_location" {
  description = "Firestore database location"
  type        = string
  default     = "europe-west1"
}
