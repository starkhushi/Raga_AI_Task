import logging
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    SENDGRID_API_KEY,
    FROM_EMAIL
)

logger = logging.getLogger(__name__)

class CommunicationManager:
    def __init__(self):
        # Twilio
        self.twilio_client = None
        self.twilio_from = TWILIO_PHONE_NUMBER
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            try:
                self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            except Exception as e:
                logger.exception("Failed to initialize Twilio client: %s", e)

        # SendGrid
        self.sendgrid_client = None
        if SENDGRID_API_KEY:
            try:
                self.sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
            except Exception as e:
                logger.exception("Failed to initialize SendGrid client: %s", e)

    def send_sms(self, to, message):
        """
        Send SMS via Twilio. `to` should be E.164 format e.g. +9190XXXXXXXX
        Returns message.sid on success, or raises exception.
        """
        if not self.twilio_client:
            raise RuntimeError("Twilio client not configured")

        try:
            msg = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_from,
                to=to
            )
            return msg.sid
        except Exception as e:
            logger.exception("Failed to send SMS: %s", e)
            raise

    def send_email(self, to_email, subject, content):
        """
        Send plain text email via SendGrid.
        """
        if not self.sendgrid_client:
            raise RuntimeError("SendGrid client not configured")

        message = Mail(from_email=FROM_EMAIL, to_emails=to_email, subject=subject, plain_text_content=content)
        try:
            resp = self.sendgrid_client.send(message)
            return resp.status_code
        except Exception as e:
            logger.exception("Failed to send email: %s", e)
            raise
