This is a shell script for Pulsar deployment by using Google Cloud CLI. 

- 1 - Install Google Cloud CLI from this link: https://cloud.google.com/sdk/docs/install 
- 2 - Create a service account with your application permissions scope in GCP
- 3 - Deployment command: ./deploy.sh "<APP-NAME>" "<PROJECT-ID>" "<REGION>" "<EXISTING-SERVICE-ACCOUNT-EMAIL>"
- 4 - Removal command: ./remove.sh "<APP-NAME>" "<PROJECT-ID>" "<REGION>"