# Load json files from secret folder contents
locals {
  # https://www.terraform.io/language/functions/fileset
  json_files = fileset(path.module,"${var.PULSAR_SECRETS_FOLDER}/*.json")
  json_data  = [ for f in local.json_files : jsondecode(file("${path.module}/${f}")) ]
}

# Create a secret for each json file
resource "google_secret_manager_secret" "pulsar_secret" {
  provider = google-beta

  for_each = { for f in local.json_data : f.id => f }
  secret_id = each.value.id

  replication {
    automatic = true
  }
}

# Add the secret data for each json file
resource "google_secret_manager_secret_version" "pulsar_secret" {
  for_each = { for f in local.json_data : f.id => f }
  secret = each.value.id
  secret_data = jsonencode(each.value)
}