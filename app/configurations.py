
# Global variable for sendgrid and secret manager
SENDGRID_SECRET_ID="pulsar_sendgrid:latest"
SENDGRID_API_KEY=""
SENDGRID_API_KEY_NAME="pulsar_sendgrid_key"
DEFAULT_MAIL_TO=""
DEFAULT_MAIL_TO_KEY_NAME="default_mail_to"
MAIL_FROM=""
MAIL_FROM_KEY_NAME="mail_from"

# Input json expected keys
EXPECTED_KEYS=["always_notify", "owners", "parameters"]

# Error messages
CONTEXT_PROJECT_ID_ERROR="Run context project_id not equal to deployment project."
CONTEXT_REGION_ERROR="Run context region not equal to deployment region."
CONTEXT_SERVICE_ACCOUNT_ERROR="Run context service_account not equal to deployment service_account."

TASK_LOAD_FAILED="Unable to load context information with message: {}"

MISSING_JSON_KEY="Missing required key < {} >, please provide it."
JSON_KEYS_ARE_PRESENT="All required keys are present."

# Success messages
CONTEXT_IS_VALID="Run context equal to deployment context"
TASK_IS_LOAD="Task ID {} is load successfully."

# Emailing
JOB_EMAIL_CAPTION="{} job status: "
DEFAULT_SUCCESS_SUBJECT="GCP project {} - {} job success"
DEFAULT_FAILURE_SUBJECT="GCP project {} - {} job failure"
SUCCESS_COLOR="#71C105"
FAILURE_COLOR="#E42827"
HEADER_COLOR="#9428FF"
DEFAULT_EMAIL_TEMPLATE_PATH="/template/mail_template.html"