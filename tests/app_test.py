import unittest
from app import main
from app import secrets_configs
from app.task import Task

import uuid
import json
import base64

# Set test data
gen_id = str(uuid.uuid1())
data="""{"key": "value"}"""

class context:
    event_id=gen_id

class App_test(unittest.TestCase):

    def build_sample(self):
        # Create sample data in cloud function format
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        event = {"data": encoded_data, "messageId": gen_id}
        return event

    def test_app_run(self):

        event_data=self.build_sample()
        event_id, response = main.run(event_data, context)
        self.assertEqual((event_id, response), (gen_id, data))

    def test_app_task(self):
        new_task = Task()
        my_task = new_task.to_dict()
        self.assertEqual(type(my_task), dict)

if __name__ == '__main__':
    unittest.main()
