"""Config flow for Cloud Weather Proxy."""

from __future__ import annotations

from typing import Any

import voluptuous as vol


from yarl import URL

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.network import get_url

from .const import CONF_WUNDERGROUND_PROXY, CONF_WEATHERCLOUD_PROXY, CONF_DNS_SERVERS, DOMAIN


class CloudWeatherProxyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the Cloud Weather Proxy."""

    VERSION = 1

    async def validate_input(hself, ass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
        return {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await self.validate_input(self.hass, user_input)
            except InvalidInput:
                errors["base"] = "invalid_input"
            else:
                base_url = URL(get_url(self.hass))
                assert base_url.host

                return self.async_create_entry(
                    title="Cloud Weather Proxy",
                    data=user_input,
                    description_placeholders={
                        "server": base_url.host,
                        "port": str(base_url.port),
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


class InvalidInput(HomeAssistantError):
    """Error to indicate there port is not usable."""
