locals {
 PULSAR_TOPIC = "${var.PULSAR_NAME}${var.PULSAR_TOPIC_SUFFIX}"
}
resource "google_pubsub_topic" "pulsar_topic" {
  provider = google-beta
  project = var.PROJECT_ID
  name=local.PULSAR_TOPIC
}