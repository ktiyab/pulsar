
import calendar
import json
import time

# https://cloud.google.com/logging/docs/view/query-library-preview


class GcsBucket(object):
    """
    Resource type name is "gcs_bucket" > class GcsBucket
    You can extend extracted values
    """

    @staticmethod
    def storage_objects_create(payload):

        """
        GCP methodName: storage.objects.create > function name: storage_objects_create
        Load key values as json
        :param payload:
        :return:JSON str
        """
        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["methodName"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "resourceLocation": payload["resource"]["labels"]["location"],
            "resourceProjectId": payload["resource"]["labels"]["project_id"],
            "resourceBucketName": payload["resource"]["labels"]["bucket_name"],
            "resourceName": payload["resource"]["labels"]["bucket_name"],
            "timestamp": str(calendar.timegm(time.gmtime()))
        })

    @staticmethod
    def storage_objects_delete(payload):

        """
        GCP methodName: storage.objects.delete > function name: storage_objects_delete
        Load key values as json
        :param payload:
        :return:JSON str
        """
        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["methodName"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "resourceLocation": payload["resource"]["labels"]["location"],
            "resourceProjectId": payload["resource"]["labels"]["project_id"],
            "resourceBucketName": payload["resource"]["labels"]["bucket_name"],
            "resourceName": payload["resource"]["labels"]["bucket_name"],
            "timestamp": str(calendar.timegm(time.gmtime()))
        })


class BigqueryResource(object):
    """
    Resource type name is "bigquery_table" > class BigqueryTable
    Load key values as json
    """

    @staticmethod
    def tableservice_insert(payload):

        """
        GCP methodName: storage.objects.delete > function name: storage_objects_delete
        Load key values as json
        :param payload:
        :return:JSON str
        """

        return json.dumps({
            "resourceType": payload["resource"]["type"],
            "methodName": payload["protoPayload"]["methodName"],
            "principalEmail": payload["protoPayload"]["authenticationInfo"]["principalEmail"],
            "callerIP": payload["protoPayload"]["requestMetadata"]["callerIp"],
            "project_id": payload["resource"]["labels"]["project_id"],
            "timestamp": str(calendar.timegm(time.gmtime()))
        })
