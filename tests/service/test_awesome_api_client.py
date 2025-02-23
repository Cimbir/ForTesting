from unittest.mock import MagicMock, Mock, patch

import pytest

from finalproject.service.awesome_api_client import (
    AWESOME_API_GET_EXCHANGE_RATE_PATH_FORMAT,
    AwesomeAPIRequestFailed,
    DefaultAwesomeAPIClient,
)
from finalproject.service.http_client import HttpxAPIClient


@patch("httpx.get")
def test_should_raise_error_when_status_code_is_not_200(mock_get: MagicMock) -> None:
    client = DefaultAwesomeAPIClient(http_client=HttpxAPIClient())

    # Make server return 404 not found error
    mock_response = Mock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    pytest.raises(AwesomeAPIRequestFailed, client.get_exchange_rate, "USD", "GEL")


@patch("httpx.get")
def test_should_raise_error_when_server_returns_invalid_response(
    mock_get: MagicMock,
) -> None:
    client = DefaultAwesomeAPIClient(http_client=HttpxAPIClient())

    # Make server return malformed json
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # This should raise KeyError
    mock_response.json.return_value = {"some_random_key": "some_random_value"}
    pytest.raises(AwesomeAPIRequestFailed, client.get_exchange_rate, "USD", "GEL")

    # This should raise TypeError
    mock_response.json.return_value = {"USDGEL": "some_random_value"}
    pytest.raises(AwesomeAPIRequestFailed, client.get_exchange_rate, "USD", "GEL")

    # Make server return invalid json that raises some exception
    mock_response.json.side_effect = ValueError()
    pytest.raises(AwesomeAPIRequestFailed, client.get_exchange_rate, "USD", "GEL")


@patch("httpx.get")
def test_should_get_exchange_rate(mock_get: MagicMock) -> None:
    client = DefaultAwesomeAPIClient(
        http_client=HttpxAPIClient(), endpoint="http://127.0.0.1"
    )

    # Define fake exchange rate data
    exchange_rate_data_from_server = {
        "code": "USD",
        "codein": "GEL",
        "name": "USD/GEL",
        "high": "2.805",
        "low": "2.8",
        "varBid": "-0.005",
        "pctChange": "-0.2",
        "bid": "2.7",
        "ask": "2.8",
        "timestamp": "1740175200",
        "create_date": "2025-02-21 19:00:00",
    }

    # Create a mock response
    mock_response = Mock()
    mock_response.status_code = 200

    # This is the fake json response from the server
    mock_response.json.return_value = {"USDGEL": exchange_rate_data_from_server}

    # Every httpx.get call will return this mock response
    mock_get.return_value = mock_response

    # Use the client to fetch the fake data
    result = client.get_exchange_rate("USD", "GEL")

    # Make sure that the client called httpx.get with the correct URL
    mock_get.assert_called_once_with(
        f"http://127.0.0.1{
            AWESOME_API_GET_EXCHANGE_RATE_PATH_FORMAT.format(
                currency_from='USD', currency_to='GEL'
            )
        }"
    )

    # Make sure the data was parsed correctly
    assert result.__dict__ == exchange_rate_data_from_server
