# Build bucket name
locals {
  SERVICE_ACCOUNT_EMAIL=var.SERVICE_ACCOUNT_EMAIL
  PULSAR_ZIP = "${var.PULSAR_NAME}.${var.PULSAR_ZIP}"
}
# Creating Cloud Function Zip file
data "archive_file" "pulsar_zip" {
  type        = var.PULSAR_ZIP
  source_dir = "../app"
  output_path = "../${local.PULSAR_ZIP}"
}

# Load zip file into Pulsar bucket
resource "google_storage_bucket_object" "pulsar_gcs_zip" {
  provider = google-beta
  bucket       = google_storage_bucket.pulsar_bucket.name
  source = data.archive_file.pulsar_zip.output_path
  content_type = "application/zip"
  name         = local.PULSAR_ZIP
  depends_on = [google_storage_bucket.pulsar_bucket, data.archive_file.pulsar_zip]
}

# Creating the Cloud Function

# Enable Cloud Functions API
resource "google_project_service" "pulsar_cloud_function_service" {
  project = var.PROJECT_ID
  service = "cloudfunctions.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Enable Cloud Build API
resource "google_project_service" "pulsar_cloud_build_service" {
  project = var.PROJECT_ID
  service = "cloudbuild.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions2_function
resource "google_cloudfunctions_function" "pulsar_function" {

  project = var.PROJECT_ID
  name = var.PULSAR_NAME
  region=var.PULSAR_REGION

  runtime = var.PULSAR_RUNTIME
  entry_point = var.PULSAR_ENTRY_POINT
  source_archive_bucket = google_storage_bucket.pulsar_bucket.name
  source_archive_object = google_storage_bucket_object.pulsar_gcs_zip.name
  max_instances  = var.PULSAR_MAX_INSTANCE
  min_instances = var.PULSAR_MIN_INSTANCE
  available_memory_mb = var.PULSAR_MEMORY
  timeout = var.PULSAR_TIMEOUT
  service_account_email=local.SERVICE_ACCOUNT_EMAIL

  event_trigger {
      event_type    = "google.pubsub.topic.publish"
      resource      = google_pubsub_topic.pulsar_topic.name
  }

  depends_on = [google_storage_bucket_object.pulsar_gcs_zip, google_pubsub_topic.pulsar_topic]
}