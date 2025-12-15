"""Simple diagnostics option. To be expanded later."""

from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .sensor import CloudWeatherEntity
from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Return config entry diagnostics."""

    known_sensors: dict[str,
                        CloudWeatherEntity] = hass.data[DOMAIN]["known_sensors"]

    # Get the per-HASS log queue
    log_queue = hass.data[DOMAIN].get("log_queue")
    logs = []
    if log_queue:
        # Access underlying deque of asyncio.Queue
        items = list(getattr(log_queue, "_queue", []))
        logs = items[-100:]

    return {
        "known_sensors": known_sensors,  # TODO: String representation sucks
        "entry_data": entry.data,  # TODO: config representation sucks
        "logs": {
            "recent": logs,
        },
    }
