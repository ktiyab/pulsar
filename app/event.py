import configurations as app_configs
import importlib
import base64

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class SinkTrigger(object):
    def __init__(self):
        pass

    def load(self, payload):
        """
        Execute package.module.class.function:parameters (or without parameters)
        :return: tuple
        """
        logger.info("--> event.SinkTrigger.load: Load Cloud Logging Sink trigger parameters...")

        try:
            # Extract resource type name
            resource_type = payload["resource"]["type"]

            # Build class name by using resource type name (gsc_object > GcsObject)
            # Refer to app.libs.logging.sink

            name_array = resource_type.split(app_configs.PROTO_PAYLOAD_NAME_SEP)
            class_reference = ""
            for name in name_array:
                class_reference = class_reference + name.capitalize()

            # Load module
            _module = importlib.import_module("{}.{}".format(app_configs.TRIGGER_PACKAGE_REFERENCE,
                                                             app_configs.TRIGGER_MODULE_REFERENCE)
                                              )
            # Arg
            arg = [payload]

            # Load class
            _class = getattr(_module, class_reference)

            # Load function with parameters if exist
            resource_data = getattr(_class, app_configs.TRIGGER_FUNCTION)(*arg)

            # Build job definition
            # Run path - Always based on the GCP resource name
            # gcs_object = custom.gcs_object.GcsObject.run:<resource_data>
            # Encode the resource information and decode it in the custom class
            data_bytes = resource_data.encode("utf-8")
            encoded_data_bytes = base64.b64encode(data_bytes)
            encoded_data = encoded_data_bytes.decode("utf-8")

            run = app_configs.TRIGGER_RUN.format(resource_type, class_reference, encoded_data)

            loaded_sink_job = app_configs.TRIGGER_JOB_TEMPLATE
            loaded_sink_job[app_configs.NAME_KEY] = resource_type
            loaded_sink_job[app_configs.PARAMETERS_KEY][app_configs.PARAMS_RUN_KEY] = run

            return loaded_sink_job

        except Exception as e:
            message = "event.SinkTrigger.load: Unable to execute with error " + str(e)
            logger.error("--->" + message)
            return None, message
            pass
