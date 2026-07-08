from __future__ import annotations

from backend.generation.embedding_encoder import (
    EmbeddingEncoder,
)

from backend.generation.generation_config import (
    GenerationConfig,
)


class EncoderService:

    def __init__(self) -> None:

        self._encoders = {
            "embedding": EmbeddingEncoder(),
        }

    def register_encoder(
        self,
        name: str,
        encoder,
    ) -> None:

        self._encoders[name] = encoder

    def encode(
        self,
        selfies_string: str,
        encoder: str | None = None,
    ) -> list[float]:

        encoder = (
            encoder
            or GenerationConfig.ENCODER
        )

        if encoder not in self._encoders:

            raise ValueError(
                f"Unknown encoder: {encoder}"
            )

        return self._encoders[
            encoder
        ].encode(
            selfies_string
        )

    def available_encoders(
        self,
    ) -> list[str]:

        return sorted(
            self._encoders.keys()
        )