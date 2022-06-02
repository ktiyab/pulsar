import base64

class BigqueryResource(object):

    @staticmethod
    def tableservice_insert(payload):
        base64_str = payload.encode("utf-8")
        base64_bytes = base64.b64decode(base64_str)
        decode_str = base64_bytes.decode("utf-8")

        return str(decode_str)
