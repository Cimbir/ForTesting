from finalproject.service.currency_conversion.currency_conversion import CurrencyConversionService
from finalproject.service.currency_conversion.exchangerate_api_adapter import (
    ExchangeRateAPIAdapter,
    ExchangeRateAPIFacade,
)
from finalproject.service.currency_conversion.exchangerate_api_client import (
    ExchangeRateAPIFakeClient,
    ExchangeRatesFromResponse,
)


def test_should_get_exchange_rate_from_api_response() -> None:
    response = ExchangeRatesFromResponse(
        base_code="USD",
        rates={"GEL": 2.5, "EUR": 0.8},
    )
    adapter = ExchangeRateAPIAdapter(ExchangeRateAPIFakeClient(fake_response=response))

    assert adapter.get_mid_rate("USD", "GEL") == 2.5
    assert adapter.get_mid_rate("USD", "EUR") == 0.8


def test_should_convert_given_amount_using_facade_class() -> None:
    response = ExchangeRatesFromResponse(
        base_code="GEL",
        rates={"USD": 0.33, "EUR": 0.2},
    )
    service: CurrencyConversionService = ExchangeRateAPIFacade(
        ExchangeRateAPIFakeClient(fake_response=response)
    )

    assert service.convert(120, "GEL", "USD") == 0.33 * 120
    assert service.convert(100, "GEL", "EUR") == 0.2 * 100
