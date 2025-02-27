from __future__ import annotations

from typing import Any, Protocol

from apexdevkit.server import UvicornServer
from fastapi import FastAPI
from starlette.testclient import TestClient

from finalproject.api.campaigns.buy_n_get_n import buy_n_get_n_api
from finalproject.api.campaigns.combos import combos_api
from finalproject.api.campaigns.product_discounts import product_discounts_api
from finalproject.api.campaigns.receipt_discounts import receipt_discount_api
from finalproject.api.products import products_api
from finalproject.api.receipts import receipts_api


class API(Protocol):
    def run(self) -> None:
        pass

    def register_state(self, name: str, state: Any) -> None:
        pass


class APIUsingFastAPI:
    def __init__(self, run_strategy: RunFastAPIStrategy) -> None:
        self._fast_api = FastAPI()
        self._register_routes()
        self._run_strategy = run_strategy

    def _register_routes(self) -> None:
        self._fast_api.include_router(
            products_api, prefix="/products", tags=["Products"]
        )
        self._fast_api.include_router(
            receipts_api, prefix="/receipts", tags=["Receipts"]
        )
        self._fast_api.include_router(
            product_discounts_api,
            prefix="/product_discounts",
            tags=["ProductDiscounts"],
        )
        self._fast_api.include_router(
            receipt_discount_api, prefix="/receipt_discounts", tags=["ReceiptDiscounts"]
        )
        self._fast_api.include_router(
            buy_n_get_n_api, prefix="/buy_n_get_n", tags=["BuyNGetN"]
        )
        self._fast_api.include_router(combos_api, prefix="/combos", tags=["Combos"])

    def run(self) -> None:
        self._run_strategy.run(self._fast_api)

    def register_state(self, name: str, state: Any) -> None:
        setattr(self._fast_api.state, name, state)


class RunFastAPIStrategy(Protocol):
    def run(self, api: FastAPI) -> None:
        pass


class RunFastAPIUsingUvicorn:
    def __init__(self, port: int) -> None:
        self._port = port

    def run(self, api: FastAPI) -> None:
        UvicornServer.from_env().and_port(self._port).run(api)


class RunFastAPIUsingTestClient:
    def __init__(self) -> None:
        self._client: TestClient | None = None

    def run(self, api: FastAPI) -> None:
        self._client = TestClient(api)

    @property
    def client(self) -> TestClient:
        if self._client is None:
            raise ValueError("TestClient not set")
        return self._client
