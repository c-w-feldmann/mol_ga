from __future__ import annotations
import math
import random

import numpy as np

def uniform_qualitle_sampling(
    population: list[tuple[float, str]],
    n_sample: int,
    shuffle: bool = True,
) -> list[str]:
    """Sample SMILES by sampling uniformly from logarithmically spaced top-N."""

    samples: list[str] = []
    quantiles = 1 - np.logspace(-2, 0, 25)
    n_samples_per_quanitile = int(math.ceil(n_sample / len(quantiles)))
    for q in quantiles:
        score_threshold = np.quantile([s for s, _ in population], q)
        eligible_population = [smiles for score, smiles in population if score >= score_threshold]
        samples.extend(random.choices(population=eligible_population, k=n_samples_per_quanitile))

    # Shuffle samples to decrease correlations between adjacent samples
    if shuffle:
        random.shuffle(samples)

    return samples[:n_sample]  # in case there are slightly too many samples
