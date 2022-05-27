# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

import json
import os
import base64

# -- -- Configuring the Google Cloud Loging client library
import logging
import google.cloud.logging

# Instantiates logger client
import requests

logging_client = google.cloud.logging.Client()

# Connects the logger to the root logging handler; by default this captures all logs at INFO level and higher
log_handler = logging_client.get_default_handler()
logging.basicConfig()
logger = logging.getLogger('logger')
logger.addHandler(log_handler)

# -------------------------------------------------------
from job import Job
import  context as app_context
import configurations as app_configs

# Minimal context
project_id = os.getenv("GCP_PROJECT")
app_name = app_context.APP_NAME


task=None
notify=None

# -- Main run function
def run(event, context):
    """
    :param event:
    :param context:
    :return: Tuple (event_id, event_data)
    """

    # Always catch error
    try:
        # Get run context
        job_context = build_context(event, context)

        # Set task cursor to entry
        job_task=initialize(job_context)

        # Run task parameters

        # Always return the event_id  and the task
        return job_context

    except Exception as e:
        # Build emergency notification
        details = "--> Main.run failed with error: " + str(e) + \
                  " \n for app " + str() + \
            " \n in the project " + str(project_id)
        caption = str(app_context.APP_NAME) + " failure"
        logger.error(details)
        notify.failure(details, caption)

def initialize(job_context):
    """
    Try to initialized a task
    :param job_context:
    :return:
    """
    logger.info("--> Main.tasked: Loading task...")
    # Always catch error
    try:
        # Initialize new task
        new_job = Job()

        # Load new task
        task = new_job.load(job_context)


        return task

    except Exception as e:
        logger.error("--> Main.tasked failed with error: " + str(e))

def build_context(event, context):
    """
    Building the running context
    :param event:
    :param context:
    :return:
    """
    logger.info("---->Main.build_context: Decoding provided data.")
    job_context = {}

    # Extract pubsub event ID and Data
    job_context["data"] = decode_event_data(event)
    job_context["event_id"] = context.event_id

    # Set env info
    if os.getenv("GCP_PROJECT"):
        # Python 3.7 et Go 1.11 envs OR local tests
        job_context["project_id"] = os.getenv("GCP_PROJECT")
        job_context["region"] = os.getenv("FUNCTION_REGION")
        job_context["service_account"] = os.getenv("FUNCTION_IDENTITY")
    else:
        # Other envs
        job_context["project_id"] = get_metadata(app_configs.INTERNAL_PROJECT_INFO)
        job_context["region"] = get_metadata(app_configs.INTERNAL_REGION_INFO)
        job_context["service_account"] = get_metadata(app_configs.INTERNAL_SERVICE_ACCOUNT_INFO)

    return job_context

def get_metadata(internal_url):
    """
    Get GCP internal meta data
    :param internal_url:
    :return: Object
    """
    logger.info("---->Main.get_metadata: Getting GCP internal meta data.")
    response = requests.get(url=internal_url, headers={'Metadata-Flavor': 'Google'})
    if internal_url == app_configs.INTERNAL_REGION_INFO:
        return str(response.text.split("/")[3])
    else:
        return str(response.text)


# -- Decode data passed to the Cloud function
def decode_event_data(event):
    """
    Get event and extract json data
    :param event:
    :return: Json object or None
    """
    logger.info("---->Main.decode_event_data: Decoding provided data.")
    if 'data' in event:
        # Get json string
        json_data = base64.b64decode(event['data'])
        # Json string to object
        return load_json_data(json_data)

# -- Transform json data into object
def load_json_data(json_string):
    """
    Try to convert string data into Json object
    :param json_string:
    :return: json object or None
    """
    logger.info("----> Running load_json_data.")
    try:
        json_object = json.loads(json_string)
        return json_object
    except ValueError as e:
        logger.error("---->The value: " + str(json_string) + " is not a valid json data. Error: " + str(e))
        return None

    return None