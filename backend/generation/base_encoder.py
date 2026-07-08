from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseEncoder(ABC):

    @abstractmethod
    def encode(
        self,
        selfies_string: str
    ) -> list[float]:
        """
        Convert a molecular representation
        into a latent vector.
        """
        raise NotImplementedError
