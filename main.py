from fastapi import FastAPI, APIRouter
import routers.Email_and_text_project.emails as emails
import routers.Email_and_text_project.text as text
import routers.pdf_project.pdf_main as pdf
import routers.serapi_project.serpapi as serp


app = FastAPI()

app.include_router(emails.router)
app.include_router(text.router)
app.include_router(pdf.router)
app.include_router(serp.router)
