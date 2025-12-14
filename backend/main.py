from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fusion import analyze_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), bbox: str = None):
    """
    Analyze uploaded image and return geolocation results.
    Optional bbox: "lat_min,lon_min,lat_max,lon_max" for refinement.
    """
    image_bytes = await file.read()
    result = analyze_image(image_bytes, bbox)
    return result
