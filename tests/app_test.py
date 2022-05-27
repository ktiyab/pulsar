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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = private.SERVICE_ACCOUNT_PATH
print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

from app import main
from app.job import Task
from app.runner import Runner

# Set test env
os.environ["GCP_PROJECT"] = private.GCP_PROJECT
os.environ["FUNCTION_REGION"] = private.FUNCTION_REGION
os.environ["FUNCTION_IDENTITY"] = private.FUNCTION_IDENTITY

# Set test data
event_id = str(uuid.uuid1())
custom_package = "custom"
custom_module = "sample"
custom_class = "Greeting"
custom_function = "get"
custom_parameters = "Pulsar"
expected_response = "Hello Pulsar"

custom_run = "{}.{}.{}.{}:{}".format(custom_package, custom_module, custom_class, custom_function, custom_parameters)
data = {
 "always_notify": "true",
 "owners": "tiyab@gcpbees.com",
 "parameters": {
        "run": custom_run,
        "response_to": "topic_name"
  }
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
        event = {"data": encoded_data}
        return event

    def test_extract(self):

        runner = Runner()
        runner.load(data["parameters"])

        self.assertEqual(runner.PACKAGE_REFERENCE, custom_package)
        self.assertEqual(runner.MODULE_REFERENCE, custom_module)
        self.assertEqual(runner.CLASS_REFERENCE, custom_class)
        self.assertEqual(runner.FUNCTION_REFERENCE, custom_function)
        self.assertEqual(runner.FUNCTION_PARAMETERS, custom_parameters.split(","))

    def test_runner(self):
        runner = Runner()
        success, response = runner.execute(data["parameters"])
        self.assertEqual(response, expected_response)

    def test_app_run(self):

        event_data = self.build_sample()
        run_context = main.run(event_data, Context)
        self.assertEqual((run_context["event_id"], run_context["data"]), (event_id, data))

    def test_app_task(self):
        new_job = Task()
        my_task = new_job.to_dict()
        self.assertEqual(type(my_task), dict)


if __name__ == '__main__':
    unittest.main()


