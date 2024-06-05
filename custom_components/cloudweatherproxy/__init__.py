"""The Wunderground Receiver integration."""

from aiocloudweather import CloudWeatherListener

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DNS_SERVERS, CONF_WEATHERCLOUD_PROXY, CONF_WUNDERGROUND_PROXY, DOMAIN
from .web import WeathercloudReceiver, WundergroundReceiver

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cloud Weather Proxy from a config entry."""

    proxy_enabled = entry.data[CONF_WUNDERGROUND_PROXY] or entry.data[CONF_WEATHERCLOUD_PROXY]
    dns_servers = entry.data[CONF_DNS_SERVERS]
    cloudweather = hass.data.setdefault(DOMAIN, {})[entry.entry_id] = (
        CloudWeatherListener(proxy_enabled=proxy_enabled, dns_servers=dns_servers.split(","))
    )
    hass.data[DOMAIN].setdefault("known_sensors", {})

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.http.register_view(WundergroundReceiver(cloudweather))
    hass.http.register_view(WeathercloudReceiver(cloudweather))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
