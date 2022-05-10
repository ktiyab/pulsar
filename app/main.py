# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

import json
import os
import base64
import logging
import globals as globals_configs

# -- -- Imports the Google Cloud Loging client library
import google.cloud.logging
dir_path = os.path.dirname(os.path.realpath(__file__))
# Instantiates logger client
logging_client = google.cloud.logging.Client()
# Connects the logger to the root logging handler; by default this captures all logs at INFO level and higher
log_handler = logging_client.get_default_handler()
logging.basicConfig()
logger = logging.getLogger('logger')
logger.addHandler(log_handler)

# Get default configs
globals_configs.DEFAULT_PROJECT_ID = os.getenv("GCP_PROJECT")
globals_configs.DEFAULT_REGION = os.getenv("FUNCTION_REGION")
globals_configs.DEFAULT_SERVICE_ACCOUNT = os.getenv("FUNCTION_IDENTITY")

# -- Main run function
def pulse(event, context):
    """

    :param event:
    :param context:
    :return:
    """

    # Extract pubsub event ID and Data
    globals_configs.PUB_SUB_MESSAGE_ID = context.event_id
    event_data = decode_event_data(event)

    print(event_data)

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
        logger.info("----> Event " + str(json_data))
        # Json string to object
        return load_json_data(json_data)

# -- Transform json data into object
def load_json_data(json_string):
    """
    Try to convert string data into Json object
    :param json_string:
    :return: json object or None
    """
    logger.info("----> Running load_json_data")
    try:
        json_object = json.loads(json_string)
        return json_object
    except ValueError as e:
        logger.error("---->The value: " + str(json_string) + " is not a valid json data. Error: " + str(e))
        return None

    return None