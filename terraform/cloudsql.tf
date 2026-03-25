resource "google_sql_database_instance" "postgres" {
  name             = "gft-hackaton-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }

  deletion_protection = false

  depends_on = [google_project_service.sqladmin]
}

resource "google_sql_database" "default" {
  name     = "app"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "default" {
  name     = "app"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
}
