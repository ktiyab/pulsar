import json


class GcsBucket(object):

    @staticmethod
    def storage_buckets_create(payload):
        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["methodName"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "location": payload["resource"]["labels"]["location"],
            "project_id": payload["resource"]["labels"]["project_id"],
            "bucket_name": payload["resource"]["labels"]["bucket_name"],
            "timestamp": payload["timestamp"]
        })


class BigqueryResource(object):

    @staticmethod
    def datasetservice_insert(payload):
        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["methodName"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "currentLocations": payload["protoPayload"]["resourceLocation"]["currentLocations"][0],
            "projectId": payload["protoPayload"]["serviceData"]["datasetInsertResponse"]["resource"]["datasetName"]["projectId"],
            "datasetId": payload["protoPayload"]["serviceData"]["datasetInsertResponse"]["resource"]["datasetName"]["datasetId"],
            "timestamp": payload["timestamp"]
        })
