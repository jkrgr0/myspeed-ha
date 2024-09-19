"""Constants for MySpeed integration."""

from logging import Logger, getLogger
from typing import Final

DOMAIN = "myspeed"
MYSPEED_CLIENTS = "myspeed_clients"
CONF_API_KEY: Final = "api_key"
CONF_HOSTNAME: Final = "hostname"
CONF_PORT: Final = "port"
CONF_USE_HTTP: Final = "use_http"

COORDINATORS = "coordinators"

LOGGER: Logger = getLogger(__package__)

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
