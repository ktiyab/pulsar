locals {
  PULSAR_TASK_SAMPLE_NAME="${var.PULSAR_NAME}${var.PULSAR_TASK_SAMPLE_NAME_SUFFIX}"
  PULSAR_TASK_SAMPLE_DESCRIPTION="The ${var.PULSAR_NAME}${var.PULSAR_TASK_SAMPLE_DESCRIPTION}"
}
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resour$%7Bvar.file_data%7D%22ces/cloud_scheduler_job
resource "google_cloud_scheduler_job" "pulsar_scheduler" {
  provider = google-beta
  project = var.PROJECT_ID
  region = var.PULSAR_REGION
  name    = local.PULSAR_TASK_SAMPLE_NAME
  description = var.PULSAR_TASK_SAMPLE_DESCRIPTION
  schedule    = var.PULSAR_TASK_SAMPLE_CRON

  pubsub_target {
    # topic.id is the topic's full resource name.
    topic_name = google_pubsub_topic.pulsar_topic.id
    data       = base64encode(file("${path.module}${path.module}/${var.PULSAR_TASKS_FOLDER}/${var.PULSAR_TASK_SAMPLE_JSON}"))
  }
}