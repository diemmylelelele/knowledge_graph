import os
from PyPDF2 import PdfReader

def read_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        print(f"[ERROR] Failed to read PDF: {e}")
        return ""

def get_input_text(input_path_or_text: str) -> str:
    """
    Accepts either direct text or a file path (.pdf or .txt).
    Returns the extracted text.
    """
    if os.path.isfile(input_path_or_text):
        if input_path_or_text.lower().endswith(".pdf"):
            return read_pdf(input_path_or_text)
        elif input_path_or_text.lower().endswith(".txt"):
            with open(input_path_or_text, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError("Unsupported file type. Use .pdf or .txt")
    else:
        return input_path_or_text
