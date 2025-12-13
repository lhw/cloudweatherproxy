"""The web server for the CloudWeatherProxy integration."""

from http import HTTPStatus
import logging

from .aiocloudweather import CloudWeatherListener
from aiohttp import web
from aiohttp.web_exceptions import HTTPClientError

from homeassistant.helpers.http import HomeAssistantView
from homeassistant.helpers.http import KEY_AUTHENTICATED

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class WundergroundReceiver(HomeAssistantView):
    """Wunderground receiver."""

    name = f"api:{DOMAIN}:wunderground"
    url = "/wunderground/weatherstation/updateweatherstation.php"

    def __init__(self, listener: CloudWeatherListener) -> None:
        """Initialize the Wunderground receiver."""
        self.listener = listener

    async def get(
        self,
        request: web.Request,
    ) -> web.Response:
        """Handle Wunderground request."""

        if not request[KEY_AUTHENTICATED]:
            return web.Response(status=HTTPStatus.UNAUTHORIZED)

        try:
            return await self.listener.handler(request)
        except HTTPClientError as e:
            _LOGGER.error(e)
            return web.Response(status=HTTPStatus.BAD_REQUEST)


class WeathercloudReceiver(HomeAssistantView):
    """Weathercloud receiver."""

    name = f"api:{DOMAIN}:weathercloud"
    url = "/weathercloud/v01/set/{values:.*}"

    def __init__(self, listener: CloudWeatherListener) -> None:
        """Initialize the Weathercloud receiver."""
        self.listener = listener

    async def get(
        self,
        request: web.Request,
        values: str,
    ) -> web.Response:
        """Handle Weathercloud request."""

        if not request[KEY_AUTHENTICATED]:
            return web.Response(status=HTTPStatus.UNAUTHORIZED)

        try:
            return await self.listener.handler(request)
        except HTTPClientError as e:
            _LOGGER.error(e)
            return web.Response(status=HTTPStatus.BAD_REQUEST)
