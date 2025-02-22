from __future__ import annotations

from typing import Protocol

from finalproject.api.api import API
from finalproject.store.distributor import StoreDistributor

STORE_DISTRIBUTOR_STATE_NAME = "distributor"


class App(Protocol):
    def with_api(self, api: API) -> App:
        pass

    def run_app(self) -> None:
        pass


class DefaultApp:
    def __init__(self, store_distributor: StoreDistributor):
        self._store_distributor = store_distributor
        self._api_list: list[API] = []

    def with_api(self, api: API) -> App:
        self._setup_state(api)
        self._api_list.append(api)
        return self

    def _setup_state(self, api: API) -> None:
        api.register_state(STORE_DISTRIBUTOR_STATE_NAME, self._store_distributor)
        # Add any state variables here

    def run_app(self) -> None:
        for api in self._api_list:
            api.run()
