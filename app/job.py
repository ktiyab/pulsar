# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Definitions: A "job" is a complete unit of work under execution. A job is made up of many steps or "tasks"
import calendar
import time
import json

import context as deployment_context
import configurations as app_configs
from notification import Notice, Stream, Publish
from runner import Runner
from event import SinkTrigger

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Task(object):

    READY_STATE = app_configs.READY_STATE
    RUNNABLE_STATE = app_configs.RUNNABLE_STATE
    COMPLETED_STATE = app_configs.COMPLETED_STATE
    INTERRUPTED_STATE = app_configs.INTERRUPTED_STATE

    CURRENT_DATE = time.strftime("%Y%m%d", time.gmtime())

    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.app = deployment_context.APP_NAME
        self.service_account = deployment_context.SERVICE_ACCOUNT_EMAIL
        self.runtime = deployment_context.RUNTIME
        self.memory = deployment_context.MEMORY
        self.state = None
        self.alert_level = "false"
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
            "name": str(self.name) if self.name else "",
            "description": str(self.description) if self.description else "",
            "state": str(self.state) if self.state else "",
            "app": str(self.app) if self.app else "",
            "project_id": str(self.project_id) if self.project_id else "",
            "region": str(self.region) if self.region else "",
            "service_account": str(self.service_account) if self.service_account else "",
            "runtime": str(self.runtime) if self.runtime else "",
            "memory": str(self.memory) if self.memory else "",
            "alert_level": str(self.alert_level) if self.alert_level else "",
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
        self.parameters = json.dumps(self.parameters)

    def succeed(self, message):
        self.success = "True"
        self.details = message

    def failed(self, message):
        self.success = "False"
        self.state = self.INTERRUPTED_STATE
        self.details = message

    def message(self, message):
        self.details = message

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

        head = '<p>' + app_configs.JOB_EMAIL_CAPTION.format(self.app.upper()) + ' </p><ul>'
        html_value = ""

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

    def update(self, success, response):
        # Update task status
        self.processed()
        if success:
            self.succeed(response)
        else:
            self.failed(response)


class Job(object):

    task = Task()
    NOTICE = None
    STREAM = None

    def __init__(self, ongoing_task=None):
        if ongoing_task:
            logger.info("--> job.Job.init: Loading existing task...")
            self.task = ongoing_task
        else:
            logger.info("--> job.Job.init: Creating new task...")

        # Load notification client
        self.NOTICE = Notice(self.task.project_id, self.task.app)
        # Load notifier with sendgrid configs
        self.NOTICE.load_secrets()
        # Load streamer with bigquery configs -- App name is the default dataset_id
        self.STREAM = Stream(self.task.project_id, self.task.app, self.task.region)

    def clean(self):
        logger.info("--> job.Job.clean: Cleaning task...")
        self.task = Task()

    # -------------- 1 - VALIDATE & LOAD TASK PARAMETERS ----------------------------------------
    def load(self, run_context):
        logger.info("--> job.Job.load: Loading task...")

        try:
            self.task.acknowledge()

            # Load task
            self.task.id = run_context[app_configs.EVENT_ID_KEY]
            self.task.state = self.task.READY_STATE
            self.task.app = deployment_context.APP_NAME
            self.task.project_id = run_context[app_configs.PROJECT_ID_KEY]
            self.task.region = run_context[app_configs.REGION_KEY]
            self.task.service_account = run_context[app_configs.SERVICE_ACCOUNT_KEY]
            self.task.runtime = deployment_context.RUNTIME
            self.task.memory = deployment_context.MEMORY

            # Check if context (allowed Project and region) is valid
            is_valid_context, check_context_message = self.is_valid_context(run_context)

            if not is_valid_context:
                # Set task state status with message
                self.task.failed(check_context_message)

            # Load data if exist
            if self.task.success.lower() == "true" and self.key_exist(app_configs.DATA_KEY, run_context):

                # Check if required json data are present
                is_valid_data, check_data_message = self.is_valid_data(run_context[app_configs.DATA_KEY])

                if not is_valid_data:
                    self.task.failed(check_data_message)
                else:
                    # Check parameters validity
                    is_valid_parameters, check_parameters_message = self.is_allowed_parameters(
                        run_context[app_configs.DATA_KEY][app_configs.PARAMETERS_KEY]
                    )
                    if not is_valid_parameters:
                        self.task.failed(check_parameters_message)
                    else:
                        # Load user payload information - Refer to configurations.py > Json control keys
                        self.task.name = run_context[app_configs.DATA_KEY][app_configs.NAME_KEY]
                        self.task.description = run_context[app_configs.DATA_KEY][app_configs.DESCRIPTION_KEY]
                        self.task.alert_level = run_context[app_configs.DATA_KEY][app_configs.ALERT_LEVEL_KEY]
                        self.task.owners = run_context[app_configs.DATA_KEY][app_configs.OWNERS_KEY]
                        self.task.parameters = run_context[app_configs.DATA_KEY][app_configs.PARAMETERS_KEY]

            # If no error, it's loaded successfully
            if self.task.success.lower() == "true":
                self.task.update(True, app_configs.TASK_IS_LOAD.format(run_context[app_configs.EVENT_ID_KEY]))

        except Exception as e:
            logger.error("--> job.Job.load: Unable to load context information with message: " + str(e))
            self.task.update(False, app_configs.TASK_LOAD_FAILED.format(str(e)))
            return False, None
        finally:
            pass

        # Stream and notify
        self.broadcast()

        return True, self.task

    def is_valid_data(self, json_data):
        """
        Check if all expected json data from user are filled
        You can extend/modify EXPECTED_KEYS array in the configuration.py file
        :param json_data:
        :return: tuple
        """
        logger.info("--> job.Job.is_valid_data: Check if the json contains all required keys...")
        # Check if the json contains all required keys
        required_keys = app_configs.EXPECTED_KEYS
        for key in required_keys:
            if not self.key_exist(key, json_data):
                return False, app_configs.MISSING_JSON_KEY.format(key)
        return True, app_configs.JSON_KEYS_ARE_PRESENT

    def is_allowed_parameters(self, parameters):
        """
        Check if parameter keys are allowed
        You can extend/modify ALLOWED_PARAMETERS_KEYS array in the configuration.py file
        :param parameters:
        :return:
        """
        logger.info("--> job.Job.is_allowed_parameters: Check if the json parameters contains allowed keys...")

        allowed_keys = app_configs.ALLOWED_PARAMETERS_KEYS
        for key in parameters:
            if key not in allowed_keys:
                return False, app_configs.NOT_ALLOWED_JSON_KEY
        return True, app_configs.KEYS_ARE_ALLOWED

    def is_valid_context(self, run_context):
        """
        Run context must equal to deployment context (project_id, region, service_account)
        :param run_context: Running context of the cloud function
        :return: True or False
        """
        logger.info("--> job.Job.is_valid_context: Checking context validity...")

        if run_context[app_configs.PROJECT_ID_KEY] != deployment_context.PROJECT_ID:
            return False, app_configs.CONTEXT_PROJECT_ID_ERROR

        if run_context[app_configs.REGION_KEY] != deployment_context.REGION:
            return False, app_configs.CONTEXT_REGION_ERROR

        if run_context[app_configs.SERVICE_ACCOUNT_KEY] != deployment_context.SERVICE_ACCOUNT_EMAIL:
            return False, app_configs.CONTEXT_SERVICE_ACCOUNT_ERROR

        return True, app_configs.CONTEXT_IS_VALID

    # -------------- 2 - CHECK IF TASK IS RUNNABLE ----------------------------------------

    def is_runnable(self):
        """
        Check if job task is runnable
        :return:
        """
        logger.info("--> job.Job.is_runnable: Check if task is runnable...")

        try:
            # Update task state
            self.task.acknowledge()
            self.task.state = self.task.RUNNABLE_STATE

            # Try to load task parameters
            runner = Runner()
            success, response = runner.load(self.task.parameters)

            # Update task status
            self.task.update(success, response)

        except Exception as e:
            logger.error("--> job.Job.is_runnable: The task is not runnable with message : " + str(e))
            self.task.update(False, app_configs.TASK_NOT_RUNNABLE.format(str(e)))
            return False, None
        finally:
            pass

        # Stream and notify
        self.broadcast()

        return True, self.task

    # -------------- 3 - RUN TASK ----------------------------------------
    def run(self):
        """
        Run a task
        :return: task
        """
        logger.info("--> job.Job.run: Running a task...")

        try:
            # Update task state
            self.task.acknowledge()
            self.task.state = self.task.COMPLETED_STATE

            # Try to execute task parameters
            runner = Runner()
            success, response = runner.execute(self.task.parameters)

            # Update task status
            self.task.update(success, response)

        except Exception as e:
            logger.error("--> job.Job.is_runnable: The task is not runnable with message : " + str(e))
            self.task.update(False, app_configs.TASK_NOT_RUNNABLE.format(str(e)))
            return False, None
        finally:
            pass

        # Stream and notify
        self.broadcast()

        return True, self.task

    # -------------- 4 - Load proto-payload ----------------------------------------

    def load_proto_payload(self, proto_payload, gcp_context, event_id):
        """
        Run proto-payload task data load
        :return: task
        """
        logger.info("--> job.Job.load_proto_payload: Running proto-payload task load...")
        self.task.acknowledge()
        try:
            sink = SinkTrigger()
            success, data = sink.load(proto_payload)
        except Exception as e:
            logger.error("--> job.Job.is_runnable: The task is not runnable with message : " + str(e))
            success = False
            data = str(e)
        finally:
            pass

        # If proto-payload load failed
        if not success:
            # Update task details and status for tracing
            self.task.id = event_id
            self.task.processed()
            self.task.name = app_configs.TRIGGERED_FROM
            self.task.alert_level = app_configs.DEFAULT_ALERT_LEVEL
            self.task.description = app_configs.TRIGGERED_DESCRIPTION
            self.task.app = deployment_context.APP_NAME
            self.task.runtime = deployment_context.RUNTIME
            self.task.memory = deployment_context.MEMORY
            self.task.project_id = gcp_context[app_configs.PROJECT_ID_KEY]
            self.task.region = gcp_context[app_configs.REGION_KEY]
            self.task.service_account = gcp_context[app_configs.SERVICE_ACCOUNT_KEY]
            self.task.parameters = json.dumps(proto_payload)
            self.task.update(False, app_configs.TASK_NOT_RUNNABLE.format(data))

            # Stream and notify
            self.broadcast()

        return success, data

    # -------------- 5 - Forward task response -------------------------------------

    def forward(self):
        """
        Forward task response
        :return: task
        """
        logger.info("--> job.Job.forward: Forward a task response if set...")

        try:

            # Check if forwarding is set
            params = self.task.parameters

            if self.key_exist(app_configs.PARAMS_RESPONSE_TO_KEY, params):

                call_params = self.get_topic_call_params(params[app_configs.PARAMS_RESPONSE_TO_KEY])

                if call_params:
                    publish = Publish(call_params[app_configs.PROJECT_ID_KEY], call_params[app_configs.TOPIC_KEY])

                    message_string = json.dumps(call_params[app_configs.TOPIC_MESSAGE_KEY])
                    data_encoded = message_string.encode("utf-8")

                    publish.into_pubsub(data_encoded)

                    return True, "Message forwarded"
                else:
                    return False, None
            else:
                return False, None
        except Exception as e:
            message = "--> job.Job.forward: The forwarding failed with message : " + str(e)
            logger.error(message)
            # Stream and notify
            self.broadcast()
            self.job_failure(message)
            pass
            return False, None

    def get_topic_call_params(self, full_topic_params):
        params = {}
        full_topic_array = full_topic_params.split(app_configs.TOPIC_PROJECT_SEP)

        if len(full_topic_array) == 2:
            # Extract project_id and topic_name
            params[app_configs.PROJECT_ID_KEY] = full_topic_array[0].split(app_configs.MODULE_SEPARATOR)[0]
            params[app_configs.TOPIC_KEY] = full_topic_array[0].split(app_configs.MODULE_SEPARATOR)[1]

            full_response = None
            # Set response if placeholder is set
            if app_configs.PLACE_HOLDER in str(full_topic_array[1]):
                full_response = str(full_topic_array[1]).format(self.task.details)

            # Check if response must be consumed by a pulsar_topic
            # If yes build job params
            if app_configs.CUSTOM_PACKAGE in full_response:
                job_to_forward = app_configs.JOB_TEMPLATE

                # Set configs default name and description
                job_to_forward[app_configs.NAME_KEY] = self.task.name + app_configs.FORWARD_NAME
                job_to_forward[app_configs.DESCRIPTION_KEY] = app_configs.FORWARD_DESCRIPTION

                # Use principal jobs configs
                job_to_forward[app_configs.ALERT_LEVEL_KEY] = self.task.alert_level
                job_to_forward[app_configs.OWNERS_KEY] = self.task.owners

                # Load run parameters
                job_to_forward[app_configs.PARAMETERS_KEY][app_configs.PARAMS_RUN_KEY] = full_response
                # Set default from
                job_to_forward[app_configs.PARAMETERS_KEY][app_configs.PARAMS_FROM_KEY] = app_configs.FORWARD_FROM

                # Override full response with job to forward definition
                full_response = job_to_forward

            params[app_configs.TOPIC_MESSAGE_KEY] = full_response

            return params
        else:
            return None

    # -------------- 6 - Failed job response -------------------------------------
    def job_failure(self, message="Unknown failure"):
        logger.error("--> job.Job.failed: The task failed with message : " + str(message))
        self.task.failed(message)

        # Stream and notify
        self.broadcast()

    # -------------- UTILS ----------------------------------------

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
        Notification level are:
        - 0 : Only failures
        - 1 : Only completed tasks
        - 2 : All task states
        :return:
        """

        logger.info("--> job.Job.notify: Checking notification status...")
        # If alert level is 1 or 2
        # or if we have a task failure, send email
        if self.task.alert_level.lower() in app_configs.SEND_ALERT_LEVELS \
                or self.task.success.lower() == "false":

            # If task succeeded
            if self.task.success.lower() == "true":
                # If alert level is 1 and task is at the completed state (Alert only on task complete)
                # or if alert level is 2 (alert at any success state)
                if (self.task.alert_level == "1" and self.task.state == app_configs.COMPLETED_STATE) \
                        or (self.task.alert_level == "2"):

                    self.NOTICE.success(self.task.to_html(), None, self.task.owners)
            else:
                # If task failed
                self.NOTICE.failure(self.task.to_html(), None, self.task.owners)

        return True

    def stream_into_bigquery(self):
        """
        Log task status into BigQuery
        :return:
        """
        logger.info("--> job.Job.push_into_bigquery: Stream task status into BigQuery...")
        table_id = self.task.get_table_id()
        table_data = self.task.to_dict()
        self.STREAM.into_bigquery(table_id, table_data)

        return True

    def broadcast(self):
        # Stream and notify
        self.stream_into_bigquery()
        self.notify()
