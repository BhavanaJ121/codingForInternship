import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from email.message import EmailMessage
import ssl
import smtplib

from starlette import status

router = APIRouter(
    prefix="/emails",
    tags=['emails']
)

load_dotenv()
sender = os.getenv('SENDER')
password = os.getenv('PASSWORD')
password_sendgrid = os.getenv('PASSWORD_SENDGRID')
carriers = {
    "verizon": "@vtext.com",
    "att": "@txt.att.net",
    "t-mobile": "@tmomail.net",
    "sprint": "@messaging.sprintpcs.com",
    "us cellular": "@email.uscc.net (sms)"
}
context = ssl.create_default_context()


class SendEmail:
    def __init__ (self, receiver, message, subject):
        self.receiver = receiver
        self.message = message
        self.subject = subject

    def send_email_or_message(self):
        em = EmailMessage()
        em['From'] = sender
        em['To'] = self.receiver
        em['Subject'] = self.subject
        em.set_content(self.message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, self.receiver, em.as_string())


def find_company(name):
    for carrier in carriers.keys():
        if name == carrier:
            return carriers[name]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/")
def send_email_api(receiver: str, message: str, subject: str):
    email_object = SendEmail(receiver, message, subject)
    email_object.send_email_or_message()


@router.get("/send-message")
def send_message_api(number: str, message: str, company: str, subject: Optional[str] = None):
    company_at = find_company(company)
    number = str(number) + company_at
    message_object = SendEmail(number, message, subject)
    if subject == None:
        subject = " "

    message_object.send_email_or_message()
