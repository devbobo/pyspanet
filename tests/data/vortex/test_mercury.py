"""Tests module."""
from __future__ import annotations

from typing import Any

import pytest

from builtins import type
from pyspanet import SpaData
from pyspanet.collections import (
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
from pyspanet.enums import (
    BlowerSpeed,
    BlowerState,
    FiltrationCycle,
    FiltrationRuntime,
    HeatPumpMode,
    LightBrightness,
    LightColour,
    LightEffect,
    LightMode,
    LockMode,
    MonthEnum,
    OffOnAutoState,
    OffOnState,
    OperationMode,
    PowerSave,
    PumpType,
    SleepTimer,
    StateLabel,
)

NoneType = type(None)


def load_data(name: str) -> Any:
    """Load spa data from text file."""
    with open(f"tests/fixtures/{name}.txt", encoding="utf-8") as file:
        return file.read()


@pytest.fixture(name='vortex_mercury')
def vortex_mercury_fixture() -> SpaData:
    """ Vortex Mercury """
    return SpaData(load_data('vortex/mercury'))


def test_vortex_mercury_blower(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury blower data """
    assert isinstance(vortex_mercury.blower, BlowerDict)
    assert isinstance(vortex_mercury.blower.state, BlowerState)
    assert isinstance(vortex_mercury.blower.speed, BlowerSpeed)
    assert vortex_mercury.blower.state == BlowerState.OFF
    assert vortex_mercury.blower.speed == BlowerSpeed.LEVEL_1


def test_vortex_mercury_device(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury data """

    assert isinstance(vortex_mercury.device, DeviceDict)
    assert isinstance(vortex_mercury.device.model, str)
    assert isinstance(vortex_mercury.device.software, str)
    assert vortex_mercury.device.model == 'SV3'
    assert vortex_mercury.device.software == 'SW V5 17 05 31'


def test_vortex_mercury_lights(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury lights data """
    assert isinstance(vortex_mercury.lights, LightDict)
    assert isinstance(vortex_mercury.lights.brightness, LightBrightness)
    assert isinstance(vortex_mercury.lights.colour, LightColour)
    assert isinstance(vortex_mercury.lights.effect, LightEffect)
    assert isinstance(vortex_mercury.lights.mode, LightMode)
    assert isinstance(vortex_mercury.lights.state, OffOnState)
    assert vortex_mercury.lights.brightness == LightBrightness.LEVEL_5
    assert vortex_mercury.lights.colour == LightColour.COLOUR_29
    assert vortex_mercury.lights.effect == LightEffect.LEVEL_5
    assert vortex_mercury.lights.mode == LightMode.COLOUR
    assert vortex_mercury.lights.state == OffOnState.OFF


def test_vortex_mercury_pumps(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury pumps data """
    assert isinstance(vortex_mercury.pumps, PumpsDict)
    assert isinstance(vortex_mercury.pumps.pump1, PumpDict)
    assert isinstance(vortex_mercury.pumps.pump1.installed, OffOnState)
    assert isinstance(vortex_mercury.pumps.pump1.state, OffOnAutoState)
    assert isinstance(vortex_mercury.pumps.pump1.speed, PumpType)
    assert vortex_mercury.pumps.pump1.installed == OffOnState.ON
    assert vortex_mercury.pumps.pump1.state == OffOnAutoState.AUTO
    assert vortex_mercury.pumps.pump1.speed == PumpType.ONE_SPEED

    assert isinstance(vortex_mercury.pumps.pump2.installed, OffOnState)
    assert isinstance(vortex_mercury.pumps.pump2.state, OffOnState)
    assert isinstance(vortex_mercury.pumps.pump2.speed, PumpType)
    assert vortex_mercury.pumps.pump2.installed == OffOnState.ON
    assert vortex_mercury.pumps.pump2.state == OffOnState.OFF
    assert vortex_mercury.pumps.pump2.speed == PumpType.ONE_SPEED

    assert isinstance(vortex_mercury.pumps.pump3.installed, OffOnState)
    assert isinstance(vortex_mercury.pumps.pump3.state, OffOnState)
    assert isinstance(vortex_mercury.pumps.pump3.speed, PumpType)
    assert vortex_mercury.pumps.pump3.installed == OffOnState.ON
    assert vortex_mercury.pumps.pump3.state == OffOnState.OFF
    assert vortex_mercury.pumps.pump3.speed == PumpType.ONE_SPEED

    assert isinstance(vortex_mercury.pumps.pump4.installed, OffOnState)
    assert vortex_mercury.pumps.pump4.installed == OffOnState.OFF

    assert isinstance(vortex_mercury.pumps.pump5.installed, OffOnState)
    assert vortex_mercury.pumps.pump5.installed == OffOnState.OFF


def test_vortex_mercury_state(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury state data """
    assert isinstance(vortex_mercury.state, StateDict)
    assert isinstance(vortex_mercury.state.auto, OffOnState)
    assert isinstance(vortex_mercury.state.clean, OffOnState)
    assert isinstance(vortex_mercury.state.heat, OffOnState)
    assert isinstance(vortex_mercury.state.label, StateLabel)
    assert isinstance(vortex_mercury.state.mode, OperationMode)
    assert isinstance(vortex_mercury.state.sleep, OffOnState)
    assert isinstance(vortex_mercury.state.uv, OffOnState)
    assert isinstance(vortex_mercury.state.water, OffOnState)
    assert vortex_mercury.state.auto == OffOnState.ON
    assert vortex_mercury.state.clean == OffOnState.OFF
    assert vortex_mercury.state.heat == OffOnState.OFF
    assert vortex_mercury.state.label == StateLabel.AUTO
    assert vortex_mercury.state.mode == OperationMode.ECON
    assert vortex_mercury.state.sleep == OffOnState.OFF
    assert vortex_mercury.state.uv == OffOnState.OFF
    assert vortex_mercury.state.water == OffOnState.ON


def test_vortex_mercury_temperature(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury temperature data """
    assert isinstance(vortex_mercury.temperature, TemperatureDict)
    assert isinstance(vortex_mercury.temperature.heater, FloatCodedInteger)
    assert isinstance(vortex_mercury.temperature.target, FloatCodedInteger)
    assert isinstance(vortex_mercury.temperature.water, FloatCodedInteger)
    assert vortex_mercury.temperature.heater == 27.3
    assert vortex_mercury.temperature.heater == 273
    assert vortex_mercury.temperature.target == 20.0
    assert vortex_mercury.temperature.target == 200
    assert vortex_mercury.temperature.water == 28.6
    assert vortex_mercury.temperature.water == 286


def test_vortex_mercury_settings(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury data """
    assert isinstance(vortex_mercury.settings, SettingDict)

    assert isinstance(vortex_mercury.settings.datetime, DateTimeDict)
    assert isinstance(vortex_mercury.settings.datetime.hours, int)
    assert isinstance(vortex_mercury.settings.datetime.minutes, int)
    assert isinstance(vortex_mercury.settings.datetime.seconds, int)
    assert isinstance(vortex_mercury.settings.datetime.day, int)
    assert isinstance(vortex_mercury.settings.datetime.month, MonthEnum)
    assert isinstance(vortex_mercury.settings.datetime.year, int)

    assert isinstance(vortex_mercury.settings.filtration, FiltrationDict)
    assert isinstance(
        vortex_mercury.settings.filtration.cycle, FiltrationCycle
    )
    assert isinstance(
        vortex_mercury.settings.filtration.runtime, FiltrationRuntime
    )

    assert isinstance(vortex_mercury.settings.heat_pump, HeatPumpDict)
    assert isinstance(vortex_mercury.settings.heat_pump.boost, OffOnState)
    assert isinstance(vortex_mercury.settings.heat_pump.mode, HeatPumpMode)

    assert isinstance(vortex_mercury.settings.lock_mode, LockMode)

    assert isinstance(vortex_mercury.settings.power_save, PowerSaveDict)
    assert isinstance(vortex_mercury.settings.power_save.state, PowerSave)
    assert isinstance(vortex_mercury.settings.power_save.peak, StartStopDict)
    assert isinstance(
        vortex_mercury.settings.power_save.peak.start,
        TimeCodedInteger
    )
    assert isinstance(
        vortex_mercury.settings.power_save.peak.stop,
        TimeCodedInteger
    )

    assert isinstance(vortex_mercury.settings.sleep, SleepDict)
    assert isinstance(vortex_mercury.settings.sleep.awake_remaining, int)
    assert isinstance(vortex_mercury.settings.sleep.timer1, SleepTimerDict)
    assert isinstance(vortex_mercury.settings.sleep.timer1.state, SleepTimer)
    assert isinstance(
        vortex_mercury.settings.sleep.timer1.start, TimeCodedInteger
    )
    assert isinstance(
        vortex_mercury.settings.sleep.timer1.stop, TimeCodedInteger
    )
    assert isinstance(vortex_mercury.settings.sleep.timer2, SleepTimerDict)
    assert isinstance(vortex_mercury.settings.sleep.timer2.state, SleepTimer)
    assert isinstance(
        vortex_mercury.settings.sleep.timer2.start, TimeCodedInteger
    )
    assert isinstance(
        vortex_mercury.settings.sleep.timer2.stop, TimeCodedInteger
    )

    assert isinstance(vortex_mercury.settings.time_out, int)


def test_vortex_mercury_settings_data(vortex_mercury: SpaData) -> None:
    """ test Vortex Mercury data """
    assert vortex_mercury.settings.datetime.hours == 13
    assert vortex_mercury.settings.datetime.minutes == 4
    assert vortex_mercury.settings.datetime.seconds == 31
    assert vortex_mercury.settings.datetime.day == 27
    assert vortex_mercury.settings.datetime.month == MonthEnum.JUN
    assert vortex_mercury.settings.datetime.year == 2023

    assert vortex_mercury.settings.filtration.cycle == FiltrationCycle.HR_3
    assert vortex_mercury.settings.filtration.runtime == 4

    assert vortex_mercury.settings.heat_pump.boost == OffOnState.OFF
    assert vortex_mercury.settings.heat_pump.mode == HeatPumpMode.DISABLED

    assert vortex_mercury.settings.lock_mode == LockMode.OFF

    assert vortex_mercury.settings.power_save.state == PowerSave.OFF
    assert vortex_mercury.settings.power_save.peak.start == 3584
    assert vortex_mercury.settings.power_save.peak.start == '14:00'
    assert vortex_mercury.settings.power_save.peak.stop == 5376
    assert vortex_mercury.settings.power_save.peak.stop == '21:00'

    assert vortex_mercury.settings.sleep.timer1.state == SleepTimer.EVERYDAY
    assert vortex_mercury.settings.sleep.timer1.start == 5662
    assert vortex_mercury.settings.sleep.timer1.start == '22:30'
    assert vortex_mercury.settings.sleep.timer1.stop == 1792
    assert vortex_mercury.settings.sleep.timer1.stop == '7:00'
    assert vortex_mercury.settings.sleep.timer2.state == SleepTimer.OFF
    assert vortex_mercury.settings.sleep.timer2.start == 5632
    assert vortex_mercury.settings.sleep.timer2.start == '22:00'
    assert vortex_mercury.settings.sleep.timer2.stop == 1792
    assert vortex_mercury.settings.sleep.timer2.stop == '7:00'

    assert vortex_mercury.settings.time_out == 30
