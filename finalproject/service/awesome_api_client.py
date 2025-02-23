from dataclasses import dataclass
from typing import Any

from finalproject.service.http_client import HttpAPIClient

AWESOME_API_DEFAULT_ENDPOINT = "https://economia.awesomeapi.com.br"
AWESOME_API_CURRENCY_KEY_FORMAT = "{currency_from}{currency_to}"
AWESOME_API_GET_EXCHANGE_RATE_PATH_FORMAT = "/last/{currency_from}-{currency_to}"


@dataclass
class GetExchangeRateResponse:
    code: str
    codein: str
    name: str
    high: str
    low: str
    varBid: str
    pctChange: str
    bid: str
    ask: str
    timestamp: str
    create_date: str


class AwesomeAPIClient:
    """
    This class implements client for the following public exchange rate API:
    https://docs.awesomeapi.com.br/api-de-moedas?ref=public_apis&utm_medium=website
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

        Usage: /last/USD-GEL
        """
        http_response = self._http_client.get(
            self._exchange_rate_path.format(
                currency_from=currency_from, currency_to=currency_to
            )
        )
        return self._parse_exchange_rate_response(
            currency_from=currency_from,
            currency_to=currency_to,
            data=http_response.json(),
        )

    def _parse_exchange_rate_response(
        self, currency_from: str, currency_to: str, data: Any
    ) -> GetExchangeRateResponse:
        key = self._currency_key_format.format(
            currency_from=currency_from, currency_to=currency_to
        )
        return GetExchangeRateResponse(**data[key])
