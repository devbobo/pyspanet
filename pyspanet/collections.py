""" pyspanet.collections """
from __future__ import annotations

from builtins import type
from collections import UserDict
from typing import Any, Optional, Union

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

NoneType = type(None)


class MyDict(UserDict):
    """ MyDict """
    def __getattr__(self, arg: Any) -> Optional[Any]:
        try:
            result = self.data[arg]
        except KeyError as error:
            raise AttributeError from error

        return result


###############################################################################
# BlowerDict
###############################################################################

class BlowerDict(MyDict):
    """ BlowerDict """
    speed: BlowerSpeed
    state: BlowerState


###############################################################################
# DateTimeDict
###############################################################################

class DateTimeDict(MyDict):
    """ DateTimeDict """
    hours: int
    minutes: int
    seconds: int
    day: int
    month: MonthEnum
    year: int


###############################################################################
# DeviceDict
###############################################################################

class DeviceDict(MyDict):
    """ DeviceDict """
    model: str
    software: str


###############################################################################
# FiltrationDict
###############################################################################

class FiltrationDict(MyDict):
    """ FiltrationDict """
    cycle: FiltrationCycle
    runtime: FiltrationRuntime


###############################################################################
# FloatCodedInteger
###############################################################################

class FloatCodedInteger(int):
    """ FloatCodedInteger """
    def __new__(cls, value: Union[int, float, str]) -> FloatCodedInteger:
        if isinstance(value, float):
            value = int(value * 10)
        elif isinstance(value, str) and not value.isnumeric():
            if value.replace('.', '').isnumeric():
                value = int(float(value) * 10)

        return super(FloatCodedInteger, cls).__new__(cls, value)

    def __float__(self) -> float:
        return float(int(self) / 10)

    def __str__(self) -> str:
        return str(float(self))

    def __eq__(self, value: object) -> bool:
        if isinstance(value, float):
            return float(self) == value

        if isinstance(value, str):
            return str(value) == value

        return super().__eq__(value)


###############################################################################
# HeatPumpDict
###############################################################################

class HeatPumpDict(MyDict):
    """ HeatPumpDict """
    boost: OffOnState
    mode: HeatPumpMode


###############################################################################
# LightDict
###############################################################################

class LightDict(MyDict):
    """ LightDict """
    brightness: LightBrightness
    colour: LightColour
    effect: LightEffect
    mode: LightMode
    state: OffOnState


###############################################################################
# PowerSaveDict
###############################################################################

class PowerSaveDict(MyDict):
    """ PowerSaveDict """
    state: PowerSave
    peak: StartStopDict


###############################################################################
# PumpDict
###############################################################################

class PumpDict(MyDict):
    """ PumpDict """
    installed: OffOnState
    speed: PumpType
    state: Union[
        OffOnState,
        OffOnAutoState,
        OffHighLowState,
        OffLowAutoState,
        HighLowState,
        NoneType
    ]

    def __getattr__(self, arg: Any) -> Optional[Any]:
        try:
            result = self.data[arg]
        except KeyError as error:
            if arg in ['speed', 'state']:
                return None

            raise AttributeError from error

        return result


###############################################################################
# PumpsDict
###############################################################################

class PumpsDict(MyDict):
    """ PumpsDict """
    pump1: PumpDict
    pump2: PumpDict
    pump3: PumpDict
    pump4: PumpDict
    pump5: PumpDict


###############################################################################
# SettingDict
###############################################################################

class SettingDict(MyDict):
    """ SettingDict """
    auto_clean: TimeCodedInteger
    datetime: DateTimeDict
    filtration: FiltrationDict
    heat_pump: HeatPumpDict
    lock_mode: LockMode
    power_save: PowerSaveDict
    sleep: SleepDict
    time_out: TimeCodedInteger


###############################################################################
# SleepDict
###############################################################################

class SleepDict(MyDict):
    """ SleepDict """
    awake_remaining: int
    timer1: SleepTimerDict
    timer2: SleepTimerDict


###############################################################################
# StartStopDict
###############################################################################

class StartStopDict(MyDict):
    """ StartStopDict """
    start: TimeCodedInteger
    stop: TimeCodedInteger


###############################################################################
# SleepTimerDict
###############################################################################

class SleepTimerDict(StartStopDict):
    """ SleepTimerDict """
    state: SleepTimer


###############################################################################
# StateDict
###############################################################################

class StateDict(MyDict):
    """ StateDict """
    auto: OffOnState
    clean: OffOnState
    heat: OffOnState
    label: StateLabel
    mode: OperationMode
    sleep: OffOnState
    uv: OffOnState
    water: OffOnState


###############################################################################
# TemperatureDict
###############################################################################

class TemperatureDict(MyDict):
    """ TemperatureDict """
    heater: FloatCodedInteger
    target: FloatCodedInteger
    water: FloatCodedInteger


###############################################################################
# TimeCodedInteger
###############################################################################

class TimeCodedInteger(int):
    """ TimeCodedInteger """
    def __new__(cls, value: Union[int, float, str]) -> TimeCodedInteger:
        if isinstance(value, str) and not value.isnumeric():
            if value.replace(':', '').isnumeric():
                hours, minutes = value.split(':', 1)
                value = int(hours) * 256 + int(minutes)

        self = super(TimeCodedInteger, cls).__new__(cls, value)

        if isinstance(self, TimeCodedInteger):
            if self < 0:
                return TimeCodedInteger(0)
            elif self > 5947:
                return TimeCodedInteger(5947)
        return self

    def __str__(self) -> str:
        hours = int(self / 256)
        minutes = self % 256

        return f'{hours}:{minutes:02}'

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return str(self) == value

        return super().__eq__(value)
