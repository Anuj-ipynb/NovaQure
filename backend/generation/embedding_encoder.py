from __future__ import annotations

import hashlib

import numpy as np
import selfies as sf

from backend.generation.base_encoder import (
    BaseEncoder
)

from backend.generation.generation_config import (
    GenerationConfig
)


class EmbeddingEncoder(
    BaseEncoder
):

    def encode(
        self,
        selfies_string: str
    ) -> list[float]:

        vector = np.zeros(
            GenerationConfig.LATENT_DIM,
            dtype=np.float32
        )

        for token in sf.split_selfies(
            selfies_string
        ):

            seed = int.from_bytes(

                hashlib.sha256(
                    token.encode()
                ).digest()[:8],

                "big"

            )

            rng = np.random.default_rng(
                seed
            )

            vector += rng.normal(

                0,

                1,

                GenerationConfig.LATENT_DIM

            )

        norm = np.linalg.norm(
            vector
        )

        if norm > 0:

            vector /= norm

        return (
            vector
            .astype(float)
            .tolist()
        )
