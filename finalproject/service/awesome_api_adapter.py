from finalproject.service.awesome_api_client import (
    AwesomeAPIClient,
    GetExchangeRateResponse,
)
from finalproject.service.currency_conversion import (
    ConversionError,
    MidExchangeRateRetriever,
)

MEDIATOR_CURRENCY = "USD"


class AwesomeAPIAdapter:
    """
    This class converts AwesomeAPIClient calls to our MidExchangeRateRetriever methods.
    """

    def __init__(self, client: AwesomeAPIClient) -> None:
        self._client = client

    def get_mid_rate(self, from_currency: str, to_currency: str) -> float:
        if from_currency == to_currency:
            return 1

        return self._calculate_mid_rate(
            self._client.get_exchange_rate(from_currency, to_currency)
        )

    def _calculate_mid_rate(self, response: GetExchangeRateResponse) -> float:
        try:
            return (float(response.bid) + float(response.ask)) / 2
        except Exception:
            raise ConversionError()


class AwesomeAPIFindAnyExchangeRateStrategy:
    """
    This class is required because awesome API only supports
    exchange rates from USD and other popular currencies, but not from GEL.
    """

    def __init__(
        self,
        client: MidExchangeRateRetriever,
        mediator_currency: str = MEDIATOR_CURRENCY,
    ) -> None:
        self._client = client
        self._mediator_currency = mediator_currency

    def get_mid_rate(self, from_currency: str, to_currency: str) -> float:
        return self._client.get_mid_rate(
            self._mediator_currency, to_currency
        ) / self._client.get_mid_rate(self._mediator_currency, from_currency)
