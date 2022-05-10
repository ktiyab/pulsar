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
# Show deployment project
gcloud config configurations list
echo "---> Creating the Cloud function with name: $PULSAR_NAME region:$REGION entrypoint:$PULSAR_ENTRY_POINT memory:$PULSAR_MEMORY runtime:$PULSAR_RUNTIME source:$SOURCE in the project ID $PROJECT_ID"
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
    pwd
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

    # Moving cursor to original position
    cd ./scripts
  else
    echo "---> Using existing Cloud Storage configurations and files"
  fi

  #--  --  --  --  --  -- B -  Deploy PubSub topic --  --  --  --  --  -- --  --  --  --  --  -- --  --  --  --
  read -p "--->> Do you want to create a new topic? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    pwd
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
    pwd
    # -- -- -- C1 - Create new secrets if exist
    read -p "--->>>> Do you want to create new secrets in Secret Manager? [Y/y or N/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      pwd
      echo "---> Creating non existing secrets"

      # -- -- Loop secret folder and load files content into secret manager
      for filename in ../$PULSAR_SECRETS_FOLDER/*$PULSAR_SECRETS_EXT; do
          [ -e "$filename" ] || continue

          # Clean and extract secret name
          echo "---------------------------------"
          echo "Found secret $filename"
          secret_name="${filename//.json}"
          secret_name="${secret_name//"../$PULSAR_SECRETS_FOLDER/"}"
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
      pwd
      echo "---> Creating new version of existing secrets"
      # -- -- Loop secret folder and load files content into secret manager
      for filename in ../$PULSAR_SECRETS_FOLDER/*$PULSAR_SECRETS_EXT; do
          [ -e "$filename" ] || continue

          # Clean and extract secret name
          echo "---------------------------------"
          echo "Found secret $filename"
          secret_name="${filename//.json}"
          secret_name="${secret_name//"../$PULSAR_SECRETS_FOLDER/"}"

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
    pwd
    #Trying to delete it if cloud function if exist
    echo "---> Trying to delete existing cloud function... "
    gcloud beta functions delete "$PULSAR_NAME"  \
    --gen2 \
    --region="$REGION"
    echo "---> The old Cloud function is deleted"

    #------------  Deploy function
    read -p "--> Do you want to create a new Cloud Function? [Y/y or N/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      pwd
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


      echo "---> The new Pulsar Cloud function is accessible on https://console.cloud.google.com/functions/details/$REGION/$PULSAR_NAME?project=$PROJECT_ID"
    fi

    echo "---> Trying to remove cloud function zip from the bucket and local folder... "
    gsutil rm $PULSAR_GCS_SOURCE_PATH
    # Removing the archive
    rm "../$PULSAR_ZIP"
  else
    echo "---> The existing cloud function is not deleted"Test
  fi

  #------------------- E - Deploy Cloud Scheduler Sample  ---------------------------------------------------------
  read -p "--->> Do you want to deploy the Cloud Scheduler sample? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    pwd
    echo "---> Loading Cloud Scheduler sample configurations in path $PULSAR_TASKS_FOLDER/$PULSAR_TASK_SAMPLE"
    MESSAGE_BODY=`cat "../$PULSAR_TASKS_FOLDER/$PULSAR_TASK_SAMPLE"`
    echo "$MESSAGE_BODY"


    #---------------- - Try to delete scheduler if exist and create new one
    echo "---> Trying to delete existing scheduler... "
    # Delete old sample if exist
    gcloud beta scheduler jobs delete "$PULSAR_TASK_SAMPLE_NAME" \
                                      --location="$REGION" \
    # Create scheduler
    echo "---> Scheduling the task JSON with the cron $PULSAR_TASK_SAMPLE_CRON"
    gcloud beta scheduler jobs create pubsub "$PULSAR_TASK_SAMPLE_NAME" \
                                            --location="$REGION" \
                                            --schedule="$PULSAR_TASK_SAMPLE_CRON" \
                                            --topic="$PULSAR_TOPIC" \
                                            --message-body="$MESSAGE_BODY"

  else
    echo "---> The Cloud Scheduler sample is not deployed"
  fi

  #------------------------------ F - Create default tables schema for Pulsar BigQuery------------------
  read -p "--->> Do you want to create the default BigQuery Pulsar analytics tables (tasked, initiated, processed, terminated)? [Y/y or N/n]: " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    pwd
    current_table_date=$(date +"%Y%m%d")

    # Create the Pulsar dataset if not exist
    echo "---> Creating the BigQuery dataset $PULSAR_NAME if not exist"
    bq --location="$REGION" mk -d \
    --description "Pulsar analytical logs." \
    "$PULSAR_NAME"

    # Create tasked default table if not exist
    echo "---> Creating empty tasked tasks table if not exist"
    bq mk --table --description "The Pulsar tasked tasks default table" "$PROJECT_ID:$PULSAR_NAME.tasked_$current_table_date" "$TASK_SCHEMA"

    # Create initiated default table if not exist
    echo "---> Creating empty initiated tasks table if not exist"
    bq mk --table --description "The Pulsar tasks initiated default table" "$PROJECT_ID:$PULSAR_NAME.initiated_$current_table_date" "$TASK_SCHEMA"

    # Create processed default table if not exist
    echo "---> Creating empty processed tasks table if not exist"
    bq mk --table --description "The Pulsar processed tasks default table" "$PROJECT_ID:$PULSAR_NAME.processed_$current_table_date" "$TASK_SCHEMA"

    # Create terminated default table if not exist
    echo "---> Creating empty terminated tasks table if not exist"
    bq mk --table --description "The Pulsar terminated tasks default table" "$PROJECT_ID:$PULSAR_NAME.terminated_$current_table_date" "$TASK_SCHEMA"

  else
    echo "---> The deployment don't create default Pulsar BigQuery tables"
  fi

else
  echo "Operation is aborted"
fi
