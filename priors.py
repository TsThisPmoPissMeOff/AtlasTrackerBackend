def population_prior(candidates):
    """
    Simple heuristic: boost mid-latitude populated regions slightly.
    """
    scores = {}
    for c in candidates:
        lat = abs(c["coords"]["lat"])
        scores[(c["coords"]["lat"], c["coords"]["lon"])] = (
            0.7 if lat < 55 else 0.4
        )
    return scores
