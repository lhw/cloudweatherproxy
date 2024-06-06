# Cloud Weather Proxy

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]

## Description

The Cloud Weather Proxy integration allows you to locally retrieve weather information from a weather station, that supports either Weather Underground or Weathercloud, and display it in Home Assistant.

To use the integration an additional local setup including DNS and a forwarding HTTP server is required, as the destination URLs for the weather station need to be spoofed.

Optionally the weather data can be passed to its indended destination.

## HomeAssistant

**This integration will set up the following platforms.**

| Platform | Description                         |
| -------- | ----------------------------------- |
| `sensor` | Show info from weather station API. |

## Installation


### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
1. Download _all_ the files from the `custom_components/cloudweatherproxy/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Cloud Weather Proxy"

### HACS
*Coming soon*


### MITM/Spoofing Setup

As the destination URLs are hard coded into most weather stations we need to spoof the DNS records in the local network.

1. Setup a local DNS server that allows overriding single entries. Some routers can do this built-in. If not simple setups like PiHole, CoreDNS and others allow for this.
2. Set the DNS server as default in your DHCP settings, if its not your router.
3. Setup a proxying HTTP server that forwards the domains and adds additional information, such as the HomeAssistant access token.

An example setup is provided in the directory *examples*. It sets up a docker stack that uses Caddy and CoreDNS. Please ensure that port 80 and 53 are available on the IP you are assigning.

* [docker-compose.yml](examples/docker-compose.yml)
  * Set the `HA_ACCESS_TOKEN` envionment variable to a permanent access token from HomeAssistant.
* [Caddyfile](examples/Caddyfile)
  * Replace `<homeassistant>` with your HomeAssistant address and port
* [Corefile](examples/Corefile)
  * Replace `<yourip>` with your MITM IP address, i.e. the server running the Caddy and CoreDNS.
## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[commits-shield]: https://img.shields.io/github/commit-activity/y/lhw/cloudweatherproxy.svg
[commits]: https://github.com/lhw/cloudweatherproxy/commits/main
[license-shield]: https://img.shields.io/github/license/lhw/cloudweatherproxy.svg
[maintenance-shield]: https://img.shields.io/badge/maintainer-Lennart%20Weller%20%40lhw-blue.svg
[releases-shield]: https://img.shields.io/github/release/lhw/cloudweatherproxy.svg
[releases]: https://github.com/lhw/cloudweatherproxy/releases
