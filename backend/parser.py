import fitz  # PyMuPDF for PDF parsing
from docx import Document  # For DOCX parsing

def extract_text(file_stream, filename):
    """
    Detects the file format based on the file extension and extracts text accordingly.
    Args:
        file_stream: A file-like object (e.g., BytesIO).
        filename: The name of the file (used to determine file type).
    """
    if filename.endswith(".pdf"):
        return read_pdf(file_stream)
    elif filename.endswith(".docx"):
        return read_docx(file_stream)
    else:
        raise ValueError(f"Unsupported file format: {filename}")

def read_pdf(file_path):
    pdf_document = fitz.open(stream=file_path.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
