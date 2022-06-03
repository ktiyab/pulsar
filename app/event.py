# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# -- Definitions: event purpose is to manage logs sink data
# This class calls dynamically classes associated to the events
import configurations as app_configs

import importlib
import base64
import requests

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class SinkTrigger(object):
    def __init__(self):
        pass

    def load(self, payload):
        """
        Execute package.module.class.function:parameters (or without parameters)
        :return: tuple
        """
        logger.info("--> event.SinkTrigger.load: Load Cloud Logging Sink trigger parameters...")

        try:
            # -- Extract resource type name and generate class name --
            resource_type = payload["resource"]["type"]

            # Build class name by using resource type name (gsc_object > GcsObject)
            # Refer to app.libs.logging.sink

            name_array = resource_type.split(app_configs.RESOURCE_TYPE_SEP)
            class_reference = ""
            for name in name_array:
                class_reference = class_reference + name.capitalize()

            # Load module
            _module = importlib.import_module("{}.{}".format(app_configs.TRIGGER_PACKAGE_REFERENCE,
                                                             app_configs.TRIGGER_MODULE_REFERENCE)
                                              )

            # Arg
            arg = [payload]

            # Load class
            _class = getattr(_module, class_reference)

            # Load function with parameters if exist

            # -- Extract method name and generate object name --
            method_name = payload["protoPayload"]["methodName"]

            function_reference = method_name.replace(app_configs.PROTO_PAYLOAD_NAME_SEP, app_configs.FUNCTION_NAME_SEP)

            resource_data = getattr(_class, function_reference)(*arg)

            # Build job definition
            # Run path - Always based on the GCP resource name
            # gcs_object = custom.gcs_object.GcsObject.run:<resource_data>
            # Encode the resource information and decode it in the custom class
            data_bytes = resource_data.encode("utf-8")
            encoded_data_bytes = base64.b64encode(data_bytes)
            encoded_data = encoded_data_bytes.decode("utf-8")

            run = app_configs.TRIGGER_RUN.format(resource_type, class_reference, function_reference, encoded_data)

            loaded_sink_job = app_configs.JOB_TEMPLATE
            loaded_sink_job[app_configs.NAME_KEY] = "{} {}".format(class_reference, function_reference)
            loaded_sink_job[app_configs.DESCRIPTION_KEY] = app_configs.TRIGGERED_DESCRIPTION\
                .format(resource_type, method_name)
            loaded_sink_job[app_configs.PARAMETERS_KEY][app_configs.PARAMS_FROM_KEY] = app_configs.TRIGGERED_FROM
            loaded_sink_job[app_configs.PARAMETERS_KEY][app_configs.PARAMS_RUN_KEY] = run

            return True, loaded_sink_job

        except Exception as e:
            # Build message and caption
            message = "event.SinkTrigger.load: Unable to execute with error " + str(e)
            logger.error("--->" + message)
            return False, message
            pass

    def get_metadata(self, internal_url):
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
