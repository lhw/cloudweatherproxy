"""Config flow for Cloud Weather Proxy."""

from __future__ import annotations

from typing import Any

import voluptuous as vol


from yarl import URL

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, ConfigEntry, OptionsFlow
# from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.network import get_url

from .const import CONF_WUNDERGROUND_PROXY, CONF_WEATHERCLOUD_PROXY, CONF_DNS_SERVERS, DOMAIN


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

    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="Cloud Weather Proxy", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_WUNDERGROUND_PROXY): bool,
                    vol.Required(CONF_WEATHERCLOUD_PROXY): bool,
                    vol.Optional(CONF_DNS_SERVERS, default="9.9.9.9"): str,
                }
            ),
        )
