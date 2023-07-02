""" SpaMicroClient class """
from __future__ import annotations

from ..client import SpaClient
from .connection import SpaMicroConfig, SpaMicroConnection


class SpaMicroClient(SpaClient):
    """ SpaMicroClient """
    def __init__(
        self,
        config: SpaMicroConfig
    ) -> None:
        """Initialize a spa client."""
        super().__init__()

        self._config = config
        self._connection = SpaMicroConnection(config)
