from geoclip_model import predict_locations
from ocr import extract_text
from exif import extract_exif
from sun_analysis import estimate_latitude
from weather import match_weather
from priors import population_prior
from refine import BBOX, apply_bounding_box

def analyze_image(image_bytes, bbox=None):
    # Optional refinement
    if bbox:
        apply_bounding_box(bbox)

    # Metadata extraction
    exif_data = extract_exif(image_bytes)
    text_data = extract_text(image_bytes)

    # Real visual geolocation
    visual_candidates = predict_locations(image_bytes)

    # Sun/shadow & weather scores (currently empty stubs)
    lat_estimate = estimate_latitude(image_bytes, exif_data)
    weather_score = match_weather(image_bytes, exif_data)

    # Population priors
    prior_score = population_prior(visual_candidates)

    # Weighted fusion of all scores
    final_candidates = []
    for c in visual_candidates:
        score = (
            0.4 * c['score'] +
            0.2 * lat_estimate.get(str(c['coords']),0) +
            0.2 * weather_score.get(str(c['coords']),0) +
            0.2 * prior_score.get(str(c['coords']),0)
        )
        final_candidates.append({**c, 'final_score': score})

    final_candidates.sort(key=lambda x: x['final_score'], reverse=True)

    explanation = {
        'EXIF': exif_data,
        'OCR': text_data,
        'Visual': [c['score'] for c in visual_candidates],
        'Sun/Shadow': lat_estimate,
        'Weather': weather_score,
        'Population': prior_score
    }

    return {
        'candidates': final_candidates[:5],
        'explanation': explanation
    }
