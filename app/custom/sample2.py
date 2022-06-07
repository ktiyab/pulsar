import base64


class Greeting2(object):
    def __init__(self):
        pass

    @staticmethod
    def say(message):
        decoded_message = Greeting2.decode(message)
        return "From sample 2 Say: {}".format(decoded_message)

    @staticmethod
    def decode(payload):
        # Decode forwarded resource information before consumption
        base64_str = payload.encode("utf-8")
        base64_bytes = base64.b64decode(base64_str)
        return base64_bytes.decode("utf-8")
