"""Registering Cloud Weather Proxy Weather Stations."""

from dataclasses import fields
import logging
import time

from aiocloudweather import CloudWeatherListener, Sensor, WeatherStation

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.unit_system import US_CUSTOMARY_SYSTEM, UnitSystem

from .const import DOMAIN, UNIT_DESCRIPTION_MAPPING

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Register new weather stations."""
    cloudweather: CloudWeatherListener = hass.data[DOMAIN][entry.entry_id]

    async def _new_dataset(station: WeatherStation) -> None:
        known_sensors: dict[str, CloudWeatherEntity] = hass.data[DOMAIN][
            "known_sensors"
        ]
        new_sensors: list[CloudWeatherEntity] = []

        for field in fields(station):
            if field.type is not Sensor:
                continue
            sensor: Sensor = getattr(station, field.name)
            if sensor is None:
                continue
            unique_id = f"{station.station_id}-{sensor.name}"

            if unique_id in known_sensors:
                await known_sensors[unique_id].update_sensor(station)
                continue

            new_sensor = CloudWeatherEntity(
                sensor, station, hass.config.units, str(
                    field.metadata.get("name"))
            )
            known_sensors[unique_id] = new_sensor
            new_sensors.append(new_sensor)

        if len(new_sensors) > 0:
            _LOGGER.debug("Adding %d sensors", len(new_sensors))
            async_add_entities(new_sensors)
        for nsensor in new_sensors:
            nsensor.async_write_ha_state()

        hass.data[DOMAIN]["known_sensors"] = known_sensors

    cloudweather.new_dataset_cb.append(_new_dataset)
    entry.async_on_unload(
        lambda: cloudweather.new_dataset_cb.remove(_new_dataset))


class CloudWeatherBaseEntity(Entity):
    """The Cloud Weather Proxy Entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, sensor: Sensor, station: WeatherStation) -> None:
        """Construct the entity."""
        self.sensor = sensor
        self.station = station

        self._attr_unique_id = f"{station.station_id}-{sensor.name}"
        self._attr_device_info = DeviceInfo(
            name=f"Weatherstation {station.station_id}",
            identifiers={(DOMAIN, station.station_id)},
            sw_version=station.station_sw_version,
            manufacturer=station.vendor,
        )

    @property
    def available(self) -> bool:
        """Return whether the state is based on actual reading from device."""
        return (self.station.update_time + 5 * 60) > time.monotonic()


class CloudWeatherEntity(CloudWeatherBaseEntity, SensorEntity):
    """The Cloud Weather Proxy Sensor Entity."""

    def __init__(
        self,
        sensor: Sensor,
        station: WeatherStation,
        unit_system: UnitSystem,
        name: str,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(sensor, station)
        self.unit_system = unit_system
        self._name = name
        if unit_system is US_CUSTOMARY_SYSTEM:
            description = UNIT_DESCRIPTION_MAPPING[sensor.imperial_unit]
        else:
            description = UNIT_DESCRIPTION_MAPPING[sensor.metric_unit]
        self.entity_description = description

    @property
    def native_value(self) -> StateType | None:
        """Return the state of the entity."""
        if self.unit_system is US_CUSTOMARY_SYSTEM:
            return self.sensor.imperial
        return self.sensor.metric

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    async def update_sensor(self, station: WeatherStation) -> None:
        """Update the entity."""
        self.station = station
        self.sensor = getattr(station, self.sensor.name)
        _LOGGER.debug("Updating %s [%s] with update time %s",
                      self.unique_id, self.sensor, self.station.update_time)
        self.async_write_ha_state()
