# -*- coding: utf-8 -*-
# By Tiyab KONLAMBIGUE
# GCP PULSAR ALPHA - A cloud function skeleton for events based app
# mailto : tiyab@gcpbees.com | ktiyab@gmail.com


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

# Instantiates logging client
from logging import getLogger, NullHandler
logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Mailer(object):

    @staticmethod
    def send(from_email, to_emails, subject, html_content, api_key=None):

        email_list = to_emails.split('|')
        to_list = Personalization()

        for email in email_list:
            to_list.add_to(Email(email))

        html_content = Content(mime_type='text/html', content=html_content)

        message = Mail(
            from_email=from_email,
            to_emails=None,
            subject=subject)
        message.add_personalization(to_list)
        message.add_content(html_content)

        try:
            if api_key:
                sg = SendGridAPIClient(api_key)
            else:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

            response = sg.send(message)

            logger.info(response)

            return response

        except Exception as e:
            logger.error("Sendgrid.client.Mailer.Send: Unable to send mail on sendgrid with error: " + str(e))
