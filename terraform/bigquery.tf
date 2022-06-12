locals {
  PULSAR_NAME = var.PULSAR_NAME
  PULSAR_DATASET_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_DATASET_DESCRIPTION}"
  PULSAR_READY_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_READY_TABLE_DESCRIPTION}"
  PULSAR_RUNNABLE_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_RUNNABLE_TABLE_DESCRIPTION}"
  PULSAR_COMPLETED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_COMPLETED_TABLE_DESCRIPTION}"
  PULSAR_INTERRUPTED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_INTERRUPTED_TABLE_DESCRIPTION}"

  CURRENT_DATE = formatdate("YYYYMMDD", timestamp())
PULSAR_TASK_SCHEMA= <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "description",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "state",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "app",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "project_id",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "region",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "service_account",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "runtime",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "memory",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "alert_level",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "owners",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "parameters",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "acknowledge_timestamp",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "processed_timestamp",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "success",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "details",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF
}
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "pulsar_dataset" {
  dataset_id                  = local.PULSAR_NAME
  friendly_name               = local.PULSAR_NAME
  description                 = local.PULSAR_DATASET_DESCRIPTION
  location                    = var.PULSAR_REGION
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table
resource "google_bigquery_table" "pulsar_table_ready" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_READY_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_READY_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_runnable" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_RUNNABLE_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_RUNNABLE_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_completed" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_COMPLETED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_COMPLETED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_interrupted" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_INTERRUPTED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_INTERRUPTED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}