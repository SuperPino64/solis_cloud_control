import logging
from typing import Protocol

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.solis_cloud_control.data import SolisCloudControlConfigEntry
from custom_components.solis_cloud_control.inverters.inverter import (
    InverterExportCalibration,
    InverterMaxExportPower,
    InverterMaxOutputPower,
    InverterMpptScanInterval,
    InverterPowerLimit,
)
from custom_components.solis_cloud_control.utils.safe_converters import safe_get_float_value

from .coordinator import SolisCloudControlCoordinator
from .entity import SolisCloudControlEntity

_LOGGER = logging.getLogger(__name__)


class _NumberConfig(Protocol):
    cid: int
    min_value: float
    max_value: float
    step: float


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolisCloudControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    inverter = entry.runtime_data.inverter
    coordinator = entry.runtime_data.coordinator
    entities = []

    if inverter.max_output_power is not None:
        entities.append(
            MaxOutputPower(
                coordinator,
                NumberEntityDescription(
                    key="max_output_power", name="Max Output Power", icon="mdi:lightning-bolt-outline"
                ),
                inverter.max_output_power,
            )
        )
    if inverter.max_export_power is not None:
        entities.append(
            MaxExportPower(
                coordinator,
                NumberEntityDescription(
                    key="max_export_power", name="Max Export Power", icon="mdi:transmission-tower-export"
                ),
                inverter.max_export_power,
            )
        )
    if inverter.export_calibration is not None:
        entities.append(
            ExportCalibration(
                coordinator,
                NumberEntityDescription(
                    key="export_calibration", name="Export Calibration", icon="mdi:image-filter-tilt-shift"
                ),
                inverter.export_calibration,
            )
        )
    if inverter.power_limit is not None:
        entities.append(
            PowerLimit(
                coordinator,
                NumberEntityDescription(key="power_limit", name="Power Limit", icon="mdi:transmission-tower-export"),
                inverter.power_limit,
            )
        )
    if inverter.mppt_scan_interval is not None:
        entities.append(
            MpptScanIntervalNumber(
                coordinator,
                NumberEntityDescription(
                    key="mppt_scan_interval", name="MPPT Multi-peak Scan Interval", icon="mdi:timer-refresh-outline"
                ),
                inverter.mppt_scan_interval,
            )
        )

    async_add_entities(entities)


class _WritableNumber(SolisCloudControlEntity, NumberEntity):
    def _set_value_attributes(self, number: _NumberConfig, *, unit: str | None = None) -> None:
        self._attr_native_min_value = number.min_value
        self._attr_native_max_value = number.max_value
        self._attr_native_step = number.step
        self._attr_mode = NumberMode.BOX
        if unit is not None:
            self._attr_native_unit_of_measurement = unit

    async def _write_value(self, cid: int, value: float, formatted: str | None = None) -> None:
        value_str = formatted or str(int(round(value)))
        _LOGGER.info("Set '%s' to %f (value: %s)", self.name, value, value_str)
        await self.coordinator.control(cid, value_str)


class MaxOutputPower(_WritableNumber):
    def __init__(self, coordinator, entity_description, inverter_max_output_power: InverterMaxOutputPower) -> None:
        super().__init__(coordinator, entity_description, inverter_max_output_power.cid)
        self.inverter_max_output_power = inverter_max_output_power
        self._set_value_attributes(inverter_max_output_power, unit=PERCENTAGE)

    @property
    def native_value(self) -> float | None:
        return safe_get_float_value(self.coordinator.data.get(self.inverter_max_output_power.cid))

    async def async_set_native_value(self, value: float) -> None:
        await self._write_value(self.inverter_max_output_power.cid, value)


class MaxExportPower(_WritableNumber):
    def __init__(self, coordinator, entity_description, inverter_max_export_power: InverterMaxExportPower) -> None:
        super().__init__(coordinator, entity_description, inverter_max_export_power.cid)
        self.inverter_max_export_power = inverter_max_export_power
        self._set_value_attributes(inverter_max_export_power, unit=UnitOfPower.WATT)
        self._attr_device_class = NumberDeviceClass.POWER

    @property
    def native_value(self) -> float | None:
        value = safe_get_float_value(self.coordinator.data.get(self.inverter_max_export_power.cid))
        return value / self.inverter_max_export_power.scale if value is not None else None

    async def async_set_native_value(self, value: float) -> None:
        await self._write_value(
            self.inverter_max_export_power.cid,
            value,
            str(int(round(value * self.inverter_max_export_power.scale))),
        )


class ExportCalibration(_WritableNumber):
    def __init__(self, coordinator, entity_description, inverter_export_calibration: InverterExportCalibration) -> None:
        super().__init__(coordinator, entity_description, inverter_export_calibration.cid)
        self.inverter_export_calibration = inverter_export_calibration
        self._set_value_attributes(inverter_export_calibration, unit=UnitOfPower.WATT)
        self._attr_device_class = NumberDeviceClass.POWER

    @property
    def native_value(self) -> float | None:
        return safe_get_float_value(self.coordinator.data.get(self.inverter_export_calibration.cid))

    async def async_set_native_value(self, value: float) -> None:
        await self._write_value(self.inverter_export_calibration.cid, value)


class PowerLimit(_WritableNumber):
    def __init__(self, coordinator, entity_description, inverter_power_limit: InverterPowerLimit) -> None:
        super().__init__(coordinator, entity_description, inverter_power_limit.cid)
        self.inverter_power_limit = inverter_power_limit
        self._set_value_attributes(inverter_power_limit, unit=PERCENTAGE)
        self._attr_mode = NumberMode.SLIDER

    @property
    def native_value(self) -> float | None:
        return safe_get_float_value(self.coordinator.data.get(self.inverter_power_limit.cid))

    async def async_set_native_value(self, value: float) -> None:
        await self._write_value(self.inverter_power_limit.cid, value)


class MpptScanIntervalNumber(_WritableNumber):
    def __init__(self, coordinator, entity_description, inverter_mppt_scan_interval: InverterMpptScanInterval) -> None:
        super().__init__(coordinator, entity_description, inverter_mppt_scan_interval.cid)
        self.inverter_mppt_scan_interval = inverter_mppt_scan_interval
        self._set_value_attributes(inverter_mppt_scan_interval)

    @property
    def native_value(self) -> float | None:
        return safe_get_float_value(self.coordinator.data.get(self.inverter_mppt_scan_interval.cid))

    async def async_set_native_value(self, value: float) -> None:
        await self._write_value(self.inverter_mppt_scan_interval.cid, value)
