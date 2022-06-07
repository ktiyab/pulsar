import time
import base64

class Greeting(object):
    def __init__(self):
        pass

    @staticmethod
    def get(name):
        return Greeting.response("From sample 1: Get Hello {}".format(name))

    @staticmethod
    def say(message):
        return Greeting.response("From sample 1: Say {}".format(message))

    @staticmethod
    def sleeper(sec):
        time.sleep(int(sec))
        return Greeting.response("From sample 1: Process waited {} seconds.".format(sec))

    @staticmethod
    def response(json_data):
        # Encode the resource information before forwarding
        data_bytes = json_data.encode("utf-8")
        encoded_data = base64.b64encode(data_bytes)
        decoded_data = encoded_data.decode("utf-8")
        return decoded_data

