from aiocloudweather.conversion import (
    fahrenheit_to_celsius,
    in_to_mm,
    inhg_to_hpa,
    mph_to_ms,
)


def test_fahrenheit_to_celsius():
    assert round(fahrenheit_to_celsius(32), 2) == 0
    assert round(fahrenheit_to_celsius(212), 2) == 100
    assert round(fahrenheit_to_celsius(50), 2) == 10


def test_inhg_to_hpa():
    assert round(inhg_to_hpa(29.92), 2) == 1013.21
    assert round(inhg_to_hpa(30), 2) == 1015.92
    assert round(inhg_to_hpa(28), 2) == 948.19


def test_in_to_mm():
    assert round(in_to_mm(1), 2) == 25.4
    assert round(in_to_mm(2.5), 2) == 63.5
    assert round(in_to_mm(0.5), 2) == 12.7


def test_mph_to_ms():
    assert round(mph_to_ms(10), 4) == 4.4704
    assert round(mph_to_ms(30), 4) == 13.4112
    assert round(mph_to_ms(5), 4) == 2.2352
