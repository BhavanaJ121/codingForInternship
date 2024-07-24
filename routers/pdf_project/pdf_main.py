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


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/upload-file')
async def read_pdf(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await uploaded_file.read()
    with open(uploaded_file.filename, "wb") as f:
        f.write(file_content)

    file = open(uploaded_file.filename, 'rb')
    reader = PyPDF2.PdfReader(file)
    text = ""
    for i in range(len(reader.pages)):
        text += str(reader.pages[i].extract_text())
    file.close()

    # text = read_pdf(uploaded_file.filename)

    pdfs_model = model.Pdfs()
    pdfs_model.name = str(uploaded_file.filename)
    pdfs_model.content = text

    db.add(pdfs_model)
    db.commit()

    return {"content": text}


@router.get("/open-files-from-database")
async def all_files(db: Session = Depends(get_db)):
    pdfs = db.query(model.Pdfs).all()
    return {"pdfs": pdfs}
