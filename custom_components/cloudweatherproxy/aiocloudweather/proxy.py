"""Proxy for forwarding data to the CloudWeather APIs."""

from enum import Enum
import logging
from aiohttp import web, TCPConnector, ClientSession, ClientResponse
from urllib.parse import quote
from aiohttp.resolver import AsyncResolver

_LOGGER = logging.getLogger(__name__)


class DataSink(Enum):
    """Data sinks for the CloudWeather API."""

    WUNDERGROUND = "wunderground"
    WEATHERCLOUD = "weathercloud"


class CloudWeatherProxy:
    """Proxy for forwarding data to the CloudWeather API."""

    def __init__(self, proxied_sinks: list[DataSink], dns_servers: list[str]):
        resolver = AsyncResolver(nameservers=dns_servers)
        self.proxied_sinks = proxied_sinks
        self.session = ClientSession(connector=TCPConnector(resolver=resolver))

    async def close(self):
        """Close the session."""
        if not self.session.closed:
            await self.session.close()

    async def forward_wunderground(self, request: web.Request) -> ClientResponse:
        """Forward Wunderground data to their API."""
        if "%" in request.query_string:
            query_string = request.query_string
        else:
            query_string = quote(request.query_string).replace("%20", "+")
        url = f"https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?{query_string}"
        _LOGGER.debug("Forwarding Wunderground data: %s", url)
        return await self.session.get(url)

    async def forward_weathercloud(self, request: web.Request) -> ClientResponse:
        """Forward WeatherCloud data to their API."""
        new_path = request.path[request.path.index("/v01/set"):]
        url = f"https://api.weathercloud.net{new_path}"
        _LOGGER.debug("Forwarding WeatherCloud data: %s", url)
        return await self.session.get(url)

    async def forward(self, sink: DataSink, request: web.Request) -> ClientResponse:
        """Forward data to the CloudWeather API."""
        if (
            sink == DataSink.WUNDERGROUND
            and DataSink.WUNDERGROUND in self.proxied_sinks
        ):
            return await self.forward_wunderground(request)
        if (
            sink == DataSink.WEATHERCLOUD
            and DataSink.WEATHERCLOUD in self.proxied_sinks
        ):
            return await self.forward_weathercloud(request)

        raise ValueError(f"Sink {sink} is not enabled or supported")
