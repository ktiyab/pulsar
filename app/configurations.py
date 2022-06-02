# Global variable for sendgrid and secret manager
SENDGRID_SECRET_ID = "pulsar_sendgrid:latest"
SENDGRID_API_KEY = ""
SENDGRID_API_KEY_NAME = "key"
DEFAULT_MAIL_TO = ""
DEFAULT_MAIL_TO_KEY_NAME = "default_to"
MAIL_FROM = ""
MAIL_FROM_KEY_NAME = "from"

# GCP context
GCP_PROJECT_ID = ""
APP_NAME = ""

# Input json expected keys
EXPECTED_KEYS = ["name", "always_notify", "owners", "parameters"]
ALLOWED_PARAMETERS_KEYS = ["from", "run", "response_to"]

# Error messages
CONTEXT_PROJECT_ID_ERROR = "Run context project_id not equal to deployment project."
CONTEXT_REGION_ERROR = "Run context region not equal to deployment region."
CONTEXT_SERVICE_ACCOUNT_ERROR = "Run context service_account not equal to deployment service_account."

TASK_LOAD_FAILED = "Unable to load context information with message: {}"
TASK_NOT_RUNNABLE = "The task is not runnable with message: {}"

# Json control
MISSING_JSON_KEY = "Missing required key < {} >, please provide it."
JSON_KEYS_ARE_PRESENT = "All required keys are present."
NOT_ALLOWED_JSON_KEY = "Found key < {} > which is not allowed, please correct it or update configuration."
KEYS_ARE_ALLOWED = "All keys are allowed."

# Json Keys
ENV_GCP_PROJECT = "GCP_PROJECT"
ENV_FUNCTION_REGION = "FUNCTION_REGION"
ENV_FUNCTION_IDENTITY = "FUNCTION_IDENTITY"

SCHEDULER = "scheduler"
PROTO_PAYLOAD = "protoPayload"
TRIGGER_TYPE = "trigger_type"
RESOURCE_TYPE_SEP = "_"
PROTO_PAYLOAD_NAME_SEP = "."
FUNCTION_NAME_SEP = "_"

PROTO_PAYLOAD_RESOURCE = "resource"
PROTO_PAYLOAD_TYPE = "type"

PROJECT_ID_KEY = "project_id"
REGION_KEY = "region"
SERVICE_ACCOUNT_KEY = "service_account"

# Level 1 of the JSON
EVENT_ID_KEY = "event_id"
DATA_KEY = "data"

# Level 2 of the JSON
NAME_KEY = "name"
DESCRIPTION_KEY = "description"
NOTIFICATION_KEY = "always_notify"
OWNERS_KEY = "owners"
PARAMETERS_KEY = "parameters"

# Level 3 of the JSON
PARAMS_FROM_KEY = "from"
PARAMS_RUN_KEY = "run"
PARAMS_RESPONSE_TO_KEY = "response_to"

# Task states
READY_STATE = "ready"
RUNNABLE_STATE = "runnable"
COMPLETED_STATE = "completed"
INTERRUPTED_STATE = "interrupted"


# Success messages
CONTEXT_IS_VALID = "Run context equal to deployment context"
TASK_IS_LOAD = "Task ID {} is load successfully."

# Emailing
JOB_EMAIL_CAPTION = "{} job status: "
DEFAULT_SUCCESS_SUBJECT = "GCP project {} - {} job success"
DEFAULT_FAILURE_SUBJECT = "GCP project {} - {} job failure"
SUCCESS_COLOR = "#71C105"
FAILURE_COLOR = "#E42827"
HEADER_COLOR = "#9428FF"
DEFAULT_EMAIL_TEMPLATE_PATH = "/template/mail_template.html"

# Metadata paths
INTERNAL_BASE_URL = "http://metadata.google.internal/computeMetadata/v1/"
INTERNAL_PROJECT_INFO = INTERNAL_BASE_URL + "project/project-id"
INTERNAL_REGION_INFO = INTERNAL_BASE_URL + "instance/region"
INTERNAL_SERVICE_ACCOUNT_INFO = INTERNAL_BASE_URL + "instance/service-accounts/default/email"

# Class Runner
RUN_KEY = "run"
MODULE_SEPARATOR = "."
PARAMETERS_SEPARATOR = ":"
VARIABLES_SEPARATOR = ","

# Trigger resource loader
# Refer libs.gcp.logging.sink and app.event
TRIGGER_PACKAGE_REFERENCE = "libs.gcp.logging"
TRIGGER_MODULE_REFERENCE = "sink"

TRIGGER_RUN = "custom.{}.{}.{}:{}"
TRIGGER_JOB_TEMPLATE = {
    "name": "",
    "description": "Triggered job",
    "always_notify": "true",
    "owners": "",
    "parameters": {
        "from": "Logging_sink",
        "run": "",
        "response_to": "None"
    }
}
