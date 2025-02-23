from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
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

    def __init__(self) -> None:
        self._base_url = "https://economia.awesomeapi.com.br/last"

    def get_exchange_rate_from_usd_to(self, currency: str) -> None:
        """
        This method returns the exchange rate from USD to the specified currency.

        Usage:
        https://economia.awesomeapi.com.br/last/USD-GEL
        """
        response = httpx.get(f"{self._base_url}/USD-{currency}")
        response.raise_for_status()
