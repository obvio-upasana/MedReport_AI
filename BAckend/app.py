from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from parser import extract_text_from_pdf


app = FastAPI()

UPLOAD_DIR = Path("../uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "MedReport AI API is running"
    }


@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "text": extracted_text
    }