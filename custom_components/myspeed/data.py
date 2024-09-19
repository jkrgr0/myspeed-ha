"""Custom types for MySpeed integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import MySpeedApiClient
    from .coordinator import MySpeedDataUpdateCoordinator


type MySpeedConfigEntry = ConfigEntry[MySpeedData]


@dataclass
class MySpeedData:
    """Data for the Blueprint integration."""

    client: MySpeedApiClient
    coordinator: MySpeedDataUpdateCoordinator
    integration: Integration
