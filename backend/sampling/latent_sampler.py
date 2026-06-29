from __future__ import annotations

import random

import numpy as np

from backend.generation.latent_space import (
    LatentVector
)

from backend.generation.generation_config import (
    GenerationConfig
)


class LatentSampler:

    def __init__(self):

        np.random.seed(
            GenerationConfig.RANDOM_SEED
        )

        random.seed(
            GenerationConfig.RANDOM_SEED
        )

    def perturb(
        self,
        latent: list[float]
    ) -> list[float]:

        vector = LatentVector(
            np.array(
                latent,
                dtype=float
            )
        )

        return (
            vector
            .perturb(
                GenerationConfig.LATENT_NOISE_STD
            )
            .to_list()
        )

    def interpolate(
        self,
        latent_a: list[float],
        latent_b: list[float],
        alpha: float
    ) -> list[float]:

        a = LatentVector(
            np.array(
                latent_a
            )
        )

        b = LatentVector(
            np.array(
                latent_b
            )
        )

        return (
            a
            .interpolate(
                b,
                alpha
            )
            .normalize()
            .to_list()
        )
