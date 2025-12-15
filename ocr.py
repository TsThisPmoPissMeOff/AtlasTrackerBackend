import pytesseract
from PIL import Image
import io

def extract_text(image_bytes):
    """Extract text using Tesseract OCR."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"OCR failed: {e}"
