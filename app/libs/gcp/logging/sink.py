
import calendar
import json
import time

# https://cloud.google.com/logging/docs/view/query-library-preview


class GcsObject(object):
    """
    Resource type name is "gcs_object" > class GcsObject
    You can extend extracted values
    """

    @staticmethod
    def as_json(payload):

        """
        Load key details as object
        :param payload:
        :return:
        """
        return json.dumps({
            "resourceType": payload["protoPayload"]["method_name"],
            "methodName": payload["protoPayload"]["method_name"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "resourceLocation": payload["resource"]["labels"]["location"],
            "resourceProjectId": payload["resource"]["labels"]["project_id"],
            "resourceBucketName": payload["resource"]["labels"]["bucket_name"],
            "resourceName": payload["resource"]["labels"]["bucket_name"],
            "timestamp": str(calendar.timegm(time.gmtime()))
        })


class BigqueryTable(object):
    """
    Resource type name is "bigquery_table" > class BigqueryTable
    You can extend extracted values
    """

    @staticmethod
    def as_json(payload):
        """
        Extract data from logger payload
        You can extend this class by adding resources you want to extract
        :param payload:
        """

        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["method_name"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp "],
            "resourceLocation": payload["protoPayload"]["serviceData"]["jobCompletedEvent"]
            ["job"]["jobName"]["location"],
            "resourceProjectId": payload["protoPayload"]["serviceData"]["jobCompletedEvent"]
            ["job"]["jobConfiguration"]["load"]["destinationTable"]["projectId"],
            "resourceDatasetId": payload["protoPayload"]["serviceData"]["jobCompletedEvent"]
            ["job"]["jobConfiguration"]["load"]["destinationTable"]["datasetId"],
            "resourceTableId": payload["protoPayload"]["serviceData"]["jobCompletedEvent"]
            ["job"]["jobConfiguration"]["load"]["destinationTable"]["tableId"],
            "timestamp": str(calendar.timegm(time.gmtime()))
        })
