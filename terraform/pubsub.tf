resource "google_pubsub_topic" "pulsar_topic" {
  provider = google-beta
  name=var.PULSAR_TOPIC
}