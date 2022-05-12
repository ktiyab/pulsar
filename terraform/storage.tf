# Build bucket name
locals {
  PULSAR_BUCKET_NAME = "${var.PROJECT_ID}${var.PULSAR_BUCKET_ID_SUFFIX}"
}
# Create the pulsar bucket in a specific region
resource "google_storage_bucket" "pulsar_bucket" {
  provider = google-beta
  project = var.PROJECT_ID
  name = local.PULSAR_BUCKET_NAME
  location = var.PULSAR_REGION
}