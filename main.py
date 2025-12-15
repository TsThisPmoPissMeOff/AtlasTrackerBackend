from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from fusion import analyze_images

app = FastAPI(
    title="AtlasFinder",
    description="Image Geolocation Analysis API",
    version="1.0.0"
)

# Allow frontend access (Cloudflare Pages, GitHub Pages, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(None),
    files: List[UploadFile] = File(None)
):
    """
    Analyze one or more images.

    - file: single image (default)
    - files: multiple images (optional, enables fusion)
    """

    image_bytes_list = []

    # Single-image mode
    if file is not None:
        image_bytes_list.append(await file.read())

    # Multi-image mode
    if files:
        for f in files:
            image_bytes_list.append(await f.read())

    if not image_bytes_list:
        return {
            "candidates": [],
            "explanation": {
                "error": "No images provided"
            }
        }

    return analyze_images(image_bytes_list)
