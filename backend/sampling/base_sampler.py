from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseSampler(ABC):

    @abstractmethod
    def sample(
        self,
        latent_vector: list[float]
    ) -> list[float]:
        """
        Return a sampled latent vector.
        """
        raise NotImplementedError
