"""
Custom integration to integrate myspeed with Home Assistant.

For more details about this integration, please refer to
https://github.com/jkrgr0/myspeed-ha
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import MySpeedApiClient
from .const import CONF_API_KEY, CONF_HOSTNAME, CONF_PORT, CONF_USE_HTTP
from .coordinator import MySpeedDataUpdateCoordinator
from .data import MySpeedData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MySpeedConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: MySpeedConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = MySpeedDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = MySpeedData(
        client=MySpeedApiClient(
            hostname=entry.data[CONF_HOSTNAME],
            port=entry.data[CONF_PORT],
            api_key=entry.data[CONF_API_KEY],
            session=async_get_clientsession(hass),
            use_http=entry.data[CONF_USE_HTTP],
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MySpeedConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: MySpeedConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
