# Pulsar

## Introduction

Warning: This is an POC which will be improved

Pulsar aimed to provide a framework skeleton for scalable Cloud Function Apps with:

- Cloud Interfaces for based on Google Cloud Scheduler and Google Cloud Log Sink for event trigger.
- Cloud Storage for file storage and management
- BigQuery for job analytics 

## Deployment

### Activate APIs below
https://console.cloud.google.com/apis/dashboard 
- Cloud Storage
- Cloud Secret Manager
- Cloud Logging
- Cloud Pub/sub
- Cloud function
- Cloud run
- Cloud scheduler
- Cloud Build
- Eventarc API
- Artifact Registry API

### Service account creation

Create a service account with this permissions (don't download the json key)
https://console.cloud.google.com/iam-admin/serviceaccounts

- BigQuery Data Editor
- BigQuery Job User
- Service Account User
- Logging Admin
- Pub/Sub Editor
- Storage Admin
- Secret Manager Secret Accessor