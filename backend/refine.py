def apply_bounding_box(bbox):
    """
    bbox format: "lat_min,lon_min,lat_max,lon_max"
    Used to restrict GeoCLIP candidate search.
    """
    # Implementation will filter candidate locations
    lat_min, lon_min, lat_max, lon_max = map(float, bbox.split(','))
    # Store globally or pass to geoclip_model
    global BBOX
    BBOX = (lat_min, lon_min, lat_max, lon_max)
