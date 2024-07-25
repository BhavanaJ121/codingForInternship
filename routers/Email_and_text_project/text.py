from typing import Optional

from fastapi import APIRouter
from routers.Email_and_text_project.emails import EmailMessage
import ssl
import smtplib

router = APIRouter(
    prefix="/text",
    tags=['text']
)
sender = 'bhavanajayanth313@gmail.com'
password = 'tmgf hpfb hyml zgoh'
password_sendgrid = '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'
context = ssl.create_default_context()


@router.get("/send-message")
async def send_message(number: str, message: str, subject: Optional[str] = None):
    number = number + "@vtext.com"
    if subject == None:
        subject = " "
    em = EmailMessage()
    em['From'] = sender
    em['To'] = number
    em['Subject'] = subject
    em.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, number, em.as_string())
