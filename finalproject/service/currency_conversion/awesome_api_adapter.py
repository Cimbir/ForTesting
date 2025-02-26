from finalproject.service.currency_conversion.awesome_api_client import (
    AwesomeAPIClient,
    DefaultAwesomeAPIClient,
    GetExchangeRateResponse,
)
from finalproject.service.currency_conversion.currency_conversion import (
    BaseCurrencyConversionService,
    BaseMidExchangeRateRetriever,
    ConversionError,
    MidExchangeRateRetriever,
)
from finalproject.service.currency_conversion.http_client import HttpxAPIClient

MEDIATOR_CURRENCY = "USD"


class AwesomeAPIAdapter(BaseMidExchangeRateRetriever):
    """
    This class converts AwesomeAPIClient calls to our MidExchangeRateRetriever methods.
    """

    def __init__(self, client: AwesomeAPIClient) -> None:
        self._client = client

    def _get_mid_rate_between_different_currencies(
        self, from_currency: str, to_currency: str
    ) -> float:
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


class AwesomeAPIFacade(BaseCurrencyConversionService):
    """
    This is class that implements CurrencyConversionService and uses AwesomeAPI
    """

    def __init__(
        self, client: AwesomeAPIClient = DefaultAwesomeAPIClient(HttpxAPIClient())
    ) -> None:
        self._direct_api_client = client
        self._adapter = AwesomeAPIFindAnyExchangeRateStrategy(
            AwesomeAPIAdapter(self._direct_api_client)
        )
        super().__init__(self._adapter)
