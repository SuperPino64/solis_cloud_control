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
            
