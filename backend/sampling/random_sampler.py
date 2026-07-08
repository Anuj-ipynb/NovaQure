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


class RandomSampler(
    BaseSampler
):

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

        sampled = vector.perturb(
            GenerationConfig.LATENT_NOISE_STD
        )

        return sampled.to_list()
