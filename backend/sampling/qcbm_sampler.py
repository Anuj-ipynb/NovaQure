from __future__ import annotations

import numpy as np

from backend.generation.generation_config import (
    GenerationConfig
)

from backend.generation.latent_space import (
    LatentVector
)

from backend.sampling.base_sampler import (
    BaseSampler
)


class QCBMSampler(
    BaseSampler
):
    """
    QCBM-inspired latent sampler.

    This is NOT a true quantum circuit.

    It simulates stochastic exploration of
    latent space while preserving compatibility
    with a future PennyLane implementation.
    """

    def sample(
        self,
        latent_vector: list[float]
    ) -> list[float]:

        vector = LatentVector(
            np.array(
                latent_vector,
                dtype=float
            )
        )

        samples = []

        for _ in range(5):

            candidate = vector.perturb(
                GenerationConfig.LATENT_NOISE_STD
            )

            samples.append(
                candidate.values
            )

        mean_vector = np.mean(
            samples,
            axis=0
        )

        return (
            LatentVector(
                mean_vector
            )
            .normalize()
            .to_list()
        )
