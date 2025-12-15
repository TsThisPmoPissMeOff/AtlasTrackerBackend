import easyocr
import cv2
import numpy as np

reader = easyocr.Reader(['en'])

def extract_text(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = reader.readtext(img)
    return " ".join([r[1] for r in result])
