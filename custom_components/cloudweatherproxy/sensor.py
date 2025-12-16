"""Registering Cloud Weather Proxy Weather Stations."""

from __future__ import annotations

from dataclasses import fields
from .aiocloudweather.utils import resolve_caster
import logging

from .aiocloudweather import CloudWeatherListener, Sensor, WeatherStation

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CloudWeatherProxyConfigEntry
from .entity import CloudWeatherEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: CloudWeatherProxyConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Register new weather stations."""
    runtime_data = entry.runtime_data
    cloudweather: CloudWeatherListener = runtime_data.listener

    async def _new_dataset(station: WeatherStation) -> None:
        known_sensors: dict[str,
                            CloudWeatherEntity] = runtime_data.known_sensors
        new_sensors: list[CloudWeatherEntity] = []

        for field in fields(station):
            field_type = field.type
            caster = resolve_caster(field_type)
            if caster is not Sensor and caster is not None:
                if getattr(caster, "__name__", "") != getattr(Sensor, "__name__", ""):
                    continue
            elif caster is None:
                continue
            sensor: Sensor | None = getattr(station, field.name)
            if sensor is None:
                continue
            unique_id = f"{station.station_id}-{sensor.name}"

            if unique_id in known_sensors:
                await known_sensors[unique_id].update_sensor(station)
                continue

            meta_name = field.metadata.get("name") or sensor.name
            new_sensor = CloudWeatherEntity(sensor, station, str(meta_name))
            known_sensors[unique_id] = new_sensor
            new_sensors.append(new_sensor)

        if len(new_sensors) > 0:
            _LOGGER.debug("Adding %d sensors", len(new_sensors))
            async_add_entities(new_sensors)
        for nsensor in new_sensors:
            nsensor.async_write_ha_state()

    cloudweather.new_dataset_cb.append(_new_dataset)
    entry.async_on_unload(
        lambda: cloudweather.new_dataset_cb.remove(_new_dataset))
