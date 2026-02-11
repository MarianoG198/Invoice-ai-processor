import pytesseract
from PIL import Image
import pdfplumber
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path: str) -> str:
    """
    Detecta si es PDF o imagen y devuelve el texto extraído.
    """
    text = ""

    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"

    else:  # JPG, PNG, etc.
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text.strip()
