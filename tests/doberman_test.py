import unittest
import uuid
import json
import base64
from app import configurations as app_configs
from event import SinkTrigger
from runner import Runner
import private

# Load test service account
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private.SERVICE_ACCOUNT_PATH

# Create the expected resource
bq_resource = {
    "protoPayload": {
        "methodName":  "datasetservice.insert",
        "authenticationInfo": {
            "principalEmail": "doberman@watchdogs.com"
        },
        "requestMetadata": {
            "callerIp": "127.0.0.1"
        },
        "resourceLocation": {
            "currentLocations": ["europe-west1"]
        },
        "serviceData": {
            "datasetInsertResponse": {
                "resource": {
                    "datasetName": {
                        "projectId": "birdly-crm-fr",
                        "datasetId": "june_2022_reports"
                    }
                }
            }
        }
    },
    "resource": {
        "type": "bigquery_resource"
    },
    "timestamp": "2022-06-01T23:04:53.682013137Z"
}

# Create the expected resource
gcs_resource = {
    "protoPayload": {
        "methodName":  "storage.buckets.create",
        "authenticationInfo": {
            "principalEmail": "doberman@watchdogs.com"
        },
        "requestMetadata": {
            "callerIp": "127.0.0.1"
        },
        "resourceLocation": {
            "currentLocations": "europe-west6"
        },
    },
    "resource": {
        "labels": {
            "location": "europe-west2",
            "project_id": "birdly-crm-fr",
            "bucket_name": "june_2022_reports"
        },
        "type": "gcs_bucket"
    },
    "timestamp": "2022-06-01T23:04:53.682013137Z"
}


class Context:
    event_id = str(uuid.uuid1())
    event_id = event_id


class DobermanTest(unittest.TestCase):

    def test_bigquery_sink_job(self):

        # Interpreting triggered json as job
        trigger = SinkTrigger()
        success, job = trigger.load(bq_resource)
        if success:
            # Load custom class runner and pass job parameters for execution
            custom_runner = Runner()
            success, response = custom_runner.execute(job["parameters"])
            self.assertEqual(success, True)

    def test_storage_sink_job(self):

        # Interpreting triggered json as job
        trigger = SinkTrigger()
        success, job = trigger.load(gcs_resource)
        if success:
            # Load custom class runner and pass job parameters for execution
            custom_runner = Runner()
            success, response = custom_runner.execute(job["parameters"])
            self.assertEqual(success, True)
