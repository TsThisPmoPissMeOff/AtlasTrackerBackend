import numpy as np
from geoclip_model import GeoCLIPModel

# Initialize GeoCLIP model once
geo_model = GeoCLIPModel()

def fuse_images(images):
    """
    Takes a list of image bytes, returns fused geolocation prediction
    """
    predictions = []
    for img_bytes in images:
        pred = geo_model.predict(img_bytes)
        predictions.append(pred)

    # Simple fusion: average latitude and longitude predictions
    lats = [p['latitude'] for p in predictions]
    lons = [p['longitude'] for p in predictions]

    fused = {
        'latitude': np.mean(lats),
        'longitude': np.mean(lons),
        'confidence': np.mean([p['confidence'] for p in predictions])
    }

    return fused
