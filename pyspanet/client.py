""" SpaClient class """
from __future__ import annotations

import logging
from builtins import type
from typing import Any, Union

from .collections import FloatCodedInteger, MyDict, PumpDict, TimeCodedInteger
from .connection import SpaConnection
from .const import (
    CMD_BLOWER,
    CMD_BLOWER_SPEED,
    CMD_CLEAN,
    CMD_CLEAN_AUTO,
    CMD_FILTRATION_CYCLE,
    CMD_FILTRATION_RUNTIME,
    CMD_HEAT_PUMP_BOOST,
    CMD_HEAT_PUMP_MODE,
    CMD_LIGHTS_BRIGHTNESS,
    CMD_LIGHTS_COLOUR,
    CMD_LIGHTS_EFFECT,
    CMD_LIGHTS_MODE,
    CMD_LIGHTS_OFF,
    CMD_LIGHTS_ON,
    CMD_LOCK_MODE,
    CMD_OPERATION_MODE,
    CMD_PUMP1,
    CMD_PUMP2,
    CMD_PUMP3,
    CMD_PUMP4,
    CMD_PUMP5,
    CMD_REFRESH,
    CMD_TEMPERATURE,
    CMD_TIME_OUT,
)
from .data import SpaData
from .enums import (
    BlowerSpeed,
    BlowerState,
    FiltrationCycle,
    FiltrationRuntime,
    HeatPumpMode,
    HighLowState,
    LightBrightness,
    LightColour,
    LightEffect,
    LightMode,
    LockMode,
    OffHighLowState,
    OffLowAutoState,
    OffOnAutoState,
    OffOnState,
    OperationMode,
)
from .exceptions import SpaConnectionError

_LOGGER = logging.getLogger(__name__)


class SpaClient():
    """ SpaClient """
    def __init__(self) -> None:
        """Initialize a spa client."""
        self._connection: SpaConnection
        self._data: SpaData

    @property
    def connected(self) -> bool:
        """ connected: bool """
        return bool(self._connection.connected)

    @property
    def data(self) -> SpaData:
        """Return the data."""
        return self._data

    async def connect(self) -> bool:
        """Connect to the spa."""
        if not await self._connection.connect():
            raise SpaConnectionError()

        if not await self.refresh():
            raise SpaConnectionError()

        return True

    async def disconnect(self) -> None:
        """ disconnect: None """
        await self._connection.disconnect()

    async def auto_clean(self, value: Union[int, str]) -> bool:
        """ time_out: bool """
        return await self._set_time_coded_integer(
            CMD_CLEAN_AUTO,
            self.data.settings,
            'auto_clean',
            value
        )

    async def blower_control(
        self,
        value: Union[BlowerSpeed, BlowerState]
    ) -> bool:
        """ blower_control: bool """
        if isinstance(value, BlowerState):
            key = 'state'
            cmd = CMD_BLOWER
        elif isinstance(value, BlowerSpeed):
            key = 'speed'
            cmd = CMD_BLOWER_SPEED

        if bool(await self._connection.send(cmd, value)):
            self.data.blower.update({key: value})

            return True

        return False

    async def clean(self) -> bool:
        """ clean: bool """
        if bool(await self._connection.send(CMD_CLEAN)):
            self.data.state.update({
                'clean': OffOnState.OFF
                if self.data.state.clean is OffOnState.ON
                else OffOnState.ON
            })
            return True

        return False

    async def filtration(
        self,
        value: Union[FiltrationCycle, FiltrationRuntime]
    ) -> bool:
        """ filtration: bool """
        if isinstance(value, FiltrationCycle):
            key = 'cycle'
            cmd = CMD_FILTRATION_CYCLE
        elif isinstance(value, FiltrationRuntime):
            key = 'runtime'
            cmd = CMD_FILTRATION_RUNTIME

        if bool(await self._connection.send(cmd, value)):
            self.data.settings.filtration.update({key: value})

            return True

        return False

    async def heat_pump(
        self,
        value: Union[HeatPumpMode, OffOnState]
    ) -> bool:
        """ heat_pump: bool """
        if isinstance(value, HeatPumpMode):
            key = 'mode'
            cmd = CMD_HEAT_PUMP_MODE
        elif isinstance(value, OffOnState):
            key = 'boost'
            cmd = CMD_HEAT_PUMP_BOOST

        if bool(await self._connection.send(cmd, value)):
            self.data.settings.heat_pump.update({key: value})

            return True

        return False

    async def lights_control(
        self,
        value: Union[
            LightBrightness,
            LightColour,
            LightEffect,
            LightMode,
            OffOnState
        ]
    ) -> bool:
        """ lights_control: bool """
        if isinstance(value, OffOnState):
            key = 'state'
            cmd = CMD_LIGHTS_ON if value == OffOnState.ON else CMD_LIGHTS_OFF
        elif isinstance(value, LightBrightness):
            key = 'brightness'
            cmd = CMD_LIGHTS_BRIGHTNESS
        elif isinstance(value, LightColour):
            key = 'colour'
            cmd = CMD_LIGHTS_COLOUR
        elif isinstance(value, LightEffect):
            key = 'effect'
            cmd = CMD_LIGHTS_EFFECT
        elif isinstance(value, LightMode):
            key = 'mode'
            cmd = CMD_LIGHTS_MODE

        if bool(await self._connection.send(
            cmd,
            value if key != 'state' else None
        )):
            self.data.lights.update({key: value})

            return True

        return False

    async def lock_mode(self, value: LockMode) -> bool:
        """ lock_mode: bool """
        if bool(await self._connection.send(CMD_LOCK_MODE, value)):
            self.data.settings.update({'lock_mode': value})
            return True

        return False

    async def operation_mode(self, value: OperationMode) -> bool:
        """ operation_mode: bool """
        if bool(await self._connection.send(CMD_OPERATION_MODE, value)):
            self.data.state.update({'mode': value})
            return True

        return False

    async def pump1_control(
        self,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ pump1_control: bool """
        return await self._pump_control(
            self.data.pumps.pump1,
            CMD_PUMP1,
            value
        )

    async def pump2_control(
        self,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ pump2_control: bool """
        return await self._pump_control(
            self.data.pumps.pump2,
            CMD_PUMP2,
            value
        )

    async def pump3_control(
        self,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ pump4_control: bool """
        return await self._pump_control(
            self.data.pumps.pump3,
            CMD_PUMP3,
            value
        )

    async def pump4_control(
        self,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ pump4_control: bool """
        return await self._pump_control(
            self.data.pumps.pump4,
            CMD_PUMP4,
            value
        )

    async def pump5_control(
        self,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ pump5_control: bool """
        return await self._pump_control(
            self.data.pumps.pump5,
            CMD_PUMP5,
            value
        )

    async def refresh(self) -> bool:
        """ refresh: bool """
        data = await self._connection.send(CMD_REFRESH)

        if isinstance(data, bool):
            return False

        self._data = SpaData(data)

        return True

    async def temperature(self, value: Union[float, int, str]) -> bool:
        """ temperature: bool """
        return await self._set_float_coded_integer(
            CMD_TEMPERATURE,
            self.data.temperature,
            'target',
            value
        )

    async def time_out(self, value: Union[int, str]) -> bool:
        """ time_out: bool """
        if TimeCodedInteger(value) > 60:
            value = 60

        return await self._set_time_coded_integer(
            CMD_TIME_OUT,
            self.data.settings,
            'time_out',
            value
        )

    async def _set_float_coded_integer(
        self,
        cmd: str,
        obj: MyDict,
        key: str,
        value: Union[float, int, str]
    ) -> bool:
        _fci = FloatCodedInteger(value)

        if bool(await self._connection.send(cmd, _fci)):
            obj.update({key: _fci})
            return True

        return False

    async def _set_time_coded_integer(
        self,
        cmd: str,
        obj: MyDict,
        key: str,
        value: Union[int, str]
    ) -> bool:
        _tci = TimeCodedInteger(value)

        if bool(await self._connection.send(cmd, _tci)):
            obj.update({key: _tci})
            return True

        return False

    async def _pump_control(
        self,
        pump: PumpDict,
        cmd: str,
        value: Union[
            OffOnState,
            OffOnAutoState,
            OffHighLowState,
            OffLowAutoState,
            HighLowState
        ]
    ) -> bool:
        """ _pump_control: bool """
        if pump.installed != OffOnState.ON:
            return False

        if type(pump.state) != type(value):
            return False

        if bool(await self._connection.send(cmd, value)):
            pump.update({'state': value})

            return True

        return False

    async def __aenter__(self) -> SpaClient:
        """Connect and start listening for messages."""
        await self.connect()

        return self

    async def __aexit__(self, *exctype: Any) -> None:
        """Disconnect."""
        await self.disconnect()
