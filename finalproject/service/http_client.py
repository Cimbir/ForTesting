from __future__ import annotations

from typing import Any, Protocol

import httpx

DEFAULT_API_ENDPOINT = "http://127.0.0.1"


class HttpAPIResponse(Protocol):
    status_code: int

    def json(self) -> Any:
        pass


class HttpAPIClient(Protocol):
    """
    We can implement this protocol with any http client library.
    """

    def with_api_endpoint(self, api_endpoint: str) -> HttpAPIClient:
        pass

    def get(self, path: str) -> HttpAPIResponse:
        """
        Returns response if and only if http status code is 200.
        Raises APICallFailedError otherwise.
        """
        pass


class HttpxAPIClient:
    def __init__(self) -> None:
        self._api_endpoint = DEFAULT_API_ENDPOINT

    def with_api_endpoint(self, api_endpoint: str) -> HttpAPIClient:
        self._api_endpoint = api_endpoint
        return self

    def get(self, path: str) -> HttpAPIResponse:
        return httpx.get(f"{self._api_endpoint}{path}")
