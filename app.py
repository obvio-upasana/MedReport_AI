from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import shutil
import tempfile

from parser import extract_text_from_pdf
from rag import add_report, clear_report, has_report
from agents import ask_agent


app = FastAPI(
    title="MedReport AI",
    description="AI-powered medical report education assistant",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class ChatRequest(BaseModel):
    question: str


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "MedReport AI API is running",
        "status": "healthy"
    }


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    temp_path = None

    try:

        # Temporary file.
        # It is deleted after processing.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_path = temp_file.name

            shutil.copyfileobj(
                file.file,
                temp_file
            )

        # Extract text / OCR
        text = extract_text_from_pdf(temp_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from this PDF."
            )

        # New report replaces old report
        clear_report()

        chunk_count = add_report(text)

        return {
            "success": True,
            "filename": file.filename,
            "characters_extracted": len(text),
            "chunks_created": chunk_count,
            "message": "Report uploaded and processed successfully."
        }

    finally:

        if temp_path:
            Path(temp_path).unlink(
                missing_ok=True
            )


# --------------------------------------------------
# Ask question about uploaded report
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    if not has_report():
        raise HTTPException(
            status_code=400,
            detail="Please upload a medical report first."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        answer = ask_agent(
            request.question
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        print("Agent error:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to generate an answer."
        )


# --------------------------------------------------
# Run:
#
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
# --------------------------------------------------