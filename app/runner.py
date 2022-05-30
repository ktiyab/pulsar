# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

# Definitions: The runner is a wrapper allowing to run existing class and function by using
# the string definition
import configurations as app_configs
import importlib

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Runner(object):

    PACKAGE_REFERENCE = None
    MODULE_REFERENCE = None
    CLASS_REFERENCE = None
    FUNCTION_REFERENCE = None
    FUNCTION_PARAMETERS = None

    def __init__(self):
        pass

    def load(self, parameters):
        """
        Load running parameters in format: package.module.class.function:,Param1,Param2...
        :param parameters:
        :return: Bool
        """
        try:
            if parameters:
                # Check if run definition is set and load it
                if self.key_exist(app_configs.RUN_KEY, parameters):

                    run_definition = parameters[app_configs.RUN_KEY]

                    # Check if class definition is set and load it
                    if app_configs.MODULE_SEPARATOR in run_definition:
                        run_references = run_definition.split(app_configs.MODULE_SEPARATOR)

                        self.PACKAGE_REFERENCE = run_references[0]
                        self.MODULE_REFERENCE = run_references[1]
                        self.CLASS_REFERENCE = run_references[2]

                        full_function_references = run_references[3]
                        if app_configs.PARAMETERS_SEPARATOR in full_function_references:
                            self.FUNCTION_REFERENCE = full_function_references.split(app_configs.PARAMETERS_SEPARATOR)[0]
                            function_parameters = full_function_references.split(app_configs.PARAMETERS_SEPARATOR)[1]
                            self.FUNCTION_PARAMETERS = function_parameters.split(app_configs.VARIABLES_SEPARATOR)
                        else:
                            self.FUNCTION_REFERENCE = full_function_references

                    return True, "The task parameters are loaded correctly."

        except Exception as e:
            message = "runner.Runner.load: Unable to load the task parameters with error " + str(e)
            logger.error("--> " + message)
            return False, message
        finally:
            pass

    def execute(self, parameters=None):
        """
        Execute package.module.class.function:parameters (or without parameters)
        :return: tuple
        """
        try:
            if parameters:
                self.load(parameters)

            # Load module
            _module = importlib.import_module("{}.{}".format(self.PACKAGE_REFERENCE, self.MODULE_REFERENCE))

            # Load class
            _class = getattr(_module, self.CLASS_REFERENCE)

            # Load function with parameters if exist
            if self.FUNCTION_PARAMETERS:
                args = self.FUNCTION_PARAMETERS
                response = getattr(_class, self.FUNCTION_REFERENCE)(*args)
            else:
                response = getattr(_class, self.FUNCTION_REFERENCE)

            return True, response

        except Exception as e:
            message = "runner.Runner.execute: Unable to execute with error " + str(e)
            logger.error("--->" + message)
            return False, message
            pass

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
