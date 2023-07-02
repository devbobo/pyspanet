""" SpaMicroConnection class """
from __future__ import annotations

import logging
import time

from typing import Any

import machine

from ..connection import SpaConnection
from .config import SpaMicroConfig

_LOGGER = logging.getLogger(__name__)


class SpaMicroConnection(SpaConnection):
    """ SpaMicroConnection """
    def __init__(self, config: SpaMicroConfig) -> None:
        self._config = config
        self._uart: machine.UART

    @property
    def _connected(self) -> bool:
        if self._uart is None:
            return False
        return True

    async def _connect(self) -> bool:
        if self.connected:
            _LOGGER.debug("UART %s -- already connected", self._config.uart_id)
            return True

        _LOGGER.debug(
            "UART %s -- establishing connection",
            self._config.uart_id
        )

        self._uart = machine.UART(self._config.uart_id, self._config.baudrate)
        self._uart.init(
            self._config.baudrate,
            bits=8,
            parity=None,
            stop=1,
            rxbuf=1024
        )

        return False

    async def _disconnect(self) -> None:
        _LOGGER.debug("UART %s -- disconnect requested", self._config.uart_id)

        if self._uart is not None:
            self._uart.deinit()

        self._uart = None
        _LOGGER.debug("UART %s -- disconnected", self._config.uart_id)

    async def _send(self, msg: str) -> Any:
        self._uart.write(f'{msg}\n')

        while not self._uart.any():
            time.sleep(0.1)

        time.sleep(1)
        result = self._uart.read()

        return result.decode('utf-8')
