"""The Wunderground Receiver integration."""

import logging
from aiocloudweather import CloudWeatherListener
from aiocloudweather.proxy import DataSink

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DNS_SERVERS, CONF_WEATHERCLOUD_PROXY, CONF_WUNDERGROUND_PROXY, DOMAIN
from .web import WeathercloudReceiver, WundergroundReceiver

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cloud Weather Proxy from a config entry."""

    proxies = [
        DataSink.WUNDERGROUND] if entry.data[CONF_WUNDERGROUND_PROXY] else []
    proxies += [DataSink.WEATHERCLOUD] if entry.data[CONF_WEATHERCLOUD_PROXY] else []

    dns_servers = entry.data[CONF_DNS_SERVERS]

    _LOGGER.debug("Setting up Cloud Weather Proxy with %s and %s",
                  proxies, dns_servers)
    cloudweather = hass.data.setdefault(DOMAIN, {})[entry.entry_id] = (
        CloudWeatherListener(proxy_sinks=proxies,
                             dns_servers=dns_servers.split(","))
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
