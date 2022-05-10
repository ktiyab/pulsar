# Call: terraform apply -var="PROJECT_ID=<PROJECT-ID>" -var="SERVICE_ACCOUNT_EMAIL=<SERVICE-ACCOUNT-EMAIL>" -var="REGION=europe-west1"
provider "google" {
  project = var.PROJECT_ID
  region = var.PULSAR_REGION
}