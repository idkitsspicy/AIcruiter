import pdfplumber
from docx import Document


# -------- PDF -------- #
def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.strip()


# -------- DOCX -------- #
def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


# -------- TXT -------- #
def extract_text_from_txt(file):
    return file.read().decode("utf-8")