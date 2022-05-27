# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Definitions: A "job" is a complete unit of work under execution. A job is made up of many steps or "tasks"

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

import calendar
import time
import json

import context as deployment_context
import configurations as app_configs
from  notification import Notice, Stream

class Task(object):

    TASKED_STATE = "ready"
    INITIATE_STATE="runnable"
    PROCESSED_STATE="completed"
    TERMINATED_STATE="interrupted"

    CURRENT_DATE = time.strftime("%Y%m%d", time.gmtime())

    def __init__(self):
        self.id = None
        self.app = deployment_context.APP_NAME
        self.service_account = deployment_context.SERVICE_ACCOUNT_EMAIL
        self.runtime = deployment_context.RUNTIME
        self.state = None
        self.always_notify = "false"
        self.owners = None
        self.project_id = deployment_context.PROJECT_ID
        self.region = deployment_context.REGION
        self.parameters = None
        self.acknowledge_timestamp = None
        self.processed_timestamp = None
        self.success = "true"
        self.details = ""

    def to_dict(self):

        return {
            "id": str(self.id) if self.id else "",
            "state": str(self.state) if self.state else "",
            "app": str(self.app) if self.app else "",
            "project_id": str(self.project_id) if self.project_id else "",
            "region": str(self.region) if self.region else "",
            "service_account": str(self.service_account) if self.service_account else "",
            "runtime": str(self.runtime) if self.runtime else "",
            "always_notify": str(self.always_notify) if self.always_notify else "",
            "owners": str(self.owners) if self.owners else "",
            "parameters": str(self.parameters) if self.parameters else "",
            "acknowledge_timestamp": str(self.acknowledge_timestamp) if self.acknowledge_timestamp else "",
            "processed_timestamp": str(self.processed_timestamp) if self.processed_timestamp else "",
            "success": str(self.success) if self.success else "",
            "details": str(self.details) if self.details else ""
        }

    def acknowledge(self):
        self.acknowledge_timestamp = str(calendar.timegm(time.gmtime()))

    def processed(self):
        self.processed_timestamp = str(calendar.timegm(time.gmtime()))

    def flat_parameters(self):
        self.parameters=json.dumps(self.parameters)

    def succeed(self, message):
        self.success = "True"
        self.details = self.details + message

    def failed(self, message):
        self.success = "False"
        self.state = self.TERMINATED_STATE
        self.details = self.details + message

    def message(self, message):
        self.details=message

    def to_json_str(self):
        """
        Convert object to json str
        :return: JSON str
        """
        task_dict = self.to_dict()
        return json.dumps(task_dict)

    def to_html(self):
        """
        Convert object to html
        :return: HTML str
        """

        head ='<p>'+ app_configs.JOB_EMAIL_CAPTION.format(self.app.upper()) + ' </p><ul>'
        html_value=""

        task_dict = self.to_dict()
        for key in task_dict:
            html_value = html_value + '<li>' + \
                                        '<b style="text-transform: capitalize;">' + \
                                             key.replace("_", " ") + \
                                        ':</b> ' + \
                                        str(task_dict[key]) + \
                                    '</li>'
        html_value = head + html_value + '</ul><br />'
        return html_value

    def get_table_id(self):
        return '{}_{}'.format(self.state.lower(), str(self.CURRENT_DATE))



class Job(object):

    task = Task()
    NOTICE = None
    STREAM = None

    def __init__(self, ongoing_task=None):
        if ongoing_task:
            logger.info("--> Job.Job.init: Loading existing task...")
            self.task=ongoing_task
        else:
            logger.info("--> Job.Job.init: Creating new task...")

        # Load notification client
        self.NOTICE = Notice(self.task.project_id, self.task.app)
        # Load notifier with sendgrid configs
        self.NOTICE.load_secrets()
        # Load streamer with bigquery configs -- App name is the default dataset_id
        self.STREAM = Stream(self.task.project_id, self.task.app, self.task.region)

    def clean(self):
        logger.info("--> Job.Job.clean: Cleaning task...")
        self.task = Task()

    def load(self, run_context):
        logger.info("--> Job.Job.load: Loading task...")

        try:
            self.task.acknowledge()

            # Load task
            self.task.id = run_context["event_id"]
            self.task.state = self.task.TASKED_STATE
            self.task.app = deployment_context.APP_NAME
            self.task.project_id = run_context["project_id"]
            self.task.region = run_context["region"]
            self.task.service_account = run_context["service_account"]
            self.task.runtime = deployment_context.RUNTIME

            # Check if context is valid
            is_valid_context, context_message = self.is_valid_context(run_context)

            if not is_valid_context:
                # Set task state status with message
                self.task.failed(context_message)

            # Load data if exist
            if self.task.success.lower()=="true" and self.key_exist("data", run_context):

                run_context_data = json.loads(run_context["data"])

                # Check if required json data are present
                is_valid_data, data_message = self.is_valid_data(run_context_data)

                if not is_valid_data:
                    self.task.failed(data_message)
                else:
                    self.task.always_notify = run_context_data["always_notify"]
                    self.task.owners = run_context_data["owners"]
                    self.task.parameters = run_context_data["parameters"]
            # If no error, it's loaded successfully
            if self.task.success.lower()=="true":
                self.task.succeed(app_configs.TASK_IS_LOAD.format(run_context["event_id"]))

            # Update timestamp
            self.task.processed()

        except Exception as e:
            logger.error("--> Job.Job.load: Unable to load context information with message: " + str(e))
            self.task.failed()
            self.task.details += app_configs.TASK_LOAD_FAILED.format(str(e))

        #TODO: We are unable to load task, send alert to admin?
        #TODO: Check always_notify and send email - Create dedicated class for email management
        #TODO: Check task state and send email or not
        # Notify by email and log analytic data

        self.stream_into_bigquery()
        self.notify()

        return self.task

    def is_valid_data(self, json_data):
        """
        Check if all expected json data from user are filled
        You can extend/modify json data with the configuration.py file
        :param json_data:
        :return: tuple
        """
        logger.info("--> Job.Job.is_valid_data: Check if the json contains all required keys...")
        # Check if the json contains all required keys
        required_keys = app_configs.EXPECTED_KEYS
        for key in required_keys:
            if not self.key_exist(key, json_data):
                return False, app_configs.MISSING_JSON_KEY.format(key)
        return True, app_configs.JSON_KEYS_ARE_PRESENT


    def is_valid_context(self, run_context):
        """
        Run context must equal to deployment context (project_id, region, service_account)
        :param run_context: Running context of the cloud function
        :return: True or False
        """
        logger.info("--> Job.Job.is_valid_context: Checking context validity...")

        if run_context["project_id"] != deployment_context.PROJECT_ID:
            return False, app_configs.CONTEXT_PROJECT_ID_ERROR

        if run_context["region"] != deployment_context.REGION:
            return False, app_configs.CONTEXT_REGION_ERROR

        if run_context["service_account"]!=deployment_context.SERVICE_ACCOUNT_EMAIL:
            return False, app_configs.CONTEXT_SERVICE_ACCOUNT_ERROR

        return True, app_configs.CONTEXT_IS_VALID

    def key_exist(self, key, json_object):
        """
        Check if key exist in json
        :param key:
        :param json_object:
        :return: Bool
        """
        for key_name in json_object:
            if key_name == key:
                return True

        return False


    def notify(self):
        """
        Send notification if required about job status
        :return:
        """

        logger.info("--> Job.Job.notify: Checking notification status...")
        # If users ask to always has notification (even in success)
        # or if we have a task failure, send email
        if self.task.always_notify.lower() =="true" or self.task.success.lower()=="false":
            if self.task.success.lower()=="true":
                self.NOTICE.success(self.task.to_html(), None, self.task.owners)
            else:
                self.NOTICE.failure(self.task.to_html(), None, self.task.owners)

        return True

    def stream_into_bigquery(self):
        """
        Log task status into BigQuery
        :return:
        """
        logger.info("--> Job.Job.push_into_bigquery: Stream task status into BigQuery...")
        table_id = self.task.get_table_id()
        table_data = self.task.to_dict()
        self.STREAM.into_bigquery(table_id, table_data)


