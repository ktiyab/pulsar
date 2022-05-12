locals {
  CURRENT_DATE = formatdate("YYYYMMDD", timestamp())
PULSAR_TASK_SCHEMA= <<EOF
[
  {
    "name": "task_id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_notifier",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_owners",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_project_id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_region",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_parameters",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_timestamp",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_success",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "task_message",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "pulsar_dataset" {
  dataset_id                  = var.PULSAR_NAME
  friendly_name               = var.PULSAR_NAME
  description                 = var.PULSAR_DATASET_DESCRIPTION
  location                    = var.PULSAR_REGION
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table
resource "google_bigquery_table" "pulsar_table_tasked" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_TASKED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = var.PULSAR_TASKED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_initiated" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_INITIATED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = var.PULSAR_INITIATED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_processed" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_PROCESSED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = var.PULSAR_PROCESSED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_terminated" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_TERMINATED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = var.PULSAR_TERMINATED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}