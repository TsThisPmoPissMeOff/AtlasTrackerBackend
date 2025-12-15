from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fusion import fuse_images
from ocr import extract_text

app = FastAPI(title="AtlasTracker Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    files: List[UploadFile] = File(...),
    refine_lat: float = Form(None),
    refine_lon: float = Form(None)
):
    """
    Accepts one or multiple images. Optional refine_lat/refine_lon to refine geolocation.
    """
    images_bytes = [await f.read() for f in files]

    # Multi-image fusion
    geo_result = fuse_images(images_bytes)

    # OCR extraction for each image
    ocr_texts = [extract_text(b) for b in images_bytes]

    # Apply refinement if provided
    if refine_lat is not None and refine_lon is not None:
        geo_result['latitude'] = (geo_result['latitude'] + refine_lat) / 2
        geo_result['longitude'] = (geo_result['longitude'] + refine_lon) / 2
        geo_result['confidence'] *= 1.1  # slightly boost confidence

    return {
        "geolocation": geo_result,
        "ocr_texts": ocr_texts
    }
