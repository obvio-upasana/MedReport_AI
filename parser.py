from langchain_community.document_loaders import PyPDFLoader

import pytesseract

from pdf2image import convert_from_path


# --------------------------------------------------
# Normal PDF extraction
# --------------------------------------------------

def extract_normal_text(file_path: str) -> str:

    loader = PyPDFLoader(
        file_path
    )

    documents = loader.load()

    text = "\n".join(
        document.page_content
        for document in documents
    )

    return text


# --------------------------------------------------
# OCR extraction
# --------------------------------------------------

def extract_ocr_text(file_path: str) -> str:

    images = convert_from_path(
        file_path
    )

    pages = []

    for image in images:

        text = pytesseract.image_to_string(
            image
        )

        pages.append(text)

    return "\n".join(pages)


# --------------------------------------------------
# Main PDF parser
# --------------------------------------------------

def extract_text_from_pdf(file_path: str) -> str:

    # Try normal text extraction
    text = extract_normal_text(
        file_path
    )

    # If enough text exists, use it
    if len(text.strip()) >= 50:

        print(
            "Normal PDF text extraction successful."
        )

        return text

    # Otherwise OCR
    print(
        "Little/no text found. Starting OCR..."
    )

    ocr_text = extract_ocr_text(
        file_path
    )

    return ocr_text