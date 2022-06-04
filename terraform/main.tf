# Call: terraform apply -var="PROJECT_ID=<PROJECT-ID>" -var="SERVICE_ACCOUNT_EMAIL=<SERVICE-ACCOUNT-EMAIL>" -var="REGION=europe-west1"
provider "google" {
  project = var.PROJECT_ID
  region = var.PULSAR_REGION
}

locals {
  CONTEXT = <<-EOT
APP_NAME = "${var.PULSAR_NAME}"
RUNTIME = "${var.PULSAR_RUNTIME}"
PROJECT_ID = "${var.PROJECT_ID}"
REGION = "${var.PULSAR_REGION}"
SERVICE_ACCOUNT_EMAIL = "${var.SERVICE_ACCOUNT_EMAIL}"
TOPIC = "${var.PULSAR_NAME}${var.PULSAR_TOPIC_SUFFIX}"
STORAGE = "${var.PROJECT_ID}-${var.PULSAR_NAME}"
DATASET = "${var.PULSAR_NAME}"
  EOT

  SECRET_VAR = upper("${var.PULSAR_SENDGRID_SECRET}")
  SECRETS = <<-EOT
  ${local.SECRET_VAR} = "${var.PULSAR_SENDGRID_SECRET}"
  EOT
}

resource "local_file" "context_py" {
  content = "${local.CONTEXT}"
  filename = "${path.module}${path.module}/app/${var.PULSAR_CONTEXT_PY_FILE}"
}

resource "local_file" "secrets_py" {
  content = "${local.SECRETS}"
  filename = "${path.module}${path.module}/app/${var.PULSAR_SECRETS_PY_FILE}"
}