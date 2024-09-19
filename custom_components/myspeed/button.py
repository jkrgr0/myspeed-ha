"""Button sensor platform for MySpeed integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .const import LOGGER
from .coordinator import MySpeedDataUpdateCoordinator
from .entity import MySpeedEntity, MySpeedEntityDescription

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import MySpeedConfigEntry


@dataclass(frozen=True, kw_only=True)
class MySpeedButtonEntityDescription(MySpeedEntityDescription, ButtonEntityDescription):
    """Class describing MySpeed buttons entities."""


MYSPEED_BUTTONS: Final[tuple[MySpeedButtonEntityDescription, ...]] = (
    MySpeedButtonEntityDescription(
        key="run_speedtest",
        icon="mdi:play",
        name="Run Speedtest",
        translation_key="run_speedtest",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MySpeedConfigEntry,
    asyncd_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button."""
    asyncd_add_entities(
        MySpeedButton(
            entry.runtime_data.coordinator,
            description,
        )
        for description in MYSPEED_BUTTONS
        if isinstance(entry.runtime_data.coordinator, MySpeedDataUpdateCoordinator)
    )


class MySpeedButton(MySpeedEntity, ButtonEntity):
    """Represents a myspeed button."""

    def __init__(
        self,
        coordinator: MySpeedDataUpdateCoordinator,
        entity_description: MySpeedButtonEntityDescription,
    ) -> None:
        """Create a run speedtest button."""
        super().__init__(coordinator, entity_description)

        self.coordinator = coordinator

    @property
    def available(self) -> bool:
        """Return sensor availability."""
        return super().available and self.coordinator.data is not None

    async def async_press(self) -> None:
        """Press the run speedtest button."""
        result = await self.coordinator.config_entry.runtime_data.client.async_run_speedtest()  # noqa: E501
        LOGGER.debug("Run speedtest button pressed: %s", result)
