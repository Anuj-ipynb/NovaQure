from __future__ import annotations

from itertools import combinations

import numpy as np


class DiversityCalculator:

    @staticmethod
    def cosine_distance(
        a: list[float],
        b: list[float]
    ) -> float:

        a = np.asarray(a)

        b = np.asarray(b)

        denom = (
            np.linalg.norm(a)
            * np.linalg.norm(b)
        )

        if denom == 0:
            return 0.0

        similarity = (
            np.dot(a, b)
            / denom
        )

        return float(
            1.0 - similarity
        )

    @classmethod
    def average_diversity(
        cls,
        vectors: list[list[float]]
    ) -> float:

        if len(vectors) < 2:
            return 0.0

        scores = []

        for a, b in combinations(
            vectors,
            2
        ):

            scores.append(
                cls.cosine_distance(
                    a,
                    b
                )
            )

        return float(
            np.mean(scores)
        )
