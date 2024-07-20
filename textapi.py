from fastapi import FastAPI
from email.message import EmailMessage
import ssl
import smtplib

app = FastAPI()
sender = 'bhavanajayanth313@gmail.com'
password = 'tmgf hpfb hyml zgoh'
password_sendgrid = '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'
context = ssl.create_default_context()

@app.get("/send-message")
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

