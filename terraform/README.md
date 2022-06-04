The "terraform" folder contains the terraform script for deployment.
More about terraform: https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/gcp-get-started

- 1.a - (Only for local tests) Execute the command below to create default credential
```shell
$ gcloud auth application-default login --no-browser
```
- 1.b - Instead of using default credential, it's recommended to create a dedicated service account to terraform
- 2 Deploy
```shell
$ terraform init 
$ terraform plan -var="PULSAR_NAME=[APP-NAME]" -var="PROJECT_ID=[PROJECT-ID]" -var="PULSAR_REGION=[REGION]" -var="SERVICE_ACCOUNT_EMAIL=[SERVICE-ACCOUNT-EMAIL]" -out=tf.plan
$ terraform apply "tf.plan"
```