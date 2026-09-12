import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.solis_cloud_control.api.solis_api import (
    SolisCloudControlApiClient,
    SolisCloudControlApiError,
)
from custom_components.solis_cloud_control.inverters.inverter import Inverter

_LOGGER = logging.getLogger(__name__)

_COORDINATOR_NAME = "Solis Cloud Control"

_UPDATE_INTERVAL = timedelta(minutes=5)

_REQUEST_REFRESH_COOLDOWN_SECONDS = 10

_UPDATE_BATCH_DATA_MAX_RETRY_TIME_SECONDS = 180
_UPDATE_DATA_MAX_RETRY_TIME_SECONDS = 60

_MAX_CONSECUTIVE_FAILURES = 5


class SolisCloudControlData(dict[int, str | None]):
    pass


class SolisCloudControlCoordinator(DataUpdateCoordinator[SolisCloudControlData]):
    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        api_client: SolisCloudControlApiClient,
        inverter: Inverter,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=_COORDINATOR_NAME,
            config_entry=config_entry,
            update_interval=_UPDATE_INTERVAL,
            request_refresh_debouncer=Debouncer(
                hass,
                _LOGGER,
                cooldown=_REQUEST_REFRESH_COOLDOWN_SECONDS,
                immediate=False,
            ),
        )

        self._api_client = api_client
        self._inverter = inverter
        self._failure_count = 0

    async def _reload_integration(self) -> None:
        _LOGGER.warning(
            "Solis communication failed %s times in a row. Reloading integration.",
            _MAX_CONSECUTIVE_FAILURES,
        )

        try:
            await self.hass.config_entries.async_reload(
                self.config_entry.entry_id
            )
        except Exception:
            _LOGGER.exception(
                "Failed reloading Solis Cloud Control integration"
            )

    async def _async_update_data(self) -> SolisCloudControlData:
        inverter_sn = self._inverter.info.serial_number

        try:
            results = await self._api_client.read_batch(
                inverter_sn,
                self._inverter.read_batch_cids,
                max_retry_time=_UPDATE_BATCH_DATA_MAX_RETRY_TIME_SECONDS,
            )

            for read_cid in self._inverter.read_cids:
                results[read_cid] = await self._api_client.read(
                    inverter_sn,
                    read_cid,
                    max_retry_time=_UPDATE_DATA_MAX_RETRY_TIME_SECONDS,
                )

            data = SolisCloudControlData(
                {
                    cid: results.get(cid)
                    for cid in self._inverter.all_cids
                }
            )

            if self._failure_count > 0:
                _LOGGER.info(
                    "Communication restored. Resetting failure counter (%s -> 0).",
                    self._failure_count,
                )

            self._failure_count = 0

            _LOGGER.debug("Data read from API: %s", data)

            return data

        except SolisCloudControlApiError as error:
            error_text = str(error).lower()

            is_recoverable_error = any(
                text in error_text
                for text in (
                    "b0072",
                    "device is offline",
                    "timeout",
                    "connection",
                    "connect",
                    "b0115",
                    "datalogger is offline",
                    "disconnected",
                    "502",
                )
            )

            if is_recoverable_error:
                self._failure_count += 1

                _LOGGER.warning(
                    "Solis communication failure %s/%s: %s",
                    self._failure_count,
                    _MAX_CONSECUTIVE_FAILURES,
                    error,
                )

                if self._failure_count >= _MAX_CONSECUTIVE_FAILURES:
                    _LOGGER.warning(
                        "Maximum failure count reached. Reloading integration."
                    )

                    self._failure_count = 0

                    asyncio.create_task(
                        self._reload_integration()
                    )
            else:
                _LOGGER.warning(
                    "Non-recoverable Solis API error: %s",
                    error,
                )

                self._failure_count = 0

            raise UpdateFailed(error) from error

    async def control(
        self,
        cid: int,
        value: str,
        old_value: str | None = None,
    ) -> None:
        if self.data:
            new_data = SolisCloudControlData(self.data)
            new_data[cid] = value
            self.async_set_updated_data(new_data)

        try:
            inverter_sn = self._inverter.info.serial_number

            await self._api_client.control(
                inverter_sn,
                cid,
                value,
                old_value,
            )

        finally:
            await self.async_request_refresh()
