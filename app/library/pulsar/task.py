# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())

import calendar
import time
import json

import context as deployment_context
import configurations as app_configs

class Task(object):

    TASKED_STATE = "ready"
    INITIATE_STATE="runnable"
    PROCESSED_STATE="completed"
    TERMINATED_STATE="interrupted"

    def __init__(self):
        self.id = None
        self.app = deployment_context.APP_NAME
        self.service_account = deployment_context.SERVICE_ACCOUNT_EMAIL
        self.runtime = deployment_context.RUNTIME
        self.state = None
        self.notifier = None
        self.owners = None
        self.project_id = deployment_context.PROJECT_ID
        self.region = deployment_context.REGION
        self.parameters = None
        self.timestamp = str(calendar.timegm(time.gmtime()))
        self.success = False
        self.message = None

    def to_dict(self):

        return {
            "id": str(self.task_id) if self.task_id else "",
            "state": str(self.task_state) if self.task_state else "",
            "app": str(self.task_state) if self.task_state else "",
            "project_id": str(self.task_project_id) if self.task_project_id else "",
            "region": str(self.task_region) if self.task_region else "",
            "service_account": str(self.task_state) if self.task_state else "",
            "runtime": str(self.task_state) if self.task_state else "",
            "notifier": str(self.task_notifier) if self.task_notifier else "",
            "owners": str(self.task_owners) if self.task_owners else "",
            "parameters": str(self.task_parameters) if self.task_parameters else "",
            "timestamp": str(self.task_timestamp) if self.task_timestamp else "",
            "success": str(self.task_success) if self.task_success else "",
            "message": str(self.task_message) if self.task_message else ""
        }

    def to_json(self):
        task_dict = self.to_dict()
        return json.loads(task_dict)

    def update_timestamp(self):
        self.task_timestamp = str(calendar.timegm(time.gmtime()))

    def flat_parameters(self):
        self.task_parameters=json.dumps(self.task_parameters)

class Manager(object):

    def __int__(self, current_task=None):
        if current_task:
            logger.info("--> Task.Manager.init: Loading existing task...")
            self.task=current_task
        else:
            logger.info("--> Task.Manager.init: Creating new task...")
            self.task = Task()

    def clean(self):
        logger.info("--> Task.Manager.clean: Cleaning task...")
        self.task = Task()

    def load(self, run_context):
        logger.info("--> Task.Manager.load: Loading task...")

        try:
            # Load task
            self.task.id = run_context["event_id"]
            self.task.state = self.task.TASKED_STATE
            self.task.app = deployment_context.APP_NAME
            self.task.project_id = run_context["project_id"]
            self.task.region = run_context["region"]
            self.task.service_account = run_context["service_account"]
            self.task.runtime = deployment_context.RUNTIME
            self.task.notifier = run_context["data"]["notifier"]
            self.task.owners = run_context["data"]["owners"]
            self.task.parameters = run_context["data"]["parameters"]
        except Exception as e:
            logger.error("Unable to load context information with message: " + str(e))
            # TODO: We are unable to load task, send alert to admin?

        # Check if context is valid
        is_valid_context, message = self.is_valid_context(run_context)
        if not is_valid_context:
            #TODO:
            # Save declared task with error message
            # Set task state status with message
            self.task.success = is_valid_context
            self.task.message = message
            return self.task

        if run_context["data"]:
            # Check if required json data are present
            is_valid_data, message = self.is_valid_data()
            if not is_valid_data:
                self.task.success = is_valid_data
                self.task.message = message
                return self.task

        # TODO: Check notifier and send email
        # Create special class for email management

        #TODO: Check task state and send email or not
        return task
    """
    """
    def is_valid_data(self, json_data):
        """
        Check if all expected json data from user are filled
        You can extend/modify json data with the configuration.py file
        :param json_data:
        :return: tuple
        """
        logger.info("--> Task.Manager.expected_data: Check if the json contains all required keys...")
        # Check if the json contains all required keys
        required_keys = app_configs.REQUIRED_KEYS
        for key in required_keys:
            if not self.key_exist(key, json_data):
                False, "Missing required key "+key+", please provide it."
        return True, "All required keys are present."


    """
        Check context validity
    """
    def is_valid_context(self, run_context):
        """
        Run context must equal to deployment context (project_id, region, service_account)
        :param run_context: Running context of the cloud function
        :return: True or False
        """
        logger.info("--> Task.Manager.is_valid_context: Checking context validity...")

        if run_context["project_id"] != deployment_context.PROJECT_ID:
            return False, "Run context roject_id not equal to deployment project."

        if run_context["region"] != deployment_context.REGION:
            return False, "Run context region not equal to deployment region."

        if run_context["service_account_email"]!=deployment_context.SERVICE_ACCOUNT_EMAIL:
            return False, "Run context service_account not equal to deployment service_account"

        return True, "Run context equal to deployment context"

    """
    Check if key exist in json
    """
    def key_exist(self, key, json_object):
        for key_name in json_object:
            if key_name == key:
                return True

        return False
