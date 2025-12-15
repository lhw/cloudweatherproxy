"""Proxy for forwarding data to the CloudWeather APIs."""

from enum import Enum
import logging
from aiohttp import web, TCPConnector, ClientSession, ClientResponse
from urllib.parse import parse_qsl, urlencode
from aiohttp.resolver import AsyncResolver

_LOGGER = logging.getLogger(__name__)


class DataSink(Enum):
    """Data sinks for the CloudWeather API."""

    WUNDERGROUND = "wunderground"
    WEATHERCLOUD = "weathercloud"


class CloudWeatherProxy:
    """Proxy for forwarding data to the CloudWeather API."""

    def __init__(self, proxied_sinks: list[DataSink], dns_servers: list[str]):
        """Initialize CloudWeatherProxy."""
        resolver = AsyncResolver(nameservers=dns_servers)
        self.proxied_sinks = proxied_sinks
        self.session = ClientSession(connector=TCPConnector(resolver=resolver))

    async def close(self):
        """Close the session."""
        if not self.session.closed:
            await self.session.close()

    async def forward_wunderground(self, request: web.Request) -> ClientResponse:
        """Forward Wunderground data to their API."""
        if not request.query_string:
            _LOGGER.error(
                "Wunderground request missing query string: %s", request.path
            )
            raise web.HTTPBadRequest(
                text="Missing query string for Wunderground request")

        pairs = parse_qsl(request.query_string, keep_blank_values=True)
        query_string = urlencode(pairs, doseq=True)

        url = (
            f"https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?{query_string}"
        )
        _LOGGER.debug("Forwarding Wunderground data: %s", url)
        return await self.session.get(url)

    async def forward_weathercloud(self, request: web.Request) -> ClientResponse:
        """Forward WeatherCloud data to their API."""
        new_path = request.path[request.path.index("/v01/set"):]
        # If there's no dataset in the path (e.g. just /v01/set) and no
        # query string, nothing useful can be forwarded.
        path_after = new_path[len("/v01/set"):]
        if (not path_after or path_after == "/") and not request.query_string:
            _LOGGER.error(
                "WeatherCloud request missing payload: %s", request.path
            )
            raise web.HTTPBadRequest(
                text="Missing path payload for WeatherCloud request")

        url = f"https://api.weathercloud.net{new_path}"
        if request.query_string:
            pairs = parse_qsl(request.query_string, keep_blank_values=True)
            query_string = urlencode(pairs, doseq=True)
            url = f"{url}?{query_string}"
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
