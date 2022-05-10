# Create the pulsar bucket in a specific region
resource "google_storage_bucket" "pulsar_bucket" {
  provider = google-beta
  name = var.PULSAR_BUCKET_NAME
  location = var.PULSAR_REGION
}