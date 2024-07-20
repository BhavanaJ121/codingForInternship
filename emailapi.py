from typing import Optional

from fastapi import FastAPI
from email.message import EmailMessage
import ssl
import smtplib

app = FastAPI()
sender = 'bhavanajayanth313@gmail.com'
password = 'tmgf hpfb hyml zgoh'
password_sendgrid = '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'
context = ssl.create_default_context()


@app.get("/")
async def send_email(receiver: str, message: str, subject: str):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(message)

    with smtplib.SMTP_SSL('smtp.sendgrid.net', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
