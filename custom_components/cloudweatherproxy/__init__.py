"""The Wunderground Receiver integration."""

from aiocloudweather import CloudWeatherListener

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .web import WeathercloudReceiver, WundergroundReceiver

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cloud Weather Proxy from a config entry."""

    cloudweather = hass.data.setdefault(DOMAIN, {})[entry.entry_id] = (
        CloudWeatherListener()
    )
    hass.data[DOMAIN].setdefault("known_sensors", {})

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.http.register_view(WundergroundReceiver(cloudweather))
    hass.http.register_view(WeathercloudReceiver(cloudweather))

    # async def handle_webhook(
    #     hass: HomeAssistant, webhook_id: str, request: web.Request
    # ) -> web.Response:
    #     """Handle webhook callback."""
    #     log = logging.getLogger(__name__)

    #     log.info("Received webhook request")
    #     log.info(request.path)
    #     log.info(request.query)

    #     return await cloudweather.handler(request)

    # webhook.async_register(
    #     hass,
    #     DOMAIN,
    #     entry.title,
    #     entry.data[CONF_WEBHOOK_ID],
    #     handle_webhook,
    #     allowed_methods=["GET"],
    # )

    # @callback
    # def _stop_CloudWeatherProxy(_: Event) -> None:
    #     """Stop the Cloud Weather Proxy listener."""
    #     webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    # entry.async_on_unload(
    #     hass.bus.async_listen_once(
    #         EVENT_HOMEASSISTANT_STOP, _stop_CloudWeatherProxy
    #     )
    # )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
