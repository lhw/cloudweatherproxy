"""Config flow for Cloud Weather Proxy."""

from __future__ import annotations

from typing import Any

from yarl import URL

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.network import get_url

from .const import DOMAIN


class CloudWeatherProxyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the Ecowitt."""

    VERSION = 1
    # _webhook_id: str

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            # self._webhook_id = secrets.token_hex(16)
            return self.async_show_form(
                step_id="user",
                # data_schema=vol.Schema(
                #     {
                #         vol.Required("provider"): selector(
                #             {
                #                 "select": {
                #                     "options": ["Wunderground", "Weathercloud"],
                #                 }
                #             }
                #         )
                #     }
                # ),
            )

        base_url = URL(get_url(self.hass))
        assert base_url.host

        return self.async_create_entry(
            title="Cloud Weather Proxy",
            data={
                # CONF_WEBHOOK_ID: self._webhook_id,
                # "provider": user_input["provider"],
            },
            description_placeholders={
                # "path": webhook.async_generate_path(self._webhook_id),
                # "server": base_url.host,
                # "port": str(base_url.port),
                # "provider": user_input["provider"],
            },
        )


class InvalidPort(HomeAssistantError):
    """Error to indicate there port is not usable."""
