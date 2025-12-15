import easyocr
import cv2
import numpy as np

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'])

def extract_text(image_bytes):
    """
    Takes image bytes and returns extracted text using EasyOCR
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = reader.readtext(img)
    return " ".join([r[1] for r in result])
