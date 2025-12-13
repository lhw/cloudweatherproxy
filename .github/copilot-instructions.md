# Cloud Weather Proxy - AI Coding Instructions

## Project Overview
This is a Home Assistant custom component (`cloudweatherproxy`) that intercepts weather station traffic (Wunderground, Weathercloud) to display it locally in Home Assistant. It acts as a "Man-in-the-Middle" proxy.

## Architecture & Data Flow
- **Core Logic**: Relies on the vendored library `aiocloudweather` (located in `custom_components/cloudweatherproxy/aiocloudweather`).
  - `station.py`: Parses raw HTTP parameters into typed `WeatherStation` objects.
  - `proxy.py`: Handles forwarding data to upstream services (Wunderground/Weathercloud).
- **Ingestion**: `web.py` registers `HomeAssistantView` endpoints that mimic the APIs of weather services (e.g., `/wunderground/weatherstation/updateweatherstation.php`).
- **Processing**: Incoming requests are passed to `CloudWeatherListener` (from `aiocloudweather`), which parses the data.
- **State Updates**: `sensor.py` subscribes to `CloudWeatherListener` callbacks. When new data arrives, it dynamically creates or updates `CloudWeatherEntity` sensors.
- **Configuration**: `config_flow.py` manages the setup, allowing users to enable/disable specific proxies and configure DNS servers.

## Development Workflow
- **Environment Setup**: Run `scripts/setup` to install dependencies.
- **Running Local HA**: Use `scripts/develop` to start a local Home Assistant instance.
  - **Crucial**: This script sets `PYTHONPATH="${PYTHONPATH}:${PWD}/custom_components"` to inject the component without symlinking or installing it into the HA site-packages.
  - The instance runs in debug mode with configuration in `config/`.
- **Testing**: Since this relies on incoming HTTP requests, testing often involves sending mocked requests to the local HA instance (port 8123 by default).

## Code Conventions
- **Async/Await**: All I/O operations, especially in `web.py` and `sensor.py`, must be asynchronous.
- **Vendored Imports**: The `aiocloudweather` library is local. Use relative imports within the component (e.g., `from .aiocloudweather import ...`) instead of absolute imports.
- **Type Hinting**: Strictly enforced. Use `typing` module and HA specific types (`HomeAssistant`, `ConfigEntry`).
- **Constants**: Centralized in `const.py`. Use `UNIT_DESCRIPTION_MAPPING` for defining sensor properties based on units.
- **Logging**: Use `_LOGGER` (standard python logging) for debug and error messages.

## Key Files
- `custom_components/cloudweatherproxy/web.py`: HTTP endpoints for receiving weather station data.
- `custom_components/cloudweatherproxy/sensor.py`: Entity logic and dynamic sensor creation.
- `custom_components/cloudweatherproxy/__init__.py`: Component setup and `CloudWeatherListener` initialization.
- `custom_components/cloudweatherproxy/aiocloudweather/`: The vendored library.
  - `station.py`: Data parsing logic.
  - `proxy.py`: Upstream forwarding logic.

## Integration Details
- **Dependency**: The `aiocloudweather` library is now part of the codebase, not an external requirement.
- **Home Assistant**: Uses standard `config_entries` and `entity_platform` patterns.
