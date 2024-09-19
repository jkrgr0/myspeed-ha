"""MySpeed parent entity class."""

from __future__ import annotations

import dataclasses

from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MySpeedDataUpdateCoordinator


@dataclasses.dataclass(frozen=True, kw_only=True)
class MySpeedEntityDescription(EntityDescription):
    """Describe a MySpeed entity."""


class MySpeedEntity(CoordinatorEntity[MySpeedDataUpdateCoordinator]):
    """Represents any entity created for the MySpeed platform."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MySpeedDataUpdateCoordinator,
        description: MySpeedEntityDescription,
    ) -> None:
        """Initialize the MySpeed entity."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    # def __init__(self, coordinator: MySpeedDataUpdateCoordinator) -> None:
    #     """Initialize."""
    #     super().__init__(coordinator)
    #     self._attr_unique_id = coordinator.config_entry.entry_id
    #     self._attr_device_info = DeviceInfo(
    #         identifiers={
    #             (
    #                 coordinator.config_entry.domain,
    #                 coordinator.config_entry.entry_id,
    #             ),
    #         },
    #     )
