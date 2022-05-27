import unittest
import uuid
import json
import base64
import os

# Set test env
import private
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=private.SERVICE_ACCOUNT_PATH
print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

os.environ["GCP_PROJECT"]=private.GCP_PROJECT
os.environ["FUNCTION_REGION"]=private.FUNCTION_REGION
os.environ["FUNCTION_IDENTITY"]=private.FUNCTION_IDENTITY

from app import main
from job import Task

# Set test data
event_id = str(uuid.uuid1())
data={
	"always_notify": "true",
	"owners": "wealthman@gcpbees.com",
	"parameters": {
		"run": "Sample-->HelloWorld->('Hello', 'World')",
		"response_to": "topic_name"
	}
}

class context:
    event_id=event_id

class App_test(unittest.TestCase):

    def build_sample(self):
        # Create sample data in cloud function format
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {"data": encoded_data}
        return event

    def test_app_run(self):

        event_data=self.build_sample()
        run_context = main.run(event_data, context)
        self.assertEqual((run_context["event_id"], run_context["data"]), (event_id, data))

    def test_app_task(self):
        new_job = Task()
        my_task = new_job.to_dict()
        self.assertEqual(type(my_task), dict)

if __name__ == '__main__':
    unittest.main()
