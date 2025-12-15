from meteostat import Point, Daily
from datetime import datetime

def score_candidates_by_weather(candidates, exif_data):
    scores = {}
    ts = exif_data.get("EXIF DateTimeOriginal")
    if not ts:
        return scores

    dt = datetime.strptime(ts, "%Y:%m:%d %H:%M:%S")

    for c in candidates:
        lat, lon = c["coords"]["lat"], c["coords"]["lon"]
        try:
            data = Daily(Point(lat, lon), dt, dt).fetch()
            if data.empty:
                scores[(lat, lon)] = 0.3
            else:
                prcp = data["prcp"].iloc[0]
                scores[(lat, lon)] = 0.7 if prcp == 0 else 0.4
        except Exception:
            scores[(lat, lon)] = 0.3

    return scores
