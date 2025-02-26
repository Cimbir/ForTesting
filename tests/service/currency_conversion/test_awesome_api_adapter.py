from finalproject.service.currency_conversion.awesome_api_adapter import (
    AwesomeAPIAdapter,
    AwesomeAPIFacade,
    AwesomeAPIFindAnyExchangeRateStrategy,
)
from finalproject.service.currency_conversion.awesome_api_client import (
    FakeAwesomeAPIClient,
    GetExchangeRateResponse,
)
from finalproject.service.currency_conversion.currency_conversion import (
    CurrencyConversionService,
    MockMidExchangeRateRetriever,
)


def test_should_calculate_mid_exchange_rate_from_bid_and_ask() -> None:
    fake_client = FakeAwesomeAPIClient()

    response1 = GetExchangeRateResponse(bid="2.5", ask="1.5")
    adapter = AwesomeAPIAdapter(fake_client.with_fake_response(response1))
    assert adapter.get_mid_rate("USD", "GEL") == 2.0

    response2 = GetExchangeRateResponse(bid="2.8", ask="2.9")
    adapter = AwesomeAPIAdapter(fake_client.with_fake_response(response2))
    assert adapter.get_mid_rate("USD", "GEL") == float(2.8 + 2.9) / 2.0


def test_should_execute_correct_strategy_to_find_exchange_rates() -> None:
    mock_rate_retriever = MockMidExchangeRateRetriever()
    rate_calculator = AwesomeAPIFindAnyExchangeRateStrategy(
        client=mock_rate_retriever, mediator_currency="USD"
    )

    mock_rate_retriever.add_rate("USD", "GEL", 2.7)
    assert rate_calculator.get_mid_rate("USD", "GEL") == 2.7

    mock_rate_retriever.add_rate("USD", "EUR", 0.8)
    assert rate_calculator.get_mid_rate("EUR", "USD") == 1.0 / 0.8

    mock_rate_retriever.add_rate("USD", "JPY", 150)
    mock_rate_retriever.add_rate("USD", "GEL", 2.8)
    assert rate_calculator.get_mid_rate("JPY", "GEL") == 2.8 / 150
    assert rate_calculator.get_mid_rate("GEL", "JPY") == 150 / 2.8


def test_should_use_facade_to_setup_service() -> None:
    fake_client = FakeAwesomeAPIClient().with_fake_response(
        GetExchangeRateResponse(bid="3", ask="2")
    )

    service: CurrencyConversionService = AwesomeAPIFacade(fake_client)
    assert service.convert(100, "USD", "GEL") == 250.0
