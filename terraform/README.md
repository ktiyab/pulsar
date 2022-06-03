This is a shell script for Pulsar deployment by using Google Cloud CLI. 

- 1 - Install Terraform CLI from this link: 
https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started
- [Only for local tests] $ gcloud auth application-default login --no-browser
- $ terraform init 
- $ terraform plan -var="PULSAR_NAME=[APP-NAME]" -var="PROJECT_ID=[PROJECT-ID]" -var="PULSAR_REGION=[REGION]" -var="SERVICE_ACCOUNT_EMAIL=[SERVICE-ACCOUNT-EMAIL]" -out=tf.plan
- $ terraform apply -var="PULSAR_NAME=[APP-NAME]" -var="PROJECT_ID=[PROJECT-ID]" -var="PULSAR_REGION=[REGION]" -var="SERVICE_ACCOUNT_EMAIL=[SERVICE-ACCOUNT-EMAIL]" -out=tf.plan