from dataclasses import dataclass
from typing import ClassVar

from custom_components.solis_cloud_control.utils.safe_converters import (
    safe_convert_power_to_watts,
    safe_get_float_value,
)


@dataclass(frozen=True)
class InverterInfo:
    ENERGY_STORAGE_CONTROL_DISABLED: ClassVar[str] = "0"
    MAX_EXPORT_POWER_DEFAULT: ClassVar[float] = 1_000_000
    MAX_EXPORT_POWER_STEP_DEFAULT: ClassVar[float] = 100
    MAX_EXPORT_POWER_SCALE_DEFAULT: ClassVar[float] = 1.0
    POWER_LIMIT_DEFAULT: ClassVar[float] = 110.0
    PARALLEL_INVERTER_COUNT_DEFAULT: ClassVar[int] = 1

    serial_number: str
    model: str | None
    version: str | None
    machine: str | None
    energy_storage_control: str | None
    smart_support: str | None
    generator_support: str | None
    collector_model: str | None
    power: str | None
    power_unit: str | None
    parallel_number: str | None

    @property
    def is_string_inverter(self) -> bool:
        return (
            self.energy_storage_control is not None
            and self.energy_storage_control == self.ENERGY_STORAGE_CONTROL_DISABLED
        )

    @property
    def max_export_power(self) -> float:
        power = safe_convert_power_to_watts(self.power, self.power_unit)
        if power is not None:
            return power * self.parallel_inverter_count
        else:
            return self.MAX_EXPORT_POWER_DEFAULT

    @property
    def max_export_power_scale(self) -> float:
        if self.model and self.model.lower() in ["3105", "3173", "3315", "3331", "3332", "5305"]:
            return 0.01
        else:
            return self.MAX_EXPORT_POWER_SCALE_DEFAULT

    @property
    def parallel_inverter_count(self) -> int:
        parallel_inverter_count = safe_get_float_value(self.parallel_number)
        if parallel_inverter_count is None or not parallel_inverter_count.is_integer() or parallel_inverter_count < 1:
            return self.PARALLEL_INVERTER_COUNT_DEFAULT
        else:
            return int(parallel_inverter_count)


@dataclass(frozen=True)
class InverterOnOff:
    on_cid: int = 52
    off_cid: int = 54
    on_value: str = "190"
    off_value: str = "222"

    def is_valid_value(self, value: str | None) -> bool:
        return value in (self.on_value, self.off_value)


@dataclass(frozen=True)
class InverterTime:
    cid: int = 56



@dataclass(frozen=True)
class InverterMaxOutputPower:
    cid: int = 376
    min_value: float = 0
    max_value: float = 100
    step: float = 1


@dataclass(frozen=True)
class InverterMaxExportPower:
    cid: int = 499
    min_value: float = 0
    max_value: float = InverterInfo.MAX_EXPORT_POWER_DEFAULT
    step: float = InverterInfo.MAX_EXPORT_POWER_STEP_DEFAULT
    scale: float = InverterInfo.MAX_EXPORT_POWER_SCALE_DEFAULT


@dataclass(frozen=True)
class InverterPowerLimit:
    cid: int = 15
    min_value: float = 0
    max_value: float = InverterInfo.POWER_LIMIT_DEFAULT
    step: float = 5


@dataclass(frozen=True)
class InverterAllowExport:
    cid: int = 6962
    on_value: str = "80"
    off_value: str = "88"


@dataclass(frozen=True)
class InverterExportCalibration:
    cid: int = 6968
    min_value: float = -1000
    max_value: float = 1000
    step: float = 1


@dataclass(frozen=True)
class InverterMpptScanInterval:
    cid: int = 4755
    min_value: float = 600
    max_value: float = 10800
    step: float = 1


@dataclass(frozen=True)
class InverterMpptScanning:
    cid: int = 4754
    on_value: str = "1"
    off_value: str = "0"


@dataclass(frozen=True)
class Inverter:
    info: InverterInfo
    on_off: InverterOnOff | None = None
    time: InverterTime | None = None
    max_output_power: InverterMaxOutputPower | None = None
    max_export_power: InverterMaxExportPower | None = None
    export_calibration: InverterExportCalibration | None = None
    power_limit: InverterPowerLimit | None = None
    allow_export: InverterAllowExport | None = None
    mppt_scan_interval: InverterMpptScanInterval | None = None
    mppt_scanning: InverterMpptScanning | None = None

    @property
    def read_batch_cids(self) -> list[int]:
        cids: list[int] = []

        if self.on_off:
            cids.append(self.on_off.on_cid)
            cids.append(self.on_off.off_cid)
        if self.time:
            cids.append(self.time.cid)
        if self.max_output_power:
            cids.append(self.max_output_power.cid)
        if self.max_export_power:
            cids.append(self.max_export_power.cid)
        if self.export_calibration:
            cids.append(self.export_calibration.cid)
        if self.power_limit:
            cids.append(self.power_limit.cid)
        if self.allow_export:
            cids.append(self.allow_export.cid)
        if self.mppt_scan_interval:
            cids.append(self.mppt_scan_interval.cid)
        if self.mppt_scanning:
            cids.append(self.mppt_scanning.cid)

        return cids

    @property
    def read_cids(self) -> list[int]:
        return []

    @property
    def all_cids(self) -> list[int]:
        return [*self.read_batch_cids, *self.read_cids]
