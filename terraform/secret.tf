# TODO: Make it work like the shell script
# Load json files from secret folder contents
locals {
  PULSAR_SENDGRID_SECRET_NAME=var.PULSAR_SENDGRID_SECRET
  PULSAR_SENDGRID_SECRET_JSON_FILE="${local.PULSAR_SENDGRID_SECRET_NAME}${var.PULSAR_SECRET_EXT}"
}

# Create a secret for each json file
resource "google_secret_manager_secret" "pulsar_secret_name" {
  provider = google-beta
  project = var.PROJECT_ID

  secret_id = local.PULSAR_SENDGRID_SECRET_NAME

  replication {
    automatic = true
  }
}

# Add the secret data for each json file
resource "google_secret_manager_secret_version" "pulsar_secret_data" {
  provider = google-beta
  secret = google_secret_manager_secret.pulsar_secret_name.id
  secret_data = file("${path.module}${path.module}/${var.PULSAR_SECRETS_FOLDER}/${local.PULSAR_SENDGRID_SECRET_JSON_FILE}")
  depends_on = [google_secret_manager_secret.pulsar_secret_name]
}