from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from finalproject.service.currency_conversion.http_client import (
    HttpAPIClient,
    HttpAPIResponse,
)

AWESOME_API_DEFAULT_ENDPOINT = "https://economia.awesomeapi.com.br"
AWESOME_API_CURRENCY_KEY_FORMAT = "{currency_from}{currency_to}"
AWESOME_API_GET_EXCHANGE_RATE_PATH_FORMAT = "/json/last/{currency_from}-{currency_to}"


@dataclass(frozen=True)
class GetExchangeRateResponse:
    code: str = ""
    codein: str = ""
    name: str = ""
    high: str = ""
    low: str = ""
    varBid: str = ""
    pctChange: str = ""
    bid: str = ""
    ask: str = ""
    timestamp: str = ""
    create_date: str = ""


class AwesomeAPIClient(Protocol):
    def get_exchange_rate(
        self, currency_from: str, currency_to: str
    ) -> GetExchangeRateResponse:
        pass


class DefaultAwesomeAPIClient:
    """
    This class implements client for the following public exchange rate API:
    https://docs.awesomeapi.com.br/api-de-moedas

    We found AwesomeAPI on public API registry: https://publicapi.dev/economia-awesome-api
    """

    def __init__(
        self,
        http_client: HttpAPIClient,
        endpoint: str = AWESOME_API_DEFAULT_ENDPOINT,
        exchange_rate_path: str = AWESOME_API_GET_EXCHANGE_RATE_PATH_FORMAT,
        currency_key_format: str = AWESOME_API_CURRENCY_KEY_FORMAT,
    ) -> None:
        self._http_client = http_client.with_api_endpoint(endpoint)
        self._exchange_rate_path = exchange_rate_path
        self._currency_key_format = currency_key_format

    def get_exchange_rate(
        self, currency_from: str, currency_to: str
    ) -> GetExchangeRateResponse:
        """
        This method returns the exchange rate from USD to the specified currency.
        """
        http_response = self._http_client.get(
            self._exchange_rate_path.format(
                currency_from=currency_from, currency_to=currency_to
            )
        )

        # Raise error if server returns status code other than 200
        if http_response.status_code != 200:
            raise AwesomeAPIRequestFailed()

        return self._parse_exchange_rate_response(
            currency_from=currency_from,
            currency_to=currency_to,
            response=http_response,
        )

    def _parse_exchange_rate_response(
        self, currency_from: str, currency_to: str, response: HttpAPIResponse
    ) -> GetExchangeRateResponse:
        key = self._currency_key_format.format(
            currency_from=currency_from, currency_to=currency_to
        )
        try:
            return GetExchangeRateResponse(**response.json()[key])
        except Exception:
            raise AwesomeAPIRequestFailed()


class AwesomeAPIRequestFailed(Exception):
    pass


class FakeAwesomeAPIClient:
    def __init__(self) -> None:
        self._fake_response = GetExchangeRateResponse()

    def with_fake_response(
        self, response: GetExchangeRateResponse
    ) -> FakeAwesomeAPIClient:
        self._fake_response = response
        return self

    def get_exchange_rate(
        self, currency_from: str, currency_to: str
    ) -> GetExchangeRateResponse:
        return self._fake_response
