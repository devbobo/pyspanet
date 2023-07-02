""" SpaMicroConfig class """
from __future__ import annotations

from dataclasses import dataclass

from ..config import SpaConfig


@dataclass
class SpaMicroConfig(SpaConfig):
    """ SpaMicroConfig """
    def __init__(self, config: dict) -> None:
        """ initialise """
        self._baudrate: int
        self._uart_id: int

        if 'baudrate' in config:
            self._baudrate = config['baudrate']
        else:
            raise KeyError('missing "baudrate" from Config dict')

        if 'uart_id' in config:
            self._uart_id = config['uart_id']
        else:
            raise KeyError('missing "uart_id" from Config dict')

        self._config = config

    @property
    def baudrate(self) -> int:
        """ _baudrate: int """
        return self._baudrate

    @property
    def uart_id(self) -> int:
        """ uart_id: int """
        return self._uart_id
