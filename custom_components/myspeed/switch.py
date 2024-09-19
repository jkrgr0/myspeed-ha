"""Switch platform for myspeed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import LOGGER
from .entity import MySpeedEntity, MySpeedEntityDescription

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MySpeedDataUpdateCoordinator
    from .data import MySpeedConfigEntry


@dataclass(frozen=True, kw_only=True)
class MySpeedSwitchEntityDescription(MySpeedEntityDescription, SwitchEntityDescription):
    """Class describing MySpeed switch entities."""


MYSPEED_SWITCHES: Final[tuple[MySpeedSwitchEntityDescription, ...]] = (
    MySpeedSwitchEntityDescription(
        key="speedtests",
        icon="mdi:speedometer",
        name="Speedtests",
        translation_key="speedtests",
    ),
)

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="myspeed",
        name="Integration Switch",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MySpeedConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        MySpeedSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in MYSPEED_SWITCHES
    )


class MySpeedSwitch(MySpeedEntity, SwitchEntity):
    """myspeed switch class."""

    def __init__(
        self,
        coordinator: MySpeedDataUpdateCoordinator,
        entity_description: MySpeedSwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.coordinator.data.get("status", {}).get("paused", True)

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        result = await (
            self.coordinator.config_entry.runtime_data.client.async_continue_speedtest()
        )
        LOGGER.debug("Switch turned on: %s", result)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        result = await self.coordinator.config_entry.runtime_data.client.async_pause_speedtest()
        LOGGER.debug("Switch turned off: %s", result)
        await self.coordinator.async_request_refresh()
