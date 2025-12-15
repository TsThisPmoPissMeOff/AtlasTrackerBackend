import numpy as np
import torch
from geoclip_model import GeoCLIPModel
from torchvision import transforms
from PIL import Image
import io

# Initialize GeoCLIP model once
geo_model = GeoCLIPModel()

# CPU-compatible transform
image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def fuse_images(images_bytes):
    """
    Takes a list of image bytes and returns fused geolocation prediction
    """
    predictions = []
    for img_bytes in images_bytes:
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img_tensor = image_transform(img).unsqueeze(0)
        pred = geo_model.predict(img_tensor)
        predictions.append(pred)

    lats = [p['latitude'] for p in predictions]
    lons = [p['longitude'] for p in predictions]

    fused = {
        'latitude': np.mean(lats),
        'longitude': np.mean(lons),
        'confidence': np.mean([p['confidence'] for p in predictions])
    }

    return fused
