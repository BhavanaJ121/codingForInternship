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
verizon = os.getenv('VERIZON')
att = os.getenv('ATT')
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


def find_company(name):
    if name == 'verizon':
        return verizon
    elif name == 'att':
        return att
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/")
def send_email(receiver: str, message: str, subject: str):
    send_email_or_message(receiver, message, subject)


@router.get("/send-message")
def send_message(number: str, message: str, company: str, subject: Optional[str] = None):
    company_at = find_company(company)
    number = str(number) + company_at
    if subject == None:
        subject = " "

    send_email_or_message(number, message, subject)
