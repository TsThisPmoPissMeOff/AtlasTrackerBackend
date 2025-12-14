def population_prior(candidates):
    """
    Assign a prior probability based on population density.
    Dummy stub: gives equal score to all candidates.
    """
    return {c['coords']['lat']: 0.5 for c in candidates}
