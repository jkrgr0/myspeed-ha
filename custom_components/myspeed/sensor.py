"""Sensor platform for MySpeed integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfDataRate, UnitOfTime

from .entity import MySpeedEntity, MySpeedEntityDescription

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import MySpeedDataUpdateCoordinator
    from .data import MySpeedConfigEntry


@dataclass(frozen=True, kw_only=True)
class MySpeedSensorEntityDescription(MySpeedEntityDescription, SensorEntityDescription):
    """Class describing MySpeed sensor entities."""


MYSPEED_SENSORS: Final[tuple[MySpeedSensorEntityDescription, ...]] = (
    MySpeedSensorEntityDescription(
        key="total_tests",
        name="Total tests",
        icon="mdi:numeric",
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=0,
        translation_key="total_tests",
    ),
    MySpeedSensorEntityDescription(
        key="failed_tests",
        name="Failed tests",
        icon="mdi:numeric",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="failed_tests",
    ),
    MySpeedSensorEntityDescription(
        key="custom_tests",
        name="Custom tests",
        icon="mdi:numeric",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="custom_tests",
    ),
    MySpeedSensorEntityDescription(
        key="min_ping",
        name="Min ping",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="min_ping",
    ),
    MySpeedSensorEntityDescription(
        key="max_ping",
        name="Max ping",
        icon="mdi:speedometer",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="max_ping",
    ),
    MySpeedSensorEntityDescription(
        key="avg_ping",
        name="Average ping",
        icon="mdi:speedometer-medium",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="avg_ping",
    ),
    MySpeedSensorEntityDescription(
        key="min_upload",
        name="Min upload",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="min_upload",
    ),
    MySpeedSensorEntityDescription(
        key="max_upload",
        name="Max upload",
        icon="mdi:speedometer",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="max_upload",
    ),
    MySpeedSensorEntityDescription(
        key="avg_upload",
        name="Avg upload",
        icon="mdi:speedometer-medium",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="avg_upload",
    ),
    MySpeedSensorEntityDescription(
        key="min_download",
        name="Min download",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="min_download",
    ),
    MySpeedSensorEntityDescription(
        key="max_download",
        name="Max download",
        icon="mdi:speedometer",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="max_download",
    ),
    MySpeedSensorEntityDescription(
        key="avg_download",
        name="Avg download",
        icon="mdi:speedometer-medium",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        translation_key="avg_download",
    ),
    MySpeedSensorEntityDescription(
        key="min_time",
        name="Min time",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="min_time",
    ),
    MySpeedSensorEntityDescription(
        key="max_time",
        name="Max time",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="max_time",
    ),
    MySpeedSensorEntityDescription(
        key="avg_time",
        name="Avg time",
        icon="mdi:timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        translation_key="avg_time",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: MySpeedConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        MySpeedSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in MYSPEED_SENSORS
    )


class MySpeedSensor(MySpeedEntity, SensorEntity):
    """myspeed Sensor class."""

    def __init__(
        self,
        coordinator: MySpeedDataUpdateCoordinator,
        entity_description: MySpeedSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        key, statistic = self.entity_description.key.split("_")
        return (
            self.coordinator.data.get("statistics", {})
            .get(statistic, {})
            .get(key, None)
        )
