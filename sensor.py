from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.solis_cloud_control.data import (
    SolisCloudControlConfigEntry,
)

from .entity import SolisCloudControlEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolisCloudControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    coordinator = entry.runtime_data.coordinator

    entities = [
        SolisTemperatureSensor(
            coordinator,
            SensorEntityDescription(
                key="temperature",
                name="Inverter Temperature",
                icon="mdi:thermometer",
            ),
        ),
        SolisAcPowerSensor(
            coordinator,
            SensorEntityDescription(
                key="ac_output_total_power",
                name="AC Output Total Power",
                icon="mdi:solar-power",
            ),
        ),
        SolisTotalEnergySensor(
            coordinator,
            SensorEntityDescription(
                key="energy_total",
                name="Energy Total",
                icon="mdi:counter",
            ),
        ),
    ]

    async_add_entities(entities)


class SolisTemperatureSensor(SolisCloudControlEntity, SensorEntity):
    def __init__(self, coordinator, entity_description) -> None:
        super().__init__(coordinator, entity_description, [])
        self.entity_description = entity_description
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self):
        details = self.coordinator.data.get("_details", {})
        value = details.get("inverterTemperature")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None


class SolisAcPowerSensor(SolisCloudControlEntity, SensorEntity):
    def __init__(self, coordinator, entity_description) -> None:
        super().__init__(coordinator, entity_description, [])
        self.entity_description = entity_description
        self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def native_value(self):
        details = self.coordinator.data.get("_details", {})
        value = details.get("pac")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None


class SolisTotalEnergySensor(SolisCloudControlEntity, SensorEntity):
    def __init__(self, coordinator, entity_description) -> None:
        super().__init__(coordinator, entity_description, [])
        self.entity_description = entity_description
        self._attr_native_unit_of_measurement = "kWh"

    @property
    def native_value(self):
        details = self.coordinator.data.get("_details", {})
        value = details.get("eTotal")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None
