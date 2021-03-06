# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# -- Definitions: Notification purpose is to alert via email

from bs4 import BeautifulSoup
import json
import os
import configurations as app_configs
from libs.gcp.sendgrid import client as sendgrid_client
from libs.gcp.secret_manager import client as secretmanager
from libs.gcp.bigquery import client as bigquery
from libs.gcp.pubsub import client as pubsub

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Load mailing template
dir_path = os.path.dirname(os.path.realpath(__file__))
DEFAULT_EMAIL_TEMPLATE_PATH = dir_path + app_configs.DEFAULT_EMAIL_TEMPLATE_PATH


class Notice(object):

    PROJECT_ID = None
    APP_NAME = ""
    MAILING_CLIENT = None

    def __init__(self, project_id, app_name=None):
        self.PROJECT_ID = project_id
        self.APP_NAME = app_name
        self.MAILING_CLIENT = sendgrid_client.Mailer()

    def load_secrets(self):

        try:

            logger.info("--> notification.Notice.load_secrets: Loading app secret from GCP.")
            project_secrets = secretmanager.SecretManagerClient(self.PROJECT_ID)

            # Load Sendgrid configs
            sendgrid_json_string = project_secrets.get_secret_by_project(app_configs.SENDGRID_SECRET_ID)
            sendgrid_json_object = json.loads(sendgrid_json_string)

            app_configs.SENDGRID_API_KEY = sendgrid_json_object[app_configs.SENDGRID_API_KEY_NAME]
            app_configs.DEFAULT_MAIL_TO = sendgrid_json_object[app_configs.DEFAULT_MAIL_TO_KEY_NAME]
            app_configs.MAIL_FROM = sendgrid_json_object[app_configs.MAIL_FROM_KEY_NAME]
            return True

        except Exception as e:
            logger.error("--> notification.Notice.load_secrets: Unable to load secret with message: " + str(e))

    def success(self, body, subject=None, mailing_list=None):
        logger.info("--> notification.Notice.success: Creating success email.")

        try:

            # Load default info if not provided
            if not mailing_list:
                mailing_list = app_configs.DEFAULT_MAIL_TO

            if not subject:
                subject = app_configs.DEFAULT_SUCCESS_SUBJECT.format(self.PROJECT_ID, self.APP_NAME)

            templating_body = self.build_template(subject, body, True)

            self.MAILING_CLIENT.send(app_configs.MAIL_FROM, mailing_list, subject,
                                     templating_body, app_configs.SENDGRID_API_KEY)

            return True

        except Exception as e:
            logger.error("--> notification.Notice.success: Unable to send success message with message: " + str(e))

    def failure(self, body, subject=None, mailing_list=None):
        logger.info("-->notification.Notice.failure: Creating failure email.")

        try:
            # Load default info if not provided
            if not mailing_list:
                mailing_list = app_configs.DEFAULT_MAIL_TO

            if not subject:
                subject = app_configs.DEFAULT_FAILURE_SUBJECT.format(self.PROJECT_ID, self.APP_NAME)

            templating_body = self.build_template(subject, body, False)

            self.MAILING_CLIENT.send(app_configs.MAIL_FROM, mailing_list,
                                     subject, templating_body, app_configs.SENDGRID_API_KEY)

            return True

        except Exception as e:
            logger.error("--> notification.Notice.success: Unable to send failure message with message: " + str(e))

    def build_template(self, title, message, success=False):
        logger.info("---> notification.Notice.build_template: Building mail template")
        if success:
            color = app_configs.SUCCESS_COLOR
        else:
            color = app_configs.FAILURE_COLOR

        with open(DEFAULT_EMAIL_TEMPLATE_PATH) as inf:
            txt = inf.read()
            template = BeautifulSoup(txt, "html.parser")

        if template:
            return template.decode().replace("%%DETAILS%%", str(title)) \
                .replace("%%HEADER_COLOR%%", app_configs.HEADER_COLOR) \
                .replace("%%MESSAGE%%", message) \
                .replace("%%STATUS%%", color)

        else:
            return message


class Stream(object):

    PROJECT_ID = None
    DATASET_ID = None
    LOCATION = None

    def __init__(self, project_id, dataset_id, location):
        self.PROJECT_ID = project_id
        self.DATASET_ID = dataset_id
        self.LOCATION = location

    def into_bigquery(self, table_id, json_data_object):
        """
        Stream data into BigQuery
        :param table_id:
        :param json_data_object:
        :return: None
        """
        project_bigquery = bigquery.BigQueryClient(self.PROJECT_ID, self.LOCATION)
        project_bigquery.stream_into_table(self.PROJECT_ID, self.DATASET_ID, self.LOCATION,
                                           table_id, json_data_object)


class Publish(object):

    PROJECT_ID = None
    TOPIC_NAME = None

    def __init__(self, project_id, topic_name):
        self.PROJECT_ID = project_id
        self.TOPIC_NAME = topic_name

    def into_pubsub(self, message):
        project_pubsub = pubsub.PubSubClient(self.PROJECT_ID)
        project_pubsub.publish(message, self.TOPIC_NAME)
