# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com


import ast


class SchemaBuilder(object):

    default_str_schema = {
        "mode": "NULLABLE",
        "type": "STRING"
    }
    default_dict_schema = {
        "fields": [
        ],
        "mode": "NULLABLE",
        "name": "placeholder",
        "type": "RECORD"
    }

    # Generate BigQuery schema from json object
    def from_json_simple_object(self, json_object):

        final_schema = []

        for (k, v) in json_object.items():

            if isinstance(v, dict):
                value = self.get_line_object_schema(v, k)
            else:
                value = self.get_line_simple_schema(k)

            if k not in final_schema:
                final_schema.append(ast.literal_eval(str(value)))
        return final_schema

    # Generate schema for simple value
    def get_line_simple_schema(self, key):

        line_schema = self.default_str_schema
        line_schema["name"] = key
        return line_schema

    # Generate schema for object
    def get_line_object_schema(self, value, key):

        field = []
        dict_schema = self.default_dict_schema
        dict_schema["name"] = key

        for (key, value) in value.items():
            line_schema = self.get_line_simple_schema(key)
            field.append(ast.literal_eval(str(line_schema)))

        dict_schema["fields"] = ast.literal_eval(str(field))

        return dict_schema
