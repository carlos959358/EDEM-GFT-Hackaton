resource "google_storage_bucket" "storage" {
  name          = "gft-hackaton-storage"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}
