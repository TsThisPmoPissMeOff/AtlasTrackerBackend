from pvlib import solarposition
from datetime import datetime
import pytz

def score_candidates_by_sun(candidates, exif_data):
    """
    Scores GeoCLIP candidates by sun elevation consistency.
    Weak signal by design.
    """
    scores = {}

    ts = exif_data.get("EXIF DateTimeOriginal")
    if not ts:
        return scores

    try:
        dt = datetime.strptime(ts, "%Y:%m:%d %H:%M:%S")
        dt = dt.replace(tzinfo=pytz.UTC)

        for c in candidates:
            lat = c["coords"]["lat"]
            lon = c["coords"]["lon"]
            sol = solarposition.get_solarposition(dt, lat, lon)
            elev = sol["apparent_elevation"].iloc[0]
            scores[(lat, lon)] = max(0, elev / 90)
    except Exception:
        pass

    return scores
