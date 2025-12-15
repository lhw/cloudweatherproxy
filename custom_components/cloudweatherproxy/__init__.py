"""The Wunderground Receiver integration."""

import logging
import contextlib
from .aiocloudweather import CloudWeatherListener
from .aiocloudweather.proxy import DataSink
from .aiocloudweather.utils import LimitedSizeQueue, DiagnosticsLogHandler

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

    dns_servers: list[str] = entry.data[CONF_DNS_SERVERS].split(",")

    _LOGGER.debug("Setting up Cloud Weather Proxy with %s and %s",
                  proxies, dns_servers)
    cloudweather = hass.data.setdefault(DOMAIN, {})[entry.entry_id] = (
        CloudWeatherListener(proxy_sinks=proxies,
                             dns_servers=dns_servers)
    )
    hass.data[DOMAIN].setdefault("known_sensors", {})
    # Per-HASS small queue to hold most recent integration logs for diagnostics
    per_hass_queue = hass.data[DOMAIN].setdefault(
        "log_queue", LimitedSizeQueue(maxsize=100))

    # Attach integration-scoped diagnostics handler so logs are captured
    # and can be included in the HA diagnostics download.
    handler = DiagnosticsLogHandler(queue=per_hass_queue)
    # Attach to the package logger (custom_components.cloudweatherproxy)
    integration_logger = logging.getLogger(__package__)
    integration_logger.addHandler(handler)
    hass.data[DOMAIN]["log_handler"] = handler

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.http.register_view(WundergroundReceiver(cloudweather))
    hass.http.register_view(WeathercloudReceiver(cloudweather))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Detach diagnostics handler if present
        handler = hass.data[DOMAIN].pop("log_handler", None)
        if handler is not None:
            integration_logger = logging.getLogger(__package__)
            with contextlib.suppress(Exception):
                integration_logger.removeHandler(handler)
                handler.close()

        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
