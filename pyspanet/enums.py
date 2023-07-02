""" pyspanet.enums """
from __future__ import annotations

from enum import IntEnum, unique
from strenum import StrEnum


@unique
class BlowerState(IntEnum):
    """ BlowerState """
    VARIABLE = 0
    RAMP = 1
    OFF = 2


@unique
class BlowerSpeed(IntEnum):
    """" BlowerSpeed """
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5


@unique
class MonthEnum(IntEnum):
    """ MonthEnum """
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


@unique
class FiltrationCycle(IntEnum):
    """ FiltrationCycle """
    HR_1 = 1
    HR_2 = 2
    HR_3 = 3
    HR_4 = 4
    HR_6 = 6
    HR_8 = 8
    HR_12 = 12
    HR_24 = 24


@unique
class FiltrationRuntime(IntEnum):
    """ FiltrationRuntime """
    HOURS_1 = 1
    HOURS_2 = 2
    HOURS_3 = 3
    HOURS_4 = 4
    HOURS_5 = 5
    HOURS_6 = 6
    HOURS_7 = 7
    HOURS_8 = 8
    HOURS_9 = 9
    HOURS_10 = 10
    HOURS_11 = 11
    HOURS_12 = 12
    HOURS_13 = 13
    HOURS_14 = 14
    HOURS_15 = 15
    HOURS_16 = 16
    HOURS_17 = 17
    HOURS_18 = 18
    HOURS_19 = 19
    HOURS_20 = 20
    HOURS_21 = 21
    HOURS_22 = 22
    HOURS_23 = 23
    HOURS_24 = 24


@unique
class HeatPumpMode(IntEnum):
    """ HeatPumpMode """
    AUTO = 0
    HEAT = 1
    COOL = 2
    DISABLED = 3


@unique
class LightBrightness(IntEnum):
    """ LightBrightness """
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5


@unique
class LightColour(IntEnum):
    """ LightColour """
    COLOUR_0 = 0
    COLOUR_1 = 1
    COLOUR_2 = 2
    COLOUR_3 = 3
    COLOUR_4 = 4
    COLOUR_5 = 5
    COLOUR_6 = 6
    COLOUR_7 = 7
    COLOUR_8 = 8
    COLOUR_9 = 9
    COLOUR_10 = 10
    COLOUR_11 = 11
    COLOUR_12 = 12
    COLOUR_13 = 13
    COLOUR_14 = 14
    COLOUR_15 = 15
    COLOUR_16 = 16
    COLOUR_17 = 17
    COLOUR_18 = 18
    COLOUR_19 = 19
    COLOUR_20 = 20
    COLOUR_21 = 21
    COLOUR_22 = 22
    COLOUR_23 = 23
    COLOUR_24 = 24
    COLOUR_25 = 25
    COLOUR_26 = 26
    COLOUR_27 = 27
    COLOUR_28 = 28
    COLOUR_29 = 29
    COLOUR_30 = 30


@unique
class LightEffect(IntEnum):
    """ LightEffect """
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5


@unique
class LightMode(IntEnum):
    """ LightMode """
    WHITE = 0
    COLOUR = 1
    FADE = 2
    STEP = 3
    PARTY = 4


@unique
class LockMode(IntEnum):
    """ LockMode """
    OFF = 0
    PARTIAL = 1
    FULL = 2


@unique
class OffOnState(IntEnum):
    """ OffOnState """
    OFF = 0
    ON = 1


@unique
class OffOnAutoState(IntEnum):
    """ OffOnAutoState """
    OFF = 0
    ON = 1
    AUTO = 4


@unique
class OffLowAutoState(IntEnum):
    """ OffLowAutoState """
    OFF = 0
    LOW = 3
    AUTO = 4


@unique
class OffHighLowState(IntEnum):
    """ OffHighLowState """
    OFF = 0
    HIGH = 2
    LOW = 3


@unique
class HighLowState(IntEnum):
    """ HighLowState """
    HIGH = 2
    LOW = 3


@unique
class OperationMode(IntEnum):
    """ OperationMode """
    NORM = 0
    ECON = 1
    AWAY = 2
    WEEK = 3


@unique
class PowerSave(IntEnum):
    """ PowerSave """
    OFF = 0
    LOW = 1
    HIGH = 2


@unique
class PumpType(IntEnum):
    """ PumpType """
    UNKNOWN = 0
    ONE_SPEED = 1
    TWO_SPEED = 2


@unique
class SleepTimer(IntEnum):
    """ SleepTimer """
    OFF = 128
    EVERYDAY = 127
    WEEKENDS = 96
    WEEKDAYS = 31


@unique
class StateLabel(StrEnum):
    """ StateLabel """
    AUTO = 'Auto'
    CLEAN = 'W.CLN'
    FILTERING = 'Filtering'
    HEATING = 'Heating'
    IN_USE = 'In use'
    SLEEPING = 'Sleeping'
