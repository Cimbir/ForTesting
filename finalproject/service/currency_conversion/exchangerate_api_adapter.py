from finalproject.service.currency_conversion.currency_conversion import (
    BaseCurrencyConversionService,
    BaseMidExchangeRateRetriever,
    ConversionError,
)
from finalproject.service.currency_conversion.exchangerate_api_client import (
    ExchangeRateAPIClient,
    ExchangeRateAPIRemoteClient,
)
from finalproject.service.currency_conversion.http_client import HttpxAPIClient


class ExchangeRateAPIAdapter(BaseMidExchangeRateRetriever):
    """
    This class converts ExchangeRateAPI calls to our MidExchangeRateRetriever methods.
    """

    def __init__(self, client: ExchangeRateAPIClient) -> None:
        self._client = client

    def _get_mid_rate_between_different_currencies(
        self, from_currency: str, to_currency: str
    ) -> float:
        try:
            return self._client.get_rates_from(from_currency).rates[to_currency]

        except KeyError:
            raise ConversionError()


class ExchangeRateAPIFacade(BaseCurrencyConversionService):
    """
    Implements CurrencyConversionService and uses ExchangeRateAPIClient
    """

    def __init__(
        self,
        client: ExchangeRateAPIClient = ExchangeRateAPIRemoteClient(HttpxAPIClient()),
    ) -> None:
        super().__init__(ExchangeRateAPIAdapter(client))
