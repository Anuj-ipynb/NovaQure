from __future__ import annotations

from backend.sampling.random_sampler import (
    RandomSampler
)

from backend.sampling.qcbm_sampler import (
    QCBMSampler
)


class SamplingService:

    def __init__(self):

        self._samplers = {

            "random": RandomSampler(),

            "qcbm": QCBMSampler(),

        }

        self._default = "qcbm"

    def register_sampler(
        self,
        name: str,
        sampler
    ):

        self._samplers[name] = sampler

    def sample(
        self,
        latent_vector: list[float],
        strategy: str | None = None
    ) -> list[float]:

        strategy = (
            strategy
            or
            self._default
        )

        if strategy not in self._samplers:

            raise ValueError(
                f"Unknown strategy: {strategy}"
            )

        return self._samplers[
            strategy
        ].sample(
            latent_vector
        )

    def available_strategies(
        self
    ) -> list[str]:

        return sorted(
            self._samplers.keys()
        )
