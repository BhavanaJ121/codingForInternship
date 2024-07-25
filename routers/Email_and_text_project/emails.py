from typing import Optional

from fastapi import APIRouter
from email.message import EmailMessage
import ssl
import smtplib

router = APIRouter(
    prefix="/emails",
    tags=['emails']
)
sender = 'bhavanajayanth313@gmail.com'
password = 'tmgf hpfb hyml zgoh'
password_sendgrid = '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'
context = ssl.create_default_context()


def send_email_or_message(receiver, message, subject):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())


@router.get("/")
def send_email(receiver: str, message: str, subject: str):
    send_email_or_message(receiver, message, subject)


@router.get("/send-message")
def send_message(number: str, message: str, subject: Optional[str] = None):
    number = str(number) + "@vtext.com"
    if subject == None:
        subject = " "

    send_email_or_message(number, message, subject)
