"""DataUpdateCoordinator for MySpeed integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    MySpeedApiClientAuthenticationError,
    MySpeedApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MySpeedConfigEntry


SCAN_INTERVAL = timedelta(seconds=30)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class MySpeedDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: MySpeedConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass, logger=LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except MySpeedApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except MySpeedApiClientError as exception:
            raise UpdateFailed(exception) from exception
