This is a shell script for Pulsar deployment by using Google Cloud CLI. 

- 1 - Install Terraform CLI from this link: 
https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started
- [Only for local tests] $ gcloud auth application-default login --no-browser
- $ terraform init 
- $ terraform plan -var="PROJECT_ID=gcpbees" -var="SERVICE_ACCOUNT_EMAIL=pulsar@gcpbees.iam.gserviceaccount.com" -var="PULSAR_REGION=europe-west1"
