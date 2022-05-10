variable "PROJECT_ID" {
  type = string
  description = "The GCP project ID"
  default = "<YOUR-PROJECT-ID>"
}

variable "SERVICE_ACCOUNT_EMAIL" {
  type = string
  description = "The dedicated service account for the framework. The service account must have authorization on services"
  default = "<YOUR-SERVICE-ACCOUNT-EMAIL>"
}

variable "PULSAR_BUCKET_NAME" {
  type = string
  description = "The pulsar bucket name which is the concatenation of project ID and PULSAR_BUCKET_ID_SUFFIX"
  default ="<YOUR-GENERATED-BUCKET-NAME>"
}

variable "PULSAR_NAME" {
  type = string
  description = "The name of the Cloud function in local folder and in GCP"
  default = "pulsar"

  validation {
    condition = length(var.PULSAR_NAME) > 4
    error_message = "Please provide a valid value for the Cloud Function name (length>4)."
  }
}

variable "PULSAR_ZIP" {
  type = string
  description = "The name of the local zip of the Cloud Function and in the Cloud Storage"
  default = "pulsar.zip"

  validation {
    condition = length(var.PULSAR_ZIP) > 8 && substr(var.PULSAR_ZIP, -4, -1)==".zip"
    error_message = "Please provide a valid value for the Cloud Function zip file (xxxx.zip)."
  }
}

# Cloud Function 2nd Gen is available in only few regions https://cloud.google.com/functions/docs/2nd-gen/overview
# For the GDPR we'll lock our regions on EU ones
variable "PULSAR_REGION" {
  type = string
  description = "The region in which the Cloud Function will be deployed"
  default = "europe-west1"

  validation {
    condition = length(var.PULSAR_REGION)==12 && substr(var.PULSAR_REGION, 0, 11)=="europe-west"
    error_message = "Please provide a valid value for the Cloud Function region (europe-westx)."
  }
}

variable "PULSAR_ENTRY_POINT" {
  type = string
  description = "The Cloud Function entry point"
  default = "pulse"

  validation {
    condition = length(var.PULSAR_ENTRY_POINT) > 4
    error_message = "Please provide a valid value for the Cloud Function name (length>4)."
  }
}

# Memory must be >= to 256
variable "PULSAR_MEMORY" {
  type = string
  description = "The Cloud Function memory"
  default = "512M"

  validation {
    condition = length(var.PULSAR_MEMORY) >= 4
    error_message = "Please provide a valid memory value (256M, 512M, 1024M)."
  }
}

variable "PULSAR_RUNTIME" {
  type = string
  description = "The Cloud Function runtime language version"
  default = "python39"

  validation {
    condition = substr(var.PULSAR_RUNTIME, 0, 6)=="python"
    error_message = "Please provide a valid runtime version (python38 or python39)."
  }
}

# Please check pricing https://cloud.google.com/functions/pricing
# By default 10min (600000 ms)
# Cost for 512MB per run = 0,000000925*600000/100 = $0.00555
# Max run time of a CF 2nd Gen is 1h but we don't want to exceed 10min
variable "PULSAR_TIMEOUT" {
  type = number
  description = "The maximum run time of the Cloud Function"
  default = 540

  validation {
    condition = var.PULSAR_TIMEOUT <=600
    error_message = "Please provide a valid timeout value."
  }
}

variable "PULSAR_MIN_INSTANCE" {
  type = number
  description = "The min cloud function up, allowing to avoid cold starts"
  default = 0

  validation {
    condition = var.PULSAR_MIN_INSTANCE>=0
    error_message = "Please provide a valid minimum instance value (x>=0)."
  }
}

variable "PULSAR_MAX_INSTANCE" {
  type = number
  description = "The max cloud function running simultaneously, allowing to avoid overconsumption of resources"
  default = 100

  validation {
    condition = var.PULSAR_MAX_INSTANCE>0
    error_message = "Please provide a valid maximum instance value (x>=0)."
  }
}

# Topic name must start with Pulsar allowing to identify topic
variable "PULSAR_TOPIC" {
  type = string
  description = "The name of the topic dedicated to the Cloud Function"
  default = "pulsar-topic"

  validation {
    condition = length(var.PULSAR_TOPIC)>0
    error_message = "Please provide a valid name for topic (PULSAR_NAME-topic)."
  }
}

variable "PULSAR_BUCKET_ID_SUFFIX" {
  type = string
  description = "The suffix of the pulsar bucket name. The prefix must be the GCP project name"
  default = "-pulsar"
}

variable "PULSAR_SECRETS_FOLDER" {
  type = string
  description = "Local folder containing secret files"
  default ="secrets"
}

variable "PULSAR_SECRETS_EXT" {
  type = string
  description = "Secret files extension"
  default = ".json"
}