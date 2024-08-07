from fastapi import FastAPI
import routers.Email_and_text_project.emails as emails
import routers.pdf_project.pdf_main as pdf
import routers.serapi_project.serpapi as serp
import model
from database import engine


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(emails.router)
app.include_router(pdf.router)
app.include_router(serp.router)
