from pvlib import solarposition
from datetime import datetime
import pytz
import math

def estimate_latitude(image_bytes, exif_data):
    """
    Estimate latitude using sun elevation and image timestamp.
    Returns a dict mapping candidate coordinates to latitude likelihood.
    """
    results = {}
    try:
        # Extract timestamp from EXIF
        timestamp_str = exif_data.get("EXIF DateTimeOriginal")
        if not timestamp_str:
            return results
        dt = datetime.strptime(timestamp_str, "%Y:%m:%d %H:%M:%S")
        dt = dt.replace(tzinfo=pytz.UTC)

        # Dummy approximation: iterate latitude -90 to 90 to compute sun elevation at noon
        for lat in range(-90, 91, 5):
            solpos = solarposition.get_solarposition(dt, lat, 0)
            elevation = solpos['apparent_elevation'].iloc[0]
            # Higher elevation closer to noon -> higher score
            score = max(0, math.cos(math.radians(90 - elevation)))
            results[lat] = score
    except Exception as e:
        print("Sun analysis error:", e)
    return results
