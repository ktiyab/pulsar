The shell scripts for Pulsar deployment in the "scripts" folder allow to deploy the your app by using Google Cloud CLI. 

- 1 - Install Google Cloud CLI from this link: https://cloud.google.com/sdk/docs/install 
- 2 - Create a deployment service/user account with permissions for GCP services listed above.
- 3 - Open the folder "/scripts/" from you command line
- 4 - The deployment command below will guide you through the questions/responses process (Y/N) in order to configure or not services. For the first deployment, you have to create items/configure all services, but for update the script allows you to skip some parts of the deployment. 
You must always accept GCS files redeployment in order to do cloud function redeployment
```shell
./deploy.sh "APP-NAME"  "PROJECT-ID"  "REGION"  "EXISTING-SERVICE-ACCOUNT-EMAIL"
```
- 5 - Removal command: you can remove specific app by running command below
```shell
./remove.sh "APP-NAME"  "PROJECT-ID"  "REGION"
```