# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com

from google.cloud import pubsub_v1

class PubSubClient(object):

    def __init__(self, project_id):
        self.project_id = project_id
        self.publisher_client = pubsub_v1.PublisherClient()

    def publish(self, data, topic_name):
        topic_path = self.publisher_client.topic_path(self.project_id, topic_name)
        self.publisher_client.publish(topic=topic_path, data=data)
