"""Binary sensor platform for myspeed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import MySpeedEntity, MySpeedEntityDescription

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MySpeedDataUpdateCoordinator
    from .data import MySpeedConfigEntry


@dataclass(frozen=True, kw_only=True)
class MySpeedBinarySensorEntityDescription(
    MySpeedEntityDescription, BinarySensorEntityDescription
):
    """Class describing MySpeed binary sensor entities."""


MYSPEED_BINARY_SENSORS: Final[tuple[MySpeedBinarySensorEntityDescription, ...]] = (
    MySpeedBinarySensorEntityDescription(
        key="speedtest_running",
        icon="mdi:play-pause",
        name="Speedtest running",
        translation_key="speedtest_running",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MySpeedConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        MySpeedBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in MYSPEED_BINARY_SENSORS
    )


class MySpeedBinarySensor(MySpeedEntity, BinarySensorEntity):
    """myspeed binary_sensor class."""

    def __init__(
        self,
        coordinator: MySpeedDataUpdateCoordinator,
        entity_description: MySpeedBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get("status", {}).get("running", False)
