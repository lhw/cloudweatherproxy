"""Config flow for Cloud Weather Proxy."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from aiocloudweather import CloudWeatherListener
from aiocloudweather.proxy import DataSink


from yarl import URL

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, ConfigEntry
# from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.network import get_url

from .const import CONF_WUNDERGROUND_PROXY, CONF_WEATHERCLOUD_PROXY, CONF_DNS_SERVERS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class CloudWeatherProxyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the Cloud Weather Proxy."""

    VERSION = 1

    # async def validate_input(hself, ass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    #     return {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if self._async_current_entries():
                return self.async_abort(reason="single_instance")

            # await self.validate_input(self.hass, user_input)
            base_url = URL(get_url(self.hass))
            assert base_url.host

            return self.async_create_entry(
                title="Cloud Weather Proxy",
                data=user_input,
                description_placeholders={
                    "address": base_url.host, "port": str(base_url.port)
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_WUNDERGROUND_PROXY): bool,
                    vol.Required(CONF_WEATHERCLOUD_PROXY): bool,
                    vol.Optional(CONF_DNS_SERVERS, default="9.9.9.9"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Add reconfigure step to allow to reconfigure a config entry."""

        config_entry: ConfigEntry = self._get_reconfigure_entry()
        listener: CloudWeatherListener = self.hass.data[DOMAIN][config_entry.entry_id]
        _LOGGER.debug("Reconfiguring Cloud Weather Proxy: %s", listener)
        current_proxy_settings = listener.get_active_proxies()
        current_dns_servers = listener.get_dns_servers()
        _LOGGER.debug("Current configuration: %s and proxies %s",
                      current_proxy_settings, current_dns_servers)

        if user_input is not None:
            _LOGGER.debug(
                "Reconfiguring Cloud Weather Proxy with %s", user_input)
            await listener.update_config(
                proxy_sinks=[
                    DataSink.WUNDERGROUND if user_input[CONF_WUNDERGROUND_PROXY] else None,
                    DataSink.WEATHERCLOUD if user_input[CONF_WEATHERCLOUD_PROXY] else None,
                ],
                dns_servers=user_input[CONF_DNS_SERVERS].split(",")
            )
            self._abort_if_unique_id_mismatch()
            return self.async_update_reload_and_abort(
                config_entry,
                data_updates={
                    CONF_WUNDERGROUND_PROXY: user_input[CONF_WUNDERGROUND_PROXY],
                    CONF_WEATHERCLOUD_PROXY: user_input[CONF_WEATHERCLOUD_PROXY],
                    CONF_DNS_SERVERS: user_input[CONF_DNS_SERVERS],
                },
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_WUNDERGROUND_PROXY, default=(DataSink.WUNDERGROUND in current_proxy_settings)): bool,
                    vol.Required(CONF_WEATHERCLOUD_PROXY, default=(DataSink.WEATHERCLOUD in current_proxy_settings)): bool,
                    vol.Optional(CONF_DNS_SERVERS, default=",".join(current_dns_servers)): str,
                }
            ),
        )
