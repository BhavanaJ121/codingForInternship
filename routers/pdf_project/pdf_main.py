# importing required classes
from fastapi import UploadFile, APIRouter, File, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
import PyPDF2
import model

# creating a pdf reader object
router = APIRouter(
    prefix="/pdf",
    tags=['pdf']
)


class PdfReader:
    def __init__(self, filename):
        self. filename = filename
        self.text = ""

    def read_pdf(self):
        file = open(self.filename, 'rb')
        reader = PyPDF2.PdfReader(file)
        text = ""
        for i in range(len(reader.pages)):
            text += str(reader.pages[i].extract_text())
        file.close()
        self.text = text
        return text

    def create_model(self, db):
        pdfs_model = model.Pdfs()
        pdfs_model.name = str(self.filename)
        pdfs_model.content = self.text

        db.add(pdfs_model)
        db.commit()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/upload-file')
async def read_pdf_api(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await uploaded_file.read()
    with open(uploaded_file.filename, "wb") as f:
        f.write(file_content)

    pdf_object = PdfReader(uploaded_file.filename)
    text = pdf_object.read_pdf()
    pdf_object.create_model(db)

    return {"content": text}


@router.get("/open-files-from-database")
async def all_files(db: Session = Depends(get_db)):
    pdfs = db.query(model.Pdfs).all()
    return {"pdfs": pdfs}
