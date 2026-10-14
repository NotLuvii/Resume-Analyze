import io

import pytest
from docx import Document


def _docx_bytes(text):
    buffer = io.BytesIO()
    doc = Document()
    doc.add_paragraph(text)
    doc.save(buffer)
    return buffer.getvalue()


@pytest.fixture
def docx_bytes():
    """Returns a function that builds a one-paragraph .docx file in memory."""
    return _docx_bytes
