"""Simple diagnostics option. To be expanded later."""

from typing import Any
from homeassistant.core import HomeAssistant

from . import CloudWeatherProxyConfigEntry, DomainData
from .entity import CloudWeatherEntity
from .const import DOMAIN, CONF_WUNDERGROUND_PROXY, CONF_WEATHERCLOUD_PROXY, CONF_DNS_SERVERS


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: CloudWeatherProxyConfigEntry) -> dict[str, Any]:
    """Return config entry diagnostics."""

    runtime_data = entry.runtime_data
    known_sensors: dict[str, CloudWeatherEntity] = runtime_data.known_sensors

    # Get the per-HASS log queue from domain-wide data
    logs = []
    if DOMAIN in hass.data:
        domain_data: DomainData = hass.data[DOMAIN]
        log_queue = domain_data.log_queue
        if log_queue:
            # Access underlying deque of asyncio.Queue
            items = list(getattr(log_queue, "_queue", []))
            logs = items[-100:]

    # Format known_sensors for human readability with masked station IDs
    # Create a mapping of station IDs to unique identifiers to prevent collisions
    station_id_mapping: dict[str, str] = {}
    station_counter = 1

    formatted_sensors = {}
    for unique_id, entity in known_sensors.items():
        station_id = entity.station.station_id
        if station_id not in station_id_mapping:
            station_id_mapping[station_id] = f"station_{station_counter}"
            station_counter += 1

        masked_key = unique_id.replace(
            station_id, station_id_mapping[station_id], 1)

        formatted_sensors[masked_key] = {
            "name": entity.name,
            "sensor_name": entity.sensor.name if entity.sensor else None,
            "value": entity.sensor.value if entity.sensor else None,
            "unit": entity.sensor.unit if entity.sensor else None,
            "available": entity.available,
            "enabled": entity.enabled,
        }

    formatted_entry_data = {
        "proxy_wunderground": entry.data.get(CONF_WUNDERGROUND_PROXY, False),
        "proxy_weathercloud": entry.data.get(CONF_WEATHERCLOUD_PROXY, False),
        "dns_servers": entry.data.get(CONF_DNS_SERVERS, ""),
    }

    return {
        "known_sensors": formatted_sensors,
        "entry_data": formatted_entry_data,
        "logs": {
            "recent": logs,
        },
    }
