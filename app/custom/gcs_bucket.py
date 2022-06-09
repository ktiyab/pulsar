import base64
import json

# Import Pulsar custom notification system and the app context
import sys
sys.path.append("..")
import notification
import context as app_context

class GcsBucket(object):
    # Defined existing alpha codes
    ALPHA_CODE_POS = 2
    ALLOWED_COUNTRY_ALPHA_CODES = ["fr", "gb", "us", "tw"]

    # Define legal constraints - https://cloud.google.com/bigquery/docs/locations
    rules = {
        "FR": ["europe-west1", "europe-west3"],
        "GB": ["europe-west2"],
        "US": ["us-west1", "us-west3"],
        "ASIA": ["asia-east1"]
    }
    # Create custom mail template
    mailing_subject = "Compliance violation from project {}."
    mailing_html_template = "<b>Doberman</b> identify a Storage item compliance violation with following details: " \
                            " <br/><pre>{}</pre>." \
                            "<br/> Data in the project <b>{}</b> must be create in following regions <b>{}</>."
    @staticmethod
    def storage_buckets_create(payload):

        # ---- Always decode the extracted payload ----
        base64_str = payload.encode("utf-8")
        base64_bytes = base64.b64decode(base64_str)
        decode_str = base64_bytes.decode("utf-8")
        payload = json.loads(decode_str)
        # ---------------------------------------------
        # Custom Control
        # 1 - Get the country name from the project id (company-crm-fr)
        project_name_array = payload["project_id"].split("-")

        if len(project_name_array) == 3:
            # 2 - Get alpha code
            country_alpha_code = project_name_array[2]
            # 3 - If we have valid alpha-code
            if country_alpha_code in GcsBucket.ALLOWED_COUNTRY_ALPHA_CODES:
                # 4 - If current location is not in the valid location list
                if payload["location"] not in GcsBucket.rules[country_alpha_code.upper()]:
                    # Houston, we have a problem
                    subject = GcsBucket.mailing_subject.format(payload["project_id"])
                    body = GcsBucket.mailing_html_template.format(json.dumps(payload, indent=4),
                                                                         payload["project_id"],
                                                                         str(GcsBucket.rules[
                                                                                 country_alpha_code.upper()]))

                    # Load pulsar mailing system
                    notifier = notification.Notice(app_context.PROJECT_ID, app_context.APP_NAME)
                    # Load secret from secret manager
                    notifier.load_secrets()
                    # Use the failure mailing template
                    notifier.failure(body, subject)

            # Return the information for the completed table details
            return json.dumps(payload)
