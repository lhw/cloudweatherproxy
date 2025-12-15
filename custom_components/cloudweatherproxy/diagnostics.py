"""Simple diagnostics option. To be expanded later."""

from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .sensor import CloudWeatherEntity
from .const import DOMAIN
from .aiocloudweather.utils import get_buffered_logs


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return config entry diagnostics."""

    known_sensors: dict[str,
                        CloudWeatherEntity] = hass.data[DOMAIN]["known_sensors"]

    return {
        "known_sensors": known_sensors,  # TODO: String representation sucks
        "entry_data": entry.data,  # TODO: config representation sucks
        "logs": {
            "recent": get_buffered_logs(max_items=200),
        },
    }
