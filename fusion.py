from geoclip_model import predict_locations
from ocr import extract_text
from exif import extract_exif

from sun_analysis import score_candidates_by_sun
from weather import score_candidates_by_weather
from priors import population_prior

from landmarks import detect_landmarks
from language_detection import detect_language

from math import sqrt


# --------------------------------------------------
# Helper: approximate distance between coordinates
# --------------------------------------------------
def coord_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# --------------------------------------------------
# Single image analysis
# --------------------------------------------------
def analyze_single_image(image_bytes):
    exif_data = extract_exif(image_bytes)
    ocr_text = extract_text(image_bytes)

    candidates = predict_locations(image_bytes)
    if not candidates:
        return [], {}

    sun_scores = score_candidates_by_sun(candidates, exif_data)
    weather_scores = score_candidates_by_weather(candidates, exif_data)
    population_scores = population_prior(candidates)

    landmark_score = detect_landmarks(image_bytes)
    detected_language = detect_language(ocr_text)

    fused_candidates = []

    for c in candidates:
        lat = c["coords"]["lat"]
        lon = c["coords"]["lon"]
        key = (lat, lon)

        final_score = (
            0.65 * c["score"] +
            0.08 * sun_scores.get(key, 0.0) +
            0.07 * weather_scores.get(key, 0.0) +
            0.10 * population_scores.get(key, 0.0) +
            0.10 * landmark_score
        )

        fused_candidates.append({
            "coords": c["coords"],
            "geo_score": c["score"],
            "final_score": round(final_score, 4)
        })

    return fused_candidates, {
        "landmark_score": landmark_score,
        "detected_language": detected_language,
        "ocr_excerpt": ocr_text[:300],
        "exif_present": bool(exif_data)
    }


# --------------------------------------------------
# Multi-image fusion
# --------------------------------------------------
def fuse_multiple_images(results, merge_threshold=0.5):
    """
    Merge candidates from multiple images.

    merge_threshold:
      Approx degrees (~0.5 ≈ 50 km)
    """

    merged = []

    for candidate_list in results:
        for c in candidate_list:
            coord = (c["coords"]["lat"], c["coords"]["lon"])
            matched = False

            for m in merged:
                mcoord = (m["coords"]["lat"], m["coords"]["lon"])
                if coord_distance(coord, mcoord) < merge_threshold:
                    m["final_score"] = round(
                        (m["final_score"] + c["final_score"]) / 2,
                        4
                    )
                    matched = True
                    break

            if not matched:
                merged.append(c.copy())

    merged.sort(key=lambda x: x["final_score"], reverse=True)
    return merged


# --------------------------------------------------
# Public API
# --------------------------------------------------
def analyze_images(image_bytes_list):
    """
    image_bytes_list:
      - 1 image  → single-image mode
      - N images → multi-image fusion
    """

    per_image_results = []
    explanations = []

    for img_bytes in image_bytes_list:
        candidates, explanation = analyze_single_image(img_bytes)
        if candidates:
            per_image_results.append(candidates)
            explanations.append(explanation)

    if not per_image_results:
        return {
            "candidates": [],
            "explanation": {
                "error": "No valid candidates found"
            }
        }

    if len(per_image_results) > 1:
        fused_candidates = fuse_multiple_images(per_image_results)
        mode = "multi-image"
    else:
        fused_candidates = per_image_results[0]
        mode = "single-image"

    return {
        "candidates": fused_candidates[:5],
        "explanation": {
            "mode": mode,
            "images_used": len(per_image_results),
            "per_image_explanations": explanations
        }
    }
