"""Tests module."""
from __future__ import annotations

from pyspanet.collections import FloatCodedInteger, TimeCodedInteger


def test_float_coded_integer() -> None:
    """ test FloatCodedIntegers """
    fci = FloatCodedInteger(325)
    assert fci == 325
    assert int(fci) == 325
    assert fci == 32.5
    assert float(fci) == 32.5
    assert fci == '32.5'
    assert str(fci) == '32.5'

    fci = FloatCodedInteger(26.7)
    assert fci == 267
    assert int(fci) == 267
    assert fci == 26.7
    assert float(fci) == 26.7
    assert fci == '26.7'
    assert str(fci) == '26.7'

    fci = FloatCodedInteger('19.8')
    assert fci == 198
    assert int(fci) == 198
    assert fci == 19.8
    assert float(fci) == 19.8
    assert fci == '19.8'
    assert str(fci) == '19.8'


def test_time_coded_integer() -> None:
    """ test TimeCodedIntegers """
    tci = TimeCodedInteger(5120)
    assert tci == 5120
    assert int(tci) == 5120
    assert tci == '20:00'
    assert str(tci) == '20:00'

    tci = TimeCodedInteger('7:45')
    assert tci == 1837
    assert int(tci) == 1837
    assert tci == '7:45'
    assert str(tci) == '7:45'

    # bounds checking
    tci = TimeCodedInteger(-1)
    assert tci != -1
    assert tci == 0

    # bounds checking
    tci = TimeCodedInteger(5948)
    assert tci != 5948
    assert tci == 5947
