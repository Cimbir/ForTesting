from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from finalproject.service.currency_conversion.currency_conversion import ConversionRequestFailed
from finalproject.service.currency_conversion.http_client import HttpAPIClient

EXCHANGE_RATE_API_DEFAULT_ENDPOINT = "https://open.er-api.com/v6"
EXCHANGE_RATE_API_GET_RATES_FORMAT = "/latest/{currency}"


@dataclass(frozen=True)
class ExchangeRatesFromResponse:
    result: str = ""
    provider: str = ""
    documentation: str = ""
    terms_of_use: str = ""
    time_last_update_unix: int = 0
    time_last_update_utc: str = ""
    time_next_update_unix: int = 0
    time_next_update_utc: str = ""
    time_eol_unix: int = 0
    base_code: str = ""
    rates: dict[str, float] = field(default_factory=dict)


class ExchangeRateAPIClient(Protocol):
    def get_rates_from(self, currency: str) -> ExchangeRatesFromResponse:
        pass


class ExchangeRateAPIRemoteClient:
    """
    This class implements open API version of the Exchange Rate API:
    https://www.exchangerate-api.com/docs/free
    """

    def __init__(
        self,
        http_client: HttpAPIClient,
        endpoint: str = EXCHANGE_RATE_API_DEFAULT_ENDPOINT,
        get_rates_format: str = EXCHANGE_RATE_API_GET_RATES_FORMAT,
    ) -> None:
        self._http_client = http_client.with_api_endpoint(endpoint)
        self._get_rates_format = get_rates_format

    def get_rates_from(self, currency: str) -> ExchangeRatesFromResponse:
        http_response = self._http_client.get(
            self._get_rates_format.format(currency=currency)
        )
        try:
            return ExchangeRatesFromResponse(**http_response.json())
        except Exception:
            raise ConversionRequestFailed()


@dataclass
class ExchangeRateAPIFakeClient:
    """
    This class is used for testing purposes only.
    """

    fake_response: ExchangeRatesFromResponse = field(
        default_factory=ExchangeRatesFromResponse
    )

    def get_rates_from(self, currency: str) -> ExchangeRatesFromResponse:
        return self.fake_response
