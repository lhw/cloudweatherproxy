"""A list of all the unit conversions. Many are just approximations."""

from .const import (
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)

# Prefer Home Assistant's unit conversion helpers when running inside HA.
try:
    from homeassistant.util.unit_conversion import (
        fahrenheit_to_celsius as _ha_fahrenheit_to_celsius,
        inhg_to_hpa as _ha_inhg_to_hpa,
        in_to_mm as _ha_in_to_mm,
        mph_to_ms as _ha_mph_to_ms,
    )
except Exception:
    _ha_fahrenheit_to_celsius = None
    _ha_inhg_to_hpa = None
    _ha_in_to_mm = None
    _ha_mph_to_ms = None


def unit(output_unit):
    """Set the output unit of the function."""

    def decorator(func):
        func.unit = output_unit
        return func

    return decorator


# imperial shenanigans
@unit(UnitOfTemperature.CELSIUS)
def fahrenheit_to_celsius(temp_f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    if _ha_fahrenheit_to_celsius is not None:
        return _ha_fahrenheit_to_celsius(temp_f)

    return (temp_f - 32) * 5.0 / 9.0


@unit(UnitOfPressure.HPA)
def inhg_to_hpa(pressure: float) -> float:
    """Convert inches of mercury (inHg) to hectopascals (hPa)."""
    if _ha_inhg_to_hpa is not None:
        return _ha_inhg_to_hpa(pressure)

    return pressure * 33.864


@unit(UnitOfPrecipitationDepth.MILLIMETERS)
def in_to_mm(length: float) -> float:
    """Convert inches to millimeters (mm)."""
    if _ha_in_to_mm is not None:
        return _ha_in_to_mm(length)

    return length * 25.4


@unit(UnitOfSpeed.METERS_PER_SECOND)
def mph_to_ms(speed: float) -> float:
    """Convert miles per hour (mph) to meters per second (m/s)."""
    if _ha_mph_to_ms is not None:
        return _ha_mph_to_ms(speed)

    return speed * 0.44704
