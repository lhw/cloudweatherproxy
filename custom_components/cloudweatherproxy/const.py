"""Constants for the Cloud Weather Proxy."""

from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    DEGREE,
    LIGHT_LUX,
    PERCENTAGE,
    UV_INDEX,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolumetricFlux,
)

DOMAIN = "cloudweatherproxy"

UNIT_DESCRIPTION_MAPPING: Final = {
    UnitOfPressure.HPA: SensorEntityDescription(
        key="PRESSURE_HPA",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfPressure.INHG: SensorEntityDescription(
        key="PRESSURE_INHG",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.INHG,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfTemperature.CELSIUS: SensorEntityDescription(
        key="TEMPERATURE_C",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfTemperature.FAHRENHEIT: SensorEntityDescription(
        key="TEMPERATURE_F",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfPrecipitationDepth.MILLIMETERS: SensorEntityDescription(
        key="RAIN_MM",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    UnitOfPrecipitationDepth.INCHES: SensorEntityDescription(
        key="RAIN_IN",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.INCHES,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
    ),
    UnitOfSpeed.METERS_PER_SECOND: SensorEntityDescription(
        key="WIND_SPEED_MS",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.METERS_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfSpeed.MILES_PER_HOUR: SensorEntityDescription(
        key="WIND_SPEED_MPH",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfIrradiance.WATTS_PER_SQUARE_METER: SensorEntityDescription(
        key="SOLAR_RADIATION_W_M2",
        device_class=SensorDeviceClass.IRRADIANCE,
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    LIGHT_LUX: SensorEntityDescription(
        key="LIGHT_LUX",
        device_class=SensorDeviceClass.ILLUMINANCE,
        native_unit_of_measurement=LIGHT_LUX,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR: SensorEntityDescription(
        key="RAIN_RATE_MM",
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        native_unit_of_measurement=UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    UnitOfVolumetricFlux.INCHES_PER_HOUR: SensorEntityDescription(
        key="RAIN_RATE_IN",
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        native_unit_of_measurement=UnitOfVolumetricFlux.INCHES_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    DEGREE: SensorEntityDescription(
        key="WIND_DIRECTION",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PERCENTAGE: SensorEntityDescription(
        key="HUMIDITY",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    UV_INDEX: SensorEntityDescription(
        key="UV_INDEX",
        state_class=SensorStateClass.MEASUREMENT,
    ),
}

CONF_WUNDERGROUND_PROXY: Final = "weatherunderground_proxy"
CONF_WEATHERCLOUD_PROXY: Final = "weathercloud_proxy"
CONF_DNS_SERVERS: Final = "dns_servers"
