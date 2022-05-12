resource "google_pubsub_topic" "pulsar_topic" {
  provider = google-beta
  project = var.PROJECT_ID
  name=var.PULSAR_TOPIC
}