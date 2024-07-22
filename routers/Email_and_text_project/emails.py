from fastapi import FastAPI, APIRouter
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


@router.get("/")
async def send_email(receiver: str, message: str, subject: str):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(message)
    #sendgrid.net
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
