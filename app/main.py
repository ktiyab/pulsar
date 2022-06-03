# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

import json
import os
import base64
import requests

# -------------------------------------------------------
# Custom functionalities
from job import Job
from notification import Notice
import context as app_context
import configurations as app_configs

# -------------------------------------------------------

# -- -- Configuring the Google Cloud Loging client library
import logging
import google.cloud.logging

# -- -- Instantiates logger client
logging_client = google.cloud.logging.Client()

# -- -- Connects the logger to the root logging handler; by default this captures
# all logs at INFO level and higher
log_handler = logging_client.get_default_handler()
logging.basicConfig()
logger = logging.getLogger('logger')
logger.addHandler(log_handler)


def run(event, context):
    """
    :param event:
    :param context:
    :return: Tuple (event_id, event_data)
    """

    logger.info("--> Main.run: Running task...")

    # Always catch error
    try:
        # Get run context
        job_context = build_context(event, context)

        if job_context:
            # Initialize task
            success, initialized_task = initialize(job_context)

            if success:
                # Check if task is runnable
                success, runnable_task = is_runnable(initialized_task)

                if success:
                    # Execute task
                    success, completed_task = execute(runnable_task)

                    if success:
                        # Send response to pubsub if set
                        success, forwarded_status = forward(completed_task)

            # Always return the event_id  and the task
            return job_context

    except Exception as e:
        # Build emergency notification
        details = "--> Main.run failed with error: " + str(e) + \
                  " \n for app " + str(app_context.APP_NAME) + \
            " \n in the project " + str(app_configs.GCP_PROJECT_ID)
        caption = str(app_context.APP_NAME).upper() + " failure"
        logger.error(details)
        Notice(app_configs.GCP_PROJECT_ID, app_context.APP_NAME).failure(details, caption)
        pass

# - - - - - TASK INITIALIZATION - - - - - - - - - - - - - - - - - -


def initialize(job_context):
    """
    Try to initialized a task
    :param job_context:
    :return:
    """
    logger.info("--> Main.initialize: Loading task...")
    # Always catch error
    try:
        # Initialize new task
        job_task = Job()
        # Load new task
        return job_task.load(job_context)

    except Exception as e:
        logger.error("--> Main.initialize failed with error: " + str(e))


def build_context(event, context):
    """
    Building the running context
    :param event:
    :param context:
    :return:
    """
    logger.info("---->Main.build_context: Decoding provided data and load GCP context.")

    gcp_context = get_gcp_context()
    event_data = decode_event_data(event)
    success = True

    if key_exist(app_configs.PROTO_PAYLOAD, event_data):
        # Extract protoPayload data and build new job definition
        job_proto = Job()
        success, event_data = job_proto.load_proto_payload(event_data, gcp_context, context.event_id)

    if success:
        # Extract pubsub event ID and Data
        job_context = {app_configs.DATA_KEY: event_data, app_configs.EVENT_ID_KEY: context.event_id}

        # Identify caller (Scheduler or Logging Sink)
        if key_exist(app_configs.PROTO_PAYLOAD, event_data):
            # Event is triggered from logging sink
            job_context[app_configs.TRIGGER_TYPE] = app_configs.PROTO_PAYLOAD
        else:
            job_context[app_configs.TRIGGER_TYPE] = app_configs.SCHEDULER

            # Set env info
            job_context.update(gcp_context)

        return job_context
    else:
        return None


def get_gcp_context():
    # Set env info
    gcp_context = {}
    if os.getenv(app_configs.ENV_GCP_PROJECT):
        # Python 3.7 et Go 1.11 envs OR local tests
        gcp_project_id = os.getenv(app_configs.ENV_GCP_PROJECT)
        gcp_context[app_configs.REGION_KEY] = os.getenv(app_configs.ENV_FUNCTION_REGION)
        gcp_context[app_configs.SERVICE_ACCOUNT_KEY] = os.getenv(app_configs.ENV_FUNCTION_IDENTITY)
    else:
        # Get env info from GCP metadata
        gcp_project_id = get_metadata(app_configs.INTERNAL_PROJECT_INFO)
        gcp_context[app_configs.REGION_KEY] = get_metadata(app_configs.INTERNAL_REGION_INFO)
        gcp_context[app_configs.SERVICE_ACCOUNT_KEY] = get_metadata(app_configs.INTERNAL_SERVICE_ACCOUNT_INFO)

    gcp_context[app_configs.PROJECT_ID_KEY] = gcp_project_id

    # Set configs variables
    app_configs.GCP_PROJECT_ID = gcp_project_id
    app_configs.APP_NAME = app_context.APP_NAME

    return gcp_context


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

# -- Decode data passed to the Cloud function  - - - - - - - - - - - -


def decode_event_data(event):
    """
    Get event and extract json data
    :param event:
    :return: Json object or None
    """
    logger.info("---->Main.decode_event_data: Decoding provided data.")
    if app_configs.DATA_KEY in event:
        # Get json string
        json_data = base64.b64decode(event[app_configs.DATA_KEY])
        # Json string to object
        return load_json_data(json_data)

# -- Transform json data into object  - - - - - - - - - - - -


def load_json_data(json_string):
    """
    Try to convert string data into Json object
    :param json_string:
    :return: json object or None
    """
    logger.info("---->Main.load_json_data: Loading JSON data.")
    try:
        json_object = json.loads(json_string)
        return json_object
    except ValueError as e:
        logger.error("---->The value: " + str(json_string) + " is not a valid json data. Error: " + str(e))
        return None

# - - - - - TASK VALIDATION - - - - - - - - - - - - - - - - - -


def is_runnable(initialized_task):
    """
    Try to load task parameters
    :param initialized_task:
    :return:Task
    """
    logger.info("--> Main.is_runnable: Loading task parameters...")
    # Always catch error
    try:
        # Initialize new task
        job_task = Job(initialized_task)
        # Load new task
        return job_task.is_runnable()

    except Exception as e:
        logger.error("--> Main.is_runnable failed with error: " + str(e))


# - - - - - TASK EXECUTION - - - - - - - - - - - - - - - - - -


def execute(runnable_task):
    """
    Try to execute task
    :param runnable_task:
    :return: Task
    """
    logger.info("--> Main.execute: Executing task...")
    # Always catch error
    try:
        # Load ongoing task
        job_task = Job(runnable_task)
        # Run
        return job_task.run()

    except Exception as e:
        logger.error("--> Main.execute failed with error: " + str(e))

# - - - - - RESPONSE FORWARDING - - - - - - - - - - - - - - - - - -


def forward(completed_task):
    """
    Try to forward task response
    :param completed_task:
    :return: Task
    """
    logger.info("--> Main.execute: Executing task...")
    # Always catch error
    try:
        # Load ongoing task
        job_task = Job(completed_task)
        # Run
        return job_task.forward()

    except Exception as e:
        logger.error("--> Main.execute failed with error: " + str(e))

# - - - - - UTILS - - - - - - - - - - - - - - - - - -


def key_exist(key, json_object):
    """
    Check if key exist in json
    :param key:
    :param json_object:
    :return: Bool
    """
    for key_name in json_object:
        if key_name == key:
            return True

    return False
