import pdfplumber
from docx import Document
import os

def extract_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT files.
    """

    extension = os.path.splitext(file_path)[1].lower()

    # PDF
    if extension == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    # DOCX
    elif extension == ".docx":
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    # TXT
    elif extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        raise ValueError(f"Unsupported file format: {extension}")