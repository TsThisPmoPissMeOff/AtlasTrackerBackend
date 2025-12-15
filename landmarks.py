import torch
import clip
from PIL import Image
import io

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

LANDMARK_PROMPTS = [
    "famous landmark",
    "historic monument",
    "tourist attraction",
    "city skyline",
    "cathedral",
    "bridge",
    "tower"
]

def detect_landmarks(image_bytes):
    image = preprocess(Image.open(io.BytesIO(image_bytes))).unsqueeze(0)
    text = clip.tokenize(LANDMARK_PROMPTS)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        scores = (image_features @ text_features.T).softmax(dim=-1)

    return float(scores.max())
