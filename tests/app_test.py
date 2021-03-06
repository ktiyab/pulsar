# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

import unittest
import uuid
import json
import base64
import os
import private

# Load test service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private.SERVICE_ACCOUNT_PATH

from app import main
from app import configurations as app_configs
from app.job import Task
from app.runner import Runner
from app.event import SinkTrigger

# Set test env
os.environ["GCP_PROJECT"] = private.GCP_PROJECT
os.environ["FUNCTION_REGION"] = private.FUNCTION_REGION
os.environ["FUNCTION_IDENTITY"] = private.FUNCTION_IDENTITY

# Set test data
event_id = str(uuid.uuid1())
custom_package = app_configs.CUSTOM_PACKAGE
custom_module = "sample"
custom_class = "Greeting"
custom_function = "get"
custom_parameters = "Pulsar"
expected_response = "Hello Pulsar"

custom_run = "{}.{}.{}.{}:{}".format(custom_package, custom_module, custom_class, custom_function, custom_parameters)
data = {
 app_configs.NAME_KEY: "Greeting",
 app_configs.DESCRIPTION_KEY: "return: Hello <parameter>",
 app_configs.ALERT_LEVEL_KEY: "1",
 app_configs.OWNERS_KEY: private.OWNERS_EMAILS,
 app_configs.PARAMETERS_KEY: {
        app_configs.PARAMS_RUN_KEY: custom_run
  }
}

gcs_resource = {
    "protoPayload": {
        "methodName": "storage.objects.create",
        "authenticationInfo": {
            "principalEmail": private.OWNERS_EMAILS
        },
        "requestMetadata": {
            "callerIp": "127.0.0.1"
        }
    },
    "resource": {
        "type": "gcs_bucket",
        "labels": {
            "location": "europe-west1",
            "project_id": private.GCP_PROJECT,
            "bucket_name": "crm_data"
        }
    },
    "resourceName": "projects/_/buckets/logs_sink_gcs",
    "timestamp": "2022-06-01T23:04:53.682013137Z"
}

bq_resource = {
    "protoPayload": {
        "methodName":  "tableservice.insert",
        "authenticationInfo": {
            "principalEmail": private.OWNERS_EMAILS
        },
        "requestMetadata": {
            "callerIp": "127.0.0.1"
        }
    },
    "resource": {
        "type": "bigquery_resource",
        "labels": {
            "project_id": private.GCP_PROJECT
        }
    },
    "resourceName": "projects/pulsar/logs_sink_gcs/pulsar/tables",
    "timestamp": "2022-06-01T23:04:53.682013137Z"
}


class Context:
    event_id = event_id


class AppTest(unittest.TestCase):

    @staticmethod
    def build_sample():
        # Create sample data in cloud function format
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {app_configs.DATA_KEY: encoded_data}
        return event

    @staticmethod
    def build_gcs_protopayload_sample():
        # Create sample data in cloud function format
        data_string = json.dumps(gcs_resource)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {app_configs.DATA_KEY: encoded_data}
        return event

    @staticmethod
    def build_bq_protopayload_sample():
        # Create sample data in cloud function format
        data_string = json.dumps(bq_resource)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {app_configs.DATA_KEY: encoded_data}
        return event

    @staticmethod
    def build_forward_sample():
        # Create sample data in cloud function format
        data_forward_to = data
        data_forward_to[app_configs.PARAMETERS_KEY][app_configs.PARAMS_RESPONSE_TO_KEY] \
            = private.GCP_PROJECT + "." + private.TOPIC_NAME + "@custom.sample.Greeting.get: Forwarded {}"

        data_string = json.dumps(data_forward_to)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {app_configs.DATA_KEY: encoded_data}
        return event

    def test_extract(self):

        runner = Runner()
        runner.load(data[app_configs.PARAMETERS_KEY])

        self.assertEqual(runner.PACKAGE_REFERENCE, custom_package)
        self.assertEqual(runner.MODULE_REFERENCE, custom_module)
        self.assertEqual(runner.CLASS_REFERENCE, custom_class)
        self.assertEqual(runner.FUNCTION_REFERENCE, custom_function)
        self.assertEqual(runner.FUNCTION_PARAMETERS, custom_parameters.split(","))

    def test_runner(self):
        runner = Runner()
        success, response = runner.execute(data[app_configs.PARAMETERS_KEY])
        self.assertEqual(response, expected_response)

    def test_app_run(self):

        event_data = self.build_sample()
        run_context = main.run(event_data, Context)
        self.assertEqual((run_context[app_configs.EVENT_ID_KEY], run_context[app_configs.DATA_KEY]), (event_id, data))

    def test_app_task(self):
        new_job = Task()
        my_task = new_job.to_dict()
        self.assertEqual(type(my_task), dict)

    def test_sink_trigger(self):
        trigger = SinkTrigger()
        success, response = trigger.load(gcs_resource)
        print(response)

    def test_run_gcs_proto_payload(self):
        event_data = self.build_gcs_protopayload_sample()
        run_context = main.run(event_data, Context)
        self.assertEqual(run_context[app_configs.EVENT_ID_KEY], event_id)

    def test_run_bq_proto_payload(self):
        event_data = self.build_bq_protopayload_sample()
        run_context = main.run(event_data, Context)
        self.assertEqual(run_context[app_configs.EVENT_ID_KEY], event_id)

    def test_run_forward_response(self):
        event_data = self.build_forward_sample()
        run_context = main.run(event_data, Context)
        self.assertEqual(run_context[app_configs.EVENT_ID_KEY], event_id)


if __name__ == '__main__':
    unittest.main()
