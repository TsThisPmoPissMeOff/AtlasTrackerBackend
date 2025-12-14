from geoclip_model import predict_locations
from ocr import extract_text
from exif import extract_exif
from sun_analysis import estimate_latitude
from weather import match_weather
from priors import population_prior
from refine import apply_bounding_box

def analyze_image(image_bytes, bbox=None):
    # Optional: narrow search using previous bounding box
    if bbox:
        apply_bounding_box(bbox)
    
    # Extract EXIF and metadata
    exif_data = extract_exif(image_bytes)
    
    # OCR & language detection
    text_data = extract_text(image_bytes)
    
    # Visual geolocation (top K candidates)
    visual_candidates = predict_locations(image_bytes)
    
    # Sun/shadow & weather
    lat_estimate = estimate_latitude(image_bytes, exif_data)
    weather_score = match_weather(image_bytes, exif_data)
    
    # Population / priors
    prior_score = population_prior(visual_candidates)
    
    # Simple weighted fusion
    final_candidates = []
    for loc in visual_candidates:
        score = (
            0.4 * loc['score'] +
            0.2 * lat_estimate.get(loc['coords'],0) +
            0.2 * weather_score.get(loc['coords'],0) +
            0.2 * prior_score.get(loc['coords'],0)
        )
        final_candidates.append({**loc, 'final_score': score})
    
    # Sort descending by final score
    final_candidates.sort(key=lambda x: x['final_score'], reverse=True)
    
    # Prepare explanation dropdown
    explanation = {
        'EXIF': exif_data,
        'OCR': text_data,
        'Visual': [c['score'] for c in visual_candidates],
        'Sun/Shadow': lat_estimate,
        'Weather': weather_score,
        'Population': prior_score
    }
    
    return {
        'candidates': final_candidates[:5],  # top 5
        'explanation': explanation
    }
