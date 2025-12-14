import pytest
from aiohttp import web
from aiocloudweather.server import CloudWeatherListener


@pytest.fixture
async def client(aiohttp_client):
    app = web.Application()
    listener = CloudWeatherListener()
    app.router.add_get("/weatherstation/updateweatherstation.php", listener.handler)
    app.router.add_get("/v01/set/{path:.*}", listener.handler)
    await listener.start()
    client = await aiohttp_client(app)
    try:
        yield client
    finally:
        await listener.stop()
        await client.close()


@pytest.mark.asyncio
async def test_handler(client):
    data_files = ["tests/data/weathercloud", "tests/data/wunderground"]

    async def test_request(client, request_url):
        response = await client.get(request_url)
        assert response.status == 200
        assert await response.text() == "OK"

    async for c in client:
        for file_path in data_files:
            with open(file_path, "r") as file:
                for line in file:
                    request_url = line.strip()
                    await test_request(c, request_url)
