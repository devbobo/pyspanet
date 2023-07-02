""" SpaConnection class """
from __future__ import annotations

import logging
from abc import abstractmethod
from builtins import type
from enum import IntEnum
from typing import Optional, Union

from .collections import FloatCodedInteger, TimeCodedInteger
from .const import (
    CMD_BLOWER,
    CMD_CLEAN,
    CMD_LIGHTS_OFF,
    CMD_LIGHTS_ON,
    CMD_PUMP1,
    CMD_PUMP2,
    CMD_PUMP3,
    CMD_PUMP4,
    CMD_PUMP5,
    CMD_REFRESH,
)

NoneType = type(None)

_LOGGER = logging.getLogger(__name__)


class SpaConnection():
    """Spa connection."""

    # def __init__(self, config: SpaConfig) -> None:
    #     self._config: SpaConfig

    #     self._config = config

    @property
    def connected(self) -> bool:
        """ Spa is connected"""
        return self._connected

    async def connect(self) -> bool:
        """Connect to the spa."""
        return await self._connect()

    async def disconnect(self) -> None:
        """Disconnect from the spa."""
        await self._disconnect()

    async def send(
        self,
        cmd: str,
        value: Union[
            IntEnum,
            FloatCodedInteger,
            TimeCodedInteger,
            NoneType
        ] = None
    ) -> Union[bool, str]:
        """ Send a command to the spa"""
        if not self.connected:
            return False

        _LOGGER.debug("Send: %s", cmd)

        msg = self._build_msg(cmd, value)
        result = await self._send(msg)

        _LOGGER.debug("Received: %s", result)

        if result is None or (
            result.startswith(CMD_REFRESH) and cmd != CMD_REFRESH
        ):
            return False

        if cmd == CMD_REFRESH:
            return str(result)

        if cmd in {
            CMD_BLOWER,
            CMD_PUMP1,
            CMD_PUMP2,
            CMD_PUMP3,
            CMD_PUMP4,
            CMD_PUMP5
        }:
            return result.strip() == f'{cmd}-OK'

        if cmd in {CMD_CLEAN, CMD_LIGHTS_OFF, CMD_LIGHTS_ON}:
            return result.strip() == cmd

        return int(result.strip()) == value

    def _build_msg(
        self,
        cmd: str,
        value: Union[
            IntEnum,
            FloatCodedInteger,
            TimeCodedInteger,
            NoneType
        ] = None
    ) -> str:
        if value is None:
            return cmd

        return f'{cmd}:{int(value)}'

    @property
    @abstractmethod
    def _connected(self) -> bool: ...

    @abstractmethod
    async def _connect(self) -> bool: ...

    @abstractmethod
    async def _disconnect(self) -> None: ...

    @abstractmethod
    async def _send(self, msg: str) -> Optional[str]: ...
