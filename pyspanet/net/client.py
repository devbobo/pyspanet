""" SpaNetClient class """
from __future__ import annotations

import logging

from ..client import SpaClient
from .connection import SpaNetConfig, SpaNetConnection

_LOGGER = logging.getLogger(__name__)


class SpaNetClient(SpaClient):
    """ SpaNetClient """
    def __init__(
        self,
        config: SpaNetConfig
    ) -> None:
        """Initialize a spa client."""
        super().__init__()

        self._config = config
        self._connection = SpaNetConnection(config)
