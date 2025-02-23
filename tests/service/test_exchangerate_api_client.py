from unittest.mock import MagicMock, Mock, patch

from finalproject.service.exchangerate_api_client import (
    EXCHANGE_RATE_API_GET_RATES_FORMAT,
    ExchangeRateAPIRemoteClient,
)
from finalproject.service.http_client import HttpxAPIClient


@patch("httpx.get")
def test_should_get_exchange_rate(mock_get: MagicMock) -> None:
    client = ExchangeRateAPIRemoteClient(
        http_client=HttpxAPIClient(), endpoint="http://127.0.0.1"
    )

    # Define fake exchange rate data
    exchange_rate_data_from_server = {
        "result": "success",
        "provider": "provider_site",
        "documentation": "documentation_url",
        "terms_of_use": "some_string",
        "time_last_update_unix": 1740268950,
        "time_last_update_utc": "last_update_time_string",
        "time_next_update_unix": 1740357100,
        "time_next_update_utc": "next_update_time_string",
        "time_eol_unix": 0,
        "base_code": "USD",
        "rates": {
            "USD": 1,
            "GEL": 2.8,
            "EUR": 0.9,
        },
    }

    # Create a mock response
    mock_response = Mock()
    mock_response.status_code = 200

    # This is the fake json response from the server
    mock_response.json.return_value = exchange_rate_data_from_server

    # Every httpx.get call will return this mock response
    mock_get.return_value = mock_response

    # Use the client to fetch the fake data
    result = client.get_rates_from("USD")

    # Make sure that the client called httpx.get with the correct URL
    mock_get.assert_called_once_with(
        f"http://127.0.0.1{EXCHANGE_RATE_API_GET_RATES_FORMAT.format(currency='USD')}"
    )

    # Make sure the data was parsed correctly
    assert result.__dict__ == exchange_rate_data_from_server
