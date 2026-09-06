from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.solis_cloud_control.data import SolisCloudControlConfigEntry
from custom_components.solis_cloud_control.inverters.inverter import (
    InverterAllowExport,
    InverterMpptScanning,
    InverterOnOff,
)

from .coordinator import SolisCloudControlCoordinator
from .entity import SolisCloudControlEntity

async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SolisCloudControlConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    inverter = entry.runtime_data.inverter
    coordinator = entry.runtime_data.coordinator
    entities = []

    if inverter.on_off is not None:
        entities.append(
            OnOffSwitch(
                coordinator,
                SwitchEntityDescription(key="on_off_switch", name="Inverter On/Off", icon="mdi:power"),
                inverter.on_off,
            )
        )
    if inverter.allow_export is not None:
        entities.append(
            AllowExportSwitch(
                coordinator,
                SwitchEntityDescription(
                    key="allow_export_switch", name="Allow Export", icon="mdi:transmission-tower-export"
                ),
                inverter.allow_export,
            )
        )
    if inverter.mppt_scanning is not None:
        entities.append(
            MpptScanningSwitch(
                coordinator,
                SwitchEntityDescription(
                    key="mppt_scanning_switch", name="MPPT Multi-peak Scanning", icon="mdi:solar-power-variant"
                ),
                inverter.mppt_scanning,
            )
        )

    async_add_entities(entities)


class OnOffSwitch(SolisCloudControlEntity, SwitchEntity):
    def __init__(self, coordinator, entity_description, inverter_on_off: InverterOnOff) -> None:
        super().__init__(coordinator, entity_description, [inverter_on_off.on_cid, inverter_on_off.off_cid])
        self.inverter_on_off = inverter_on_off

    @property
    def assumed_state(self) -> bool:
        on_value = self.coordinator.data.get(self.inverter_on_off.on_cid)
        off_value = self.coordinator.data.get(self.inverter_on_off.off_cid)
        return not (
            on_value == off_value
            and self.inverter_on_off.is_valid_value(on_value)
            and self.inverter_on_off.is_valid_value(off_value)
        )

    @property
    def is_on(self) -> bool | None:
        on_value = self.coordinator.data.get(self.inverter_on_off.on_cid)
        off_value = self.coordinator.data.get(self.inverter_on_off.off_cid)
        if on_value == off_value and self.inverter_on_off.is_valid_value(on_value) and self.inverter_on_off.is_valid_value(
            off_value
        ):
            return on_value == self.inverter_on_off.on_value
        return None

    async def async_turn_on(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        await self.coordinator.control(self.inverter_on_off.on_cid, self.inverter_on_off.on_value)

    async def async_turn_off(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        await self.coordinator.control(self.inverter_on_off.off_cid, self.inverter_on_off.off_value)


class AllowExportSwitch(SolisCloudControlEntity, SwitchEntity):
    def __init__(self, coordinator, entity_description, inverter_allow_export: InverterAllowExport) -> None:
        super().__init__(coordinator, entity_description, inverter_allow_export.cid)
        self.inverter_allow_export = inverter_allow_export

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get(self.inverter_allow_export.cid)
        return value == "0" if value is not None else None

    async def async_turn_on(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        old_value = self._old_value()
        if old_value is None:
            return
        await self.coordinator.control(self.inverter_allow_export.cid, "0", old_value)

    async def async_turn_off(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        old_value = self._old_value()
        if old_value is None:
            return
        await self.coordinator.control(self.inverter_allow_export.cid, "1", old_value)

    def _old_value(self) -> str | None:
        state = self.is_on
        if state is None:
            return None
        return self.inverter_allow_export.on_value if state else self.inverter_allow_export.off_value


class MpptScanningSwitch(SolisCloudControlEntity, SwitchEntity):
    def __init__(self, coordinator, entity_description, inverter_mppt_scanning: InverterMpptScanning) -> None:
        super().__init__(coordinator, entity_description, inverter_mppt_scanning.cid)
        self.inverter_mppt_scanning = inverter_mppt_scanning

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get(self.inverter_mppt_scanning.cid)
        return value == self.inverter_mppt_scanning.on_value if value is not None else None

    async def async_turn_on(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        await self._set_state(self.inverter_mppt_scanning.on_value)

    async def async_turn_off(self, **kwargs) -> None:  # noqa: ANN003, ARG002
        await self._set_state(self.inverter_mppt_scanning.off_value)

    async def _set_state(self, value: str) -> None:
        old_value = self.inverter_mppt_scanning.on_value if self.is_on else self.inverter_mppt_scanning.off_value
        await self.coordinator.control(self.inverter_mppt_scanning.cid, value, old_value)
