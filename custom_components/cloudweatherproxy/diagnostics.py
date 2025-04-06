from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .sensor import CloudWeatherEntity
from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return config entry diagnostics."""

    known_sensors: dict[str,
                        CloudWeatherEntity] = hass.data[DOMAIN]["known_sensors"]

    return {
        "known_sensors": known_sensors,  # TODO: String representation sucks
        "entry_data": entry.data,  # TODO: config representation sucks
    }
