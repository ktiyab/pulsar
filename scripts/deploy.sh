#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for light GCP event-based Apps
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# More about commands
# Cloud function https://cloud.google.com/sdk/gcloud/reference/functions/deploy
# Topic https://cloud.google.com/sdk/gcloud/reference/pubsub/topics/create

# Deployment command: ./deploy.sh "<PROJECT-ID>" "<EXISTING-SERVICE-ACCOUNT-EMAIL>" "<REGION>"

# --  --  --  --  --  --  Deployment of the Cloud Function Skeleton and his PubSub topic --  --  --  --  --  --
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
    echo "---> The app will be deployed in GCP project: "$1
    PROJECT_ID=$1
fi

# -- Check if service account email is set
if [ -z "$2" ]
  then
    echo "---> Service account email is not provided, please provide valid one for the deployment;"
    exit 1
  else
    echo "---> The app will use the service account email: "$2
    SERVICE_ACCOUNT_EMAIL=$2
fi

# -- Check if default region is empty
REGION=$PULSAR_REGION
if [ -z "$3" ]
  then
    echo "---> No custom region is specified, the deployment will use the default one: "$PULSAR_REGION
  else
    echo "---> Custom region is specified, the deployment will use region: "$3
    REGION=$3
fi

# --  -- Build default resources names
# Default storage buckets names
PULSAR_BUCKET_NAME=$PROJECT_ID$PULSAR_BUCKET_ID_SUFFIX

# Default resources paths
PULSAR_BUCKET_NAME_PATH="gs://"$PULSAR_BUCKET_NAME"/"
PULSAR_GCS_SOURCE_PATH=$PULSAR_BUCKET_NAME_PATH$PULSAR_ZIP


# Notification
echo "---> Creating the Cloud function with name: $PULSAR_NAME region:$REGION entrypoint:$PULSAR_ENTRY_POINT memory:$PULSAR_MEMORY runtime:$PULSAR_RUNTIME source:$SOURCE"
read -p "---> Continue? [Y/y or N/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo "Deployment"

  # --  --  --  --  --  --   A - Create cloud function zip from file  --  --  --  --  --  -- --  --  --  --
  read -p "--->> Do you want to configure Cloud Storage and load files? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      # Root folder
      cd ..
      echo "---> Creating the Cloud functions ZIP file..."

      # Removing existing zip
      rm $PULSAR_ZIP
      cd "$PULSAR_FOLDER"

      # Write new version date
      echo 'Pulsar build of: '$(date +"%m/%d/%Y") > README.txt
      zip -r "../$PULSAR_ZIP" *

      # --  --  --  --  --  -- A1 - Create buckets if not exist --  --  --  --  --  -- --  --  --  --  --  --
      echo "---> Creating the default GCS bucket $PULSAR_BUCKET_NAME if not exist..."
      # Root folder
      cd ..
      gsutil mb -l $REGION $PULSAR_BUCKET_NAME_PATH

      # Copy function to bucket
      echo "---> Trying to delete existing cloud function zip in the bucket... "
      gsutil rm $PULSAR_GCS_SOURCE_PATH
      echo "---> Copying the cloud function to the bucket..."
      gsutil cp "$PULSAR_ZIP" "$PULSAR_BUCKET_NAME_PATH"
  else
      echo "---> Using existing Cloud Storage configurations and files"
  fi

  #--  --  --  --  --  -- B -  Deploy PubSub topic --  --  --  --  --  -- --  --  --  --  --  -- --  --  --  --
  read -p "--->> Do you want to create a new topic? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      #--  --  --  -- Creating topic
      echo "---> Creating topic if not exist $PULSAR_TOPIC"
      gcloud pubsub topics create "$PULSAR_TOPIC"
      echo "---> The pulsar topic is created"
  else
      echo "---> Using existing topic"
  fi

  #--  --  --  --  --  -- C -  Deploy Secret Manager files --  --  --  --  --  -- --  --  --  --  --  -- --  --
  read -p "--->> Do you want to configure Cloud Secret Manager for Pulsar ? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    # -- -- -- C1 - Create new secrets if exist
    read -p "--->>>> Do you want to create new secrets in Secret Manager? [Y/y or N/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
          echo "---> Creating non existing secrets"
          # -- -- Loop secret folder and load files content into secret manager
          for filename in ./$PULSAR_SECRETS_FOLDER/*$PULSAR_SECRETS_EXT; do
              [ -e "$filename" ] || continue

              # Clean and extract secret name
              echo "---------------------------------"
              echo "Found secret $filename"
              secret_name="${filename//.json}"
              secret_name="${secret_name//"./$PULSAR_SECRETS_FOLDER/"}"
              echo "Secret name is $secret_name"
              existing_secret=$(gcloud secrets list --filter=$secret_name)
              echo "Found $existing_secret"

              # If value secret doesn't exist create it
              if [[ $existing_secret == "" ]]; then
                echo "--> Create new secret with name $secret_name"
                gcloud secrets create $secret_name --replication-policy="automatic"
                gcloud secrets versions add $secret_name --data-file=$filename
              else
                echo "--> The secret exist, you can update automatically the secret in next step."
              fi
              echo "---------------------------------"
          done
    fi
    # -- -- -- C2 - Update existing secrets if exist
    read -p "--->>>> Do you want to create new version of existing secrets in Secret Manager? [Y/y or N/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
          echo "---> Creating new version of existing secrets"
          # -- -- Loop secret folder and load files content into secret manager
          for filename in ./$PULSAR_SECRETS_FOLDER/*$PULSAR_SECRETS_EXT; do
              [ -e "$filename" ] || continue

              # Clean and extract secret name
              echo "---------------------------------"
              echo "Found secret $filename"
              secret_name="${filename//.json}"
              secret_name="${secret_name//"./$PULSAR_SECRETS_FOLDER/"}"

              # If value secret doesn't exist create it
              gcloud secrets versions add $secret_name --data-file=$filename

              echo "---------------------------------"
          done
    fi

  else
      echo "---> The existing Cloud Secret Manager items will be used"
  fi

  #--  --  --  --  --  -- D -  Deploy Cloud Function --  --  --  --  --  -- --  --  --  --  --  -- --  -- --
  read -p "--->>>> Do you want to deploy new cloud function? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      #Trying to delete it if cloud function if exist
      echo "---> Trying to delete existing cloud function... "
      gcloud beta functions delete "$PULSAR_NAME"  \
      --gen2 \
      --region="$REGION"
      echo "---> The old Cloud function is deleted"

          #------------  Deploy function
          read -p "--> Do you want to create a new cloud function? [Y/y or N/n]: " -n 1 -r
          echo
          if [[ $REPLY =~ ^[Yy]$ ]]
          then
              echo "---> Creating the Cloud function with name: $PULSAR_NAME region:$PULSAR_REGION entrypoint:$PULSAR_ENTRY_POINT memory:$PULSAR_MEMORY runtime:$PULSAR_RUNTIME source:$PULSAR_GCS_SOURCE_PATH"
              gcloud beta functions deploy "$PULSAR_NAME" \
                                      --gen2 \
                                      --region="$REGION" \
                                      --service-account="$PULSAR_SERVICE_ACCOUNT" \
                                      --entry-point="$PULSAR_ENTRY_POINT" \
                                      --memory="$PULSAR_MEMORY" \
                                      --runtime="$PULSAR_RUNTIME" \
                                      --source="$PULSAR_GCS_SOURCE_PATH" \
                                      --trigger-topic="$PULSAR_TOPIC" \
                                      --timeout="$PULSAR_TIMEOUT" \
                                      --min-instances="$PULSAR_MIN_INSTANCE" \
                                      --max-instances="$PULSAR_MAX_INSTANCE" \
                                      --no-allow-unauthenticated


              echo "---> The new cumulus Cloud function is accessible on https://console.cloud.google.com/functions/details/$REGION/$PULSAR_NAME?project=$PROJECT_ID"
          fi
  else
      echo "---> The existing cloud function is not deleted"
  fi

  echo "---> Trying to remove cloud function zip from the bucket and local folder... "
  gsutil rm $PULSAR_GCS_SOURCE_PATH
  rm $PULSAR_ZIP


else
  echo "Operation is aborted"
fi
