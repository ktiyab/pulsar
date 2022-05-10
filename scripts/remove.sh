#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for light GCP event-based Apps
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Remove deployment command: ./remove.sh "<PROJECT-ID>" "<REGION>"
# --  --  --  --  --  --  Remove the deployment of the Cloud Function Skeleton and his PubSub topic --  --  --  --  --  --
# --  --  PARAMETERS CHECKS  --  --
# -- Check if .env file exists, and load default configurations
if [ -e .variables ]; then
    source .variables
else
    echo "--->Please set up your .env file before deployment."
    exit 1
fi

# -- Check if project ID is set
if [ -z "$1" ]
  then
    echo "---> Project ID is not provided, please provide valid one for the deployment;"
    exit 1
  else
    echo "---> The app will be removed from the GCP project: "$1
    PROJECT_ID=$1
fi

# -- Check if default region is empty
REGION=$PULSAR_REGION
if [ -z "$2" ]
  then
    echo "---> No custom region is specified, the process  will use the default one: "$PULSAR_REGION
  else
    echo "---> Custom region is specified, the process  will use region: "$2
    REGION=$2
fi

# --  -- Build default resources names
# Default storage buckets names
PULSAR_BUCKET_NAME=$PROJECT_ID$PULSAR_BUCKET_ID_SUFFIX

# Default resources paths
PULSAR_BUCKET_NAME_PATH="gs://"$PULSAR_BUCKET_NAME"/"

echo "---> Do you really want to remove "$PULSAR_NAME" from the project "$PROJECT_ID" ?"

read -p "---> Continue? [Y/y or N/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Removing "$PULSAR_NAME" cloud function..."
  gcloud beta functions delete "$PULSAR_NAME" \
                          --gen2 \
                          --region="$REGION"

  echo "Removing "$PULSAR_NAME" pubsub..."
  gcloud pubsub topics delete "$PULSAR_TOPIC"

  echo "Removing "$PULSAR_NAME" storage bucket..."
  gsutil rb $PULSAR_BUCKET_NAME_PATH

else
    echo "Removing "$PULSAR_NAME" operation is ABORTED"
fi

echo ">>>> 1 - Please don't forget to remove "$PULSAR_NAME" BIGQUERY DATASET from the project "$PROJECT_ID" MANUALLY"
echo ">>>> 2 - Please don't forget to remove "$PULSAR_NAME" SECRETS from the project "$PROJECT_ID" MANUALLY"