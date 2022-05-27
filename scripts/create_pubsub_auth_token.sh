#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for light GCP event-based Apps
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com


# -- If you enabled the Pub/Sub service account on or before April 8, 2021,
# grant the iam.serviceAccountTokenCreator role to the Pub/Sub service account:

# -- Check if project ID is set
if [ -z "$1" ]
  then
    echo "---> Project ID is not provided, please provide valid one for the pubsub;"
    exit 1
  else
    echo "---> The serviceAccount will be create in the GCP project: $1"
    PROJECT_ID=$1
fi

# Set cursor on right project
echo "You current project is"
echo "---------------------------------------------------- ----------------------------------------------------"
gcloud config set project $PROJECT_ID
gcloud config configurations list
echo "---------------------------------------------------- ----------------------------------------------------"

PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member  serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
  --role roles/iam.serviceAccountTokenCreator