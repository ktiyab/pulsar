locals {
  PULSAR_NAME = var.PULSAR_NAME
  PULSAR_DATASET_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_DATASET_DESCRIPTION}"
  PULSAR_TASKED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_TASKED_TABLE_DESCRIPTION}"
  PULSAR_INITIATED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_INITIATED_TABLE_DESCRIPTION}"
  PULSAR_PROCESSED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_PROCESSED_TABLE_DESCRIPTION}"
  PULSAR_TERMINATED_TABLE_DESCRIPTION = "The ${var.PULSAR_NAME}${var.PULSAR_TERMINATED_TABLE_DESCRIPTION}"

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
    "name": "always_notify",
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
resource "google_bigquery_table" "pulsar_table_tasked" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_TASKED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_TASKED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_initiated" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_INITIATED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_INITIATED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_processed" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_PROCESSED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_PROCESSED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}
resource "google_bigquery_table" "pulsar_table_terminated" {
  dataset_id = google_bigquery_dataset.pulsar_dataset.dataset_id
  table_id   = "${var.PULSAR_TERMINATED_TABLE_NAME}_${local.CURRENT_DATE}"
  description = local.PULSAR_TERMINATED_TABLE_DESCRIPTION

  schema = local.PULSAR_TASK_SCHEMA

}