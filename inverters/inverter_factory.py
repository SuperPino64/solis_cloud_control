from custom_components.solis_cloud_control.api.solis_api import SolisCloudControlApiClient
from custom_components.solis_cloud_control.inverters.inverter import (
    Inverter,
    InverterAllowExport,
    InverterExportCalibration,
    InverterInfo,
    InverterMaxExportPower,
    InverterMaxOutputPower,
    InverterMpptScanInterval,
    InverterMpptScanning,
    InverterOnOff,
    InverterPowerLimit,
    InverterTime,
)

_MAX_RETRY_TIME_SECONDS = 60


async def create_inverter_info(api_client: SolisCloudControlApiClient, inverter_sn: str) -> InverterInfo:
    inverter_details = await api_client.inverter_details(inverter_sn, _MAX_RETRY_TIME_SECONDS)

    inverter_info = InverterInfo(
        serial_number=inverter_sn,
        model=_get_inverter_detail(inverter_details, "model"),
        version=_get_inverter_detail(inverter_details, "version"),
        machine=_get_inverter_detail(inverter_details, "machine"),
        energy_storage_control=_get_inverter_detail(inverter_details, "energyStorageControl"),
        smart_support=_get_inverter_detail(inverter_details, "smartSupport"),
        generator_support=_get_inverter_detail(inverter_details, "generatorSupport"),
        collector_model=_get_inverter_detail(inverter_details, "collectorModel"),
        power=_get_inverter_detail(inverter_details, "power"),
        power_unit=_get_inverter_detail(inverter_details, "powerStr"),
        parallel_number=_get_inverter_detail(inverter_details, "parallelNumber"),
    )

    return inverter_info


def create_inverter(inverter_info: InverterInfo) -> Inverter:
    if inverter_info.is_string_inverter:
        return _create_string_inverter(inverter_info)
    else:
        return _create_hybrid_inverter(inverter_info)


def _get_inverter_detail(inverter_details: dict, field: str) -> str | None:
    return str(value) if (value := inverter_details.get(field)) is not None else None


def _create_string_inverter(
    inverter_info: InverterInfo,
) -> Inverter:
    return Inverter(
        info=inverter_info,
        on_off=InverterOnOff(on_cid=48, off_cid=53),
        time=InverterTime(cid=18),
        power_limit=InverterPowerLimit(),
    )


def _create_hybrid_inverter(inverter_info: InverterInfo) -> Inverter:
    max_export_power = InverterMaxExportPower(
        max_value=inverter_info.max_export_power, scale=inverter_info.max_export_power_scale
    )

    return Inverter(
        info=inverter_info,
        on_off=InverterOnOff(),
        time=InverterTime(),
        max_output_power=InverterMaxOutputPower(),
        max_export_power=max_export_power,
        export_calibration=InverterExportCalibration(),
        allow_export=InverterAllowExport(),
        mppt_scan_interval=InverterMpptScanInterval(),
        mppt_scanning=InverterMpptScanning(),
    )
