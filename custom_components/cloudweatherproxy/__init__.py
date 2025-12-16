"""The Wunderground Receiver integration."""

from __future__ import annotations

import logging
import contextlib
from dataclasses import dataclass, field

from .aiocloudweather import CloudWeatherListener
from .aiocloudweather.proxy import DataSink
from .aiocloudweather.utils import LimitedSizeQueue, DiagnosticsLogHandler

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DNS_SERVERS, CONF_WEATHERCLOUD_PROXY, CONF_WUNDERGROUND_PROXY, DOMAIN
from .web import WeathercloudReceiver, WundergroundReceiver
from .entity import CloudWeatherEntity

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


@dataclass
class RuntimeData:
    """Runtime data for Cloud Weather Proxy."""

    listener: CloudWeatherListener
    known_sensors: dict[str, CloudWeatherEntity] = field(default_factory=dict)


CloudWeatherProxyConfigEntry = ConfigEntry[RuntimeData]


@dataclass
class DomainData:
    """Domain-wide data for Cloud Weather Proxy."""

    log_queue: LimitedSizeQueue
    log_handler: DiagnosticsLogHandler


async def async_setup_entry(hass: HomeAssistant, entry: CloudWeatherProxyConfigEntry) -> bool:
    """Set up Cloud Weather Proxy from a config entry."""

    proxies = [
        DataSink.WUNDERGROUND] if entry.data[CONF_WUNDERGROUND_PROXY] else []
    proxies += [DataSink.WEATHERCLOUD] if entry.data[CONF_WEATHERCLOUD_PROXY] else []

    dns_servers: list[str] = entry.data[CONF_DNS_SERVERS].split(",")

    _LOGGER.debug("Setting up Cloud Weather Proxy with %s and %s",
                  proxies, dns_servers)
    cloudweather = CloudWeatherListener(
        proxy_sinks=proxies, dns_servers=dns_servers
    )

    # Store per-entry runtime data
    entry.runtime_data = RuntimeData(listener=cloudweather)

    # Initialize domain-wide data on first entry setup
    if DOMAIN not in hass.data:
        # Per-HASS small queue to hold most recent integration logs for diagnostics
        per_hass_queue = LimitedSizeQueue(maxsize=100)

        # Attach integration-scoped diagnostics handler so logs are captured
        # and can be included in the HA diagnostics download.
        handler = DiagnosticsLogHandler(queue=per_hass_queue)
        # Attach to the package logger (custom_components.cloudweatherproxy)
        integration_logger = logging.getLogger(__package__)
        integration_logger.addHandler(handler)

        hass.data[DOMAIN] = DomainData(
            log_queue=per_hass_queue, log_handler=handler)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.http.register_view(WundergroundReceiver(cloudweather))
    hass.http.register_view(WeathercloudReceiver(cloudweather))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: CloudWeatherProxyConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # Cleanup listener resources (proxy session)
        await entry.runtime_data.listener.stop()

        # Check if this is the last config entry for this domain
        remaining_entries = [
            e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id
        ]
        if not remaining_entries and DOMAIN in hass.data:
            # Detach diagnostics handler if present
            domain_data: DomainData = hass.data[DOMAIN]
            integration_logger = logging.getLogger(__package__)
            with contextlib.suppress(Exception):
                integration_logger.removeHandler(domain_data.log_handler)
                domain_data.log_handler.close()

            # Clean up domain-wide data
            hass.data.pop(DOMAIN)

    return unload_ok
