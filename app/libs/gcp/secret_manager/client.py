# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Import the Secret Manager client library.
from google.cloud import secretmanager

class SecretManagerClient(object):

    SEPARATOR=":"

    def __init__(self, project_id=None):
        # Create the Secret Manager client.
        self.project_id = project_id
        self.sm_client = secretmanager.SecretManagerServiceClient()


    def get_secret_text(self, secret_name, secret_version="latest"):
        client = secretmanager.SecretManagerServiceClient()
        name = self.sm_client.secret_version_path(self.project_id, secret_name, str(secret_version))
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def get_secret_by_project(self, secret_name_n_version):
        if self.project_id is None:
            print("[!] Warning please set the Project ID on init ")
            return None

        return self.get_secret(secret_name_n_version)


    def get_secret(self, secret_name_n_version):
        # Extract secret name and version separated by :
        secret_name_info = secret_name_n_version.split(":")
        return self.get_secret_text(secret_name_info[0], secret_name_info[1])