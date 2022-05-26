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
logging_client = google.cloud.logging.Client()
# Connects the logger to the root logging handler; by default this captures all logs at INFO level and higher
log_handler = logging_client.get_default_handler()
logging.basicConfig()
logger = logging.getLogger('logger')
logger.addHandler(log_handler)
# -------------------------------------------------------
from app.library.pulsar.task import Manager
task=None

# -- Main run function
def run(event, context):
    """
    :param event:
    :param context:
    :return: Tuple (event_id, event_data)
    """

    # Get run context
    run_context = get_run_context()
    # Extract pubsub event ID and Data
    run_context["data"]  = decode_event_data(event)
    run_context["event_id"] = context.event_id

    # Always return the event_id  and the task
    return run_context

def tasked(run_context):
    # Always catch error
    try:
        # Initialize new task
        manager = Manager()
        # Load new task
        manager.load(run_context)

    except Exception as e:
        logger.error(str(e))

def get_run_context():
    run_context = {}
    run_context["project_id"] = os.getenv("GCP_PROJECT")
    run_context["region"] = os.getenv("FUNCTION_REGION")
    run_context["service_account"] = os.getenv("FUNCTION_IDENTITY")
    return run_context

# -- Decode data passed to the Cloud function
def decode_event_data(event):
    """
    Get event and extract json data
    :param event:
    :return: Json object or None
    """
    logger.info("----> Running load_event_data")
    if 'data' in event:
        # Get json string
        json_data = base64.b64decode(event['data']).decode('utf-8')
        logger.info("----> Decoded data: " + str(json_data))
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