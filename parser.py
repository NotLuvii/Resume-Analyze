import fitz  # PyMuPDF for PDF parsing
from docx import Document  # For DOCX parsing

def read_pdf(file_path):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_docx(file_path):
    """
    Extracts text from a DOCX file.
    """
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    """
    Detects the file format and extracts text accordingly.
    """
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
