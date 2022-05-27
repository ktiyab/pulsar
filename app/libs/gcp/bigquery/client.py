# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

from google.cloud import bigquery
import google.cloud.logging
from . import schema_builder
import logging
import time

# Instantiates a client
logging_client = google.cloud.logging.Client()
# Connects the logger to the root logging handler; by default this captures
# all logs at INFO level and higher
logging.basicConfig()
logger = logging.getLogger('logger')

# Waiting after fresh table creation
SLEEP_AFTER_TABLE_CREATION = 5


class BigQueryClient(object):

    def __init__(self, project_id, location):
        # Create the BigQuery client.
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id, location=location)

    def stream_into_table(self, project_id, dataset_id, location, table_id, json_data_object):
        """
        Stream data into BigQuery
        :param project_id:
        :param dataset_id:
        :param location:
        :param table_id:
        :param json_data_object:
        :return: Bool
        """
        logger.info("--> libs.gcp.bigquery.client.BigQueryClient.push_into_table: Pushing data into table.")

        try:
            # Create dataset if not exist
            dataset_reference = bigquery.DatasetReference(project_id, dataset_id)
            if not self._dataset_exists(dataset_reference):
                dataset = bigquery.Dataset(dataset_reference)
                self.bq_client.create_dataset(dataset, timeout=30)
                logger.info("--> libs.gcp.bigquery.client.BigQueryClient.create_dataset:Created dataset {} "
                            .format(self.bq_client.project, dataset_reference.dataset_id))

            # Generate schema on the fly
            my_schema_builder = schema_builder.SchemaBuilder()
            json_schema_object = my_schema_builder.from_json_simple_object(json_data_object)

            # Create table if not exist
            table_reference = bigquery.TableReference(dataset_reference, table_id)
            table = bigquery.Table(table_reference, schema=json_schema_object)

            if not self._table_exists(table_reference):
                self.bq_client.create_table(table)
                time.sleep(SLEEP_AFTER_TABLE_CREATION)

            # Stream data into BigQuery
            self.bq_client.insert_rows_json(table=table_reference, json_rows=[json_data_object])

            return True

        except Exception as e:
            logger.info('--->libs.gcp.client.BigQueryClient.push_into_table: Unable to push into table '
                        ' {}.{}.{} in location with error {}'
                        .format(project_id, dataset_id, table_id, location, str(e))
                        )
            logger.error(str(e))
            return False
        finally:
            return False
            pass

    def _dataset_exists(self, dataset_reference):
        """
        Check if dataset exist
        :param dataset_reference:
        :return: Bool
        """
        try:
            self.bq_client.get_dataset(dataset_reference)
            return True
        except Exception as e:
            logger.error('--->libs.gcp.client.BigQueryClient._dataset_exists:'
                         ' Unable to find dataset ' + str(e))
            return False

    def _table_exists(self, table_reference):
        """
        Check if table existence
        :param table_reference:
        :return: Bool
        """
        try:
            self.bq_client.get_table(table_reference)
            return True
        except Exception as e:
            logger.error('--->libs.gcp.client.BigQueryClient._table_exists:'
                         ' Unable to find table ' + str(e))
            return False
