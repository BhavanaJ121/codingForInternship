# importing required classes
from pypdf import PdfReader
from fastapi import FastAPI, UploadFile, APIRouter
from db import SessionLocal

# creating a pdf reader object
router = APIRouter(
    prefix="/pdf",
    tags=['pdf']
)
'''
reader = PdfReader('example.pdf') 


# printing number of pages in pdf file 
print(len(reader.pages)) 

# creating a page object 
page = reader.pages[0] 

# extracting text from page 
print(page.extract_text()) '''


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        file_path = f"C:\\Users\\hp\\OneDrive\\Documents\\gfg/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return {"message": "File saved successfully"}

    except Exception as e:
        return {"message": e.args}
    text = ""
    reader = await PdfReader(file.filename)
    for i in range(len(reader.pages)):
        text += str(reader.pages[i].extract_text())
    return {"content": text}


@router.post('/upload-file')
async def read_pdf(file: UploadFile):
    file_content = await file.read(file.size)
    file_content = str(file_content)
    return {"content": file_content}
