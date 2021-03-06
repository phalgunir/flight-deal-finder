import smtplib
from twilio.rest import Client
from variables import *


# This class is responsible for sending notifications with the flight details.
class NotificationManager:

    def send_sms(self, sms_text):
        """Requires SMS body as argument. Sends SMS to your phone number using Twilio API."""
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=sms_text, from_=TWILIO_PH_NO, to=MY_PH_NO)
        print(f'SMS Status: {message.status}')


    def send_email(self, email_text, to_email_list):
        """Requires email body as argument. Sends email to your email address using SMTPLib module."""
        for to_email in to_email_list:
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_email,
                                    msg=f'Subject: Low Flight Price Alert!\n\n{email_text}')
                print(f'Email sent to {to_email}')
