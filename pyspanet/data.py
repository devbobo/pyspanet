""" SpaData class """
from __future__ import annotations

import logging
import re
from builtins import type
from typing import Optional, Union

from .collections import (
    BlowerDict,
    DateTimeDict,
    DeviceDict,
    FiltrationDict,
    FloatCodedInteger,
    HeatPumpDict,
    LightDict,
    PowerSaveDict,
    PumpDict,
    PumpsDict,
    SettingDict,
    SleepDict,
    SleepTimerDict,
    StartStopDict,
    StateDict,
    TemperatureDict,
    TimeCodedInteger,
)
from .const import CMD_REFRESH
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
    MonthEnum,
    OffHighLowState,
    OffLowAutoState,
    OffOnAutoState,
    OffOnState,
    OperationMode,
    PowerSave,
    PumpType,
    SleepTimer,
    StateLabel,
)

R2 = 'R2'
R3 = 'R3'
R4 = 'R4'
R5 = 'R5'
R6 = 'R6'
R7 = 'R7'
R9 = 'R9'
RA = 'RA'
RB = 'RB'
RC = 'RC'
RE = 'RE'
RG = 'RG'

NoneType = type(None)

_LOGGER = logging.getLogger(__name__)


class SpaData():
    """ SpaData """
    def __init__(self, data: str) -> None:
        self._blower: BlowerDict
        self._device: DeviceDict
        self._lights: LightDict
        self._pumps: PumpsDict
        self._settings: SettingDict
        self._state: StateDict
        self._temperature: TemperatureDict

        self._parse(data)

    @property
    def blower(self) -> BlowerDict:
        """Return the blower."""
        return self._blower

    @property
    def cleaning(self) -> OffOnState:
        """Return the cleaning state."""
        return self.state.clean

    @property
    def device(self) -> Optional[DeviceDict]:
        """Return the device."""
        return self._device

    @property
    def heating(self) -> OffOnState:
        """Return the heating state."""
        return self.state.heat

    @property
    def lights(self) -> LightDict:
        """Return the lights."""
        return self._lights

    @property
    def pumps(self) -> PumpsDict:
        """Return the pumps."""
        return self._pumps

    @property
    def settings(self) -> SettingDict:
        """Return the settings."""
        return self._settings

    @property
    def sleeping(self) -> OffOnState:
        """Return the sleeping state."""
        return self.state.sleep

    @property
    def state(self) -> StateDict:
        """Return the pumps."""
        return self._state

    @property
    def temperature(self) -> TemperatureDict:
        """Return the pumps."""
        return self._temperature

    @property
    def target_temperature(self) -> float:
        """Return the target temperature."""
        return self.temperature.target

    @property
    def water_temperature(self) -> float:
        """Return the water temperature."""
        return self.temperature.water

    def _parse(self, data: str) -> None:
        lines = re.split(r',?:\*?\r?\n,?', data)

        if lines[0] != CMD_REFRESH:
            return

        info = {}

        for line in lines:
            if line in ('', line == CMD_REFRESH):
                continue

            items = line.split(',')
            key = items.pop(0)
            info[key] = items

        self._blower = BlowerDict({
            'speed': BlowerSpeed(int(info[R6][0])),
            'state': BlowerState(int(info[RC][9]))
        })

        self._settings = SettingDict({
            'auto_clean': TimeCodedInteger(info[R7][0]),
            'datetime': DateTimeDict({
                'hours': int(info[R2][5]),
                'minutes': int(info[R2][6]),
                'seconds': int(info[R2][7]),
                'day': int(info[R2][8]),
                'month': MonthEnum(int(info[R2][9])),
                'year': int(info[R2][10])
            }),
            'filtration': FiltrationDict({
                'cycle': FiltrationCycle(int(info[R6][6])),
                'runtime': FiltrationRuntime(int(info[R6][5])),
                # 'total-runtime': int(info[R2][16]),
                # 'requested-runtime': int(info[R2][17])
            }),
            'heat_pump': HeatPumpDict({
                'boost': OffOnState(int(info[R7][24])),
                'mode': HeatPumpMode(int(info[R7][25]))
            }),
            'lock_mode': LockMode(int(info[RG][11])),
            'power_save': PowerSaveDict({
                'state': PowerSave(int(info[R6][9])),
                'peak': StartStopDict({
                    'start': TimeCodedInteger(int(info[R6][10])),
                    'stop': TimeCodedInteger(int(info[R6][11]))
                })
            }),
            'sleep': SleepDict({
                'awake_remaining': int(info[R2][15]),
                'timer1': SleepTimerDict({
                    'state': SleepTimer(int(info[R6][12])),
                    'start': TimeCodedInteger(info[R6][14]),
                    'stop': TimeCodedInteger(info[R6][16])
                }),
                'timer2': SleepTimerDict({
                    'state': SleepTimer(int(info[R6][13])),
                    'start': TimeCodedInteger(info[R6][15]),
                    'stop': TimeCodedInteger(info[R6][17])
                })
            }),
            'time_out': TimeCodedInteger(info[R6][19])
        })

        self._device = DeviceDict({
            'model': info[R3][6],
            'software': info[R3][5]
        })

        self._lights = LightDict({
            'brightness': LightBrightness(int(info[R6][1])),
            'colour': LightColour(int(info[R6][2])),
            'effect': LightEffect(int(info[R6][4])),
            'mode': LightMode(int(info[R6][3])),
            'state': OffOnState(int(info[R5][13]))
        })

        self._pumps = PumpsDict({
            'pump1': PumpDict(self._get_pump(info[RG][6], int(info[R5][17]))),
            'pump2': PumpDict(self._get_pump(info[RG][7], int(info[R5][18]))),
            'pump3': PumpDict(self._get_pump(info[RG][8], int(info[R5][19]))),
            'pump4': PumpDict(self._get_pump(info[RG][9], int(info[R5][20]))),
            'pump5': PumpDict(self._get_pump(info[RG][10], int(info[R5][21])))
        })

        self._state = StateDict({
            'auto': OffOnState(int(info[R5][12])),
            'clean': OffOnState(int(info[R5][15])),
            'heat': OffOnState(int(info[R5][11])),
            'label': StateLabel(info[R3][19]),
            'mode': getattr(OperationMode, info[R4][0]),
            'sleep': OffOnState(int(info[R5][9])),
            'uv': OffOnState(int(info[R5][10])),
            'water': OffOnState(int(info[R2][13]))
        })

        self._temperature = TemperatureDict({
            'heater': FloatCodedInteger(info[R2][11]),
            'target': FloatCodedInteger(info[R6][7]),
            'water': FloatCodedInteger(info[R5][14])
        })

        # self._power = {
        #     'current': int(info[R2][0]),
        #     'current_limit': int(info[R3][0]),
        #     'heat_element_current': int(info[R3][21]),
        #     'voltage': int(info[R2][1])
        # }

    def _get_pump(self, pump_type: str, value: int) -> dict:
        _installed = OffOnState.ON if re.match(r'^1-', pump_type) \
            else OffOnState.OFF
        _state: Union[
            OffOnState, OffOnAutoState, OffHighLowState, OffLowAutoState,
            HighLowState, NoneType
        ] = None
        _type: Optional[PumpType] = None

        result = {
            'installed': _installed,
            'state': _state,
            'speed': _type
        }

        if result['installed'] == OffOnState.OFF:
            return result

        if re.match(r'.+-1-', pump_type):
            result['speed'] = PumpType.ONE_SPEED
        elif re.match(r'.+-2-', pump_type):
            result['speed'] = PumpType.TWO_SPEED
        else:
            result['speed'] = PumpType.UNKNOWN

        if re.match(r'.+01$', pump_type):
            result['state'] = OffOnState(value)
        elif re.match(r'.+014$', pump_type):
            result['state'] = OffOnAutoState(value)
        elif re.match(r'.+034$', pump_type):
            result['state'] = OffLowAutoState(value)
        elif re.match(r'.+023$', pump_type):
            result['state'] = OffHighLowState(value)
        elif re.match(r'.+23$', pump_type):
            result['state'] = HighLowState(value)

        return result
