""" SpaNetConnection class """
from __future__ import annotations

import logging
import socket

from typing import Optional

from .config import SpaNetConfig
from ..connection import SpaConnection

CONNECT_SUCCESS = 'Successfully connected'

_LOGGER = logging.getLogger(__name__)


class SpaNetConnection(SpaConnection):
    """ SpaNetConnection """
    def __init__(self, config: SpaNetConfig) -> None:
        self._config = config
        self._socket: socket.socket

    @property
    def _connected(self) -> bool:
        try:
            # read bytes without blocking and or removing them from buffer
            data = self._socket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)

            if len(data) == 0:
                return False
        except AttributeError:
            return False
        except BlockingIOError:
            return True  # socket is open and reading from it would block
        except ConnectionResetError:
            return False  # socket was closed for some other reason
        except Exception:
            return True
        return True

    async def _connect(self) -> bool:
        """Connect to the spa."""
        if self.connected:
            _LOGGER.debug("%s -- already connected", self._config.host)
            return True

        _LOGGER.debug("%s -- establishing connection", self._config.host)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._socket.connect((self._config.host, self._config.port))
            self._socket.send(bytes(self._config.connect_string, 'utf-8'))
            data = self._socket.recv(22)
        except Exception:
            return False

        if data.decode() == CONNECT_SUCCESS:
            return True

        return False

    async def _disconnect(self) -> None:
        """Disconnect from the spa."""
        _LOGGER.debug("%s -- disconnect requested", self._config.host)

        if self.connected:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()

        _LOGGER.debug("%s -- disconnected", self._config.host)

    async def _send(self, msg: str) -> Optional[str]:
        if not self.connected:
            if not await self._connect():
                return None

        self._socket.sendall(bytes(f'{msg}\n', 'utf-8'))
        result = self._socket.recv(1024)

        return str(result.decode('utf-8'))
