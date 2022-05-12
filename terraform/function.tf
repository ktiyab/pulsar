# Build bucket name
locals {
  SERVICE_ACCOUNT_EMAIL="${var.SERVICE_ACCOUNT_EMAIL}"
}
# Creating Cloud Function Zip file
data "archive_file" "pulsar_zip" {
  type        = "zip"
  source_dir = "../app"
  output_path = "../${var.PULSAR_ZIP}"
}

# Load zip file into Pulsar bucket
resource "google_storage_bucket_object" "pulsar_gcs_zip" {
  provider = google-beta
  bucket       = google_storage_bucket.pulsar_bucket.name
  source = data.archive_file.pulsar_zip.output_path
  content_type = "application/zip"
  name         = var.PULSAR_ZIP
  depends_on = [google_storage_bucket.pulsar_bucket, data.archive_file.pulsar_zip]
}

# Creating the Cloud Function
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions2_function
resource "google_cloudfunctions2_function" "pulsar_function" {
  provider = google-beta
  project = var.PROJECT_ID
  name = var.PULSAR_NAME
  location=var.PULSAR_REGION

  build_config {
    runtime = var.PULSAR_RUNTIME
    entry_point = var.PULSAR_ENTRY_POINT

    source {
      storage_source {
        bucket = google_storage_bucket.pulsar_bucket.name
        object = google_storage_bucket_object.pulsar_gcs_zip.name
      }
    }
  }

  service_config {
    max_instance_count  = var.PULSAR_MAX_INSTANCE
    min_instance_count = var.PULSAR_MIN_INSTANCE
    available_memory    = var.PULSAR_MEMORY
    timeout_seconds     = var.PULSAR_TIMEOUT
    #service_account_email = local.SERVICE_ACCOUNT_EMAIL
    ingress_settings = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
  }

  #event_trigger {
  #  trigger_region = var.PULSAR_REGION
  #  event_type = "google.cloud.pubsub.topic.v1.messagePublished"
  #  pubsub_topic = google_pubsub_topic.pulsar_topic.id
  #  retry_policy = "RETRY_POLICY_RETRY"
  #}

  depends_on = [google_storage_bucket_object.pulsar_gcs_zip, google_pubsub_topic.pulsar_topic]
}