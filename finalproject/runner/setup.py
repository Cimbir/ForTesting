from finalproject.api.api import (
    APIUsingFastAPI,
    RunFastAPIStrategy,
)
from finalproject.app.app import App, DefaultApp
from finalproject.store.distributor import SQLiteStoreDistributor, StoreDistributor


def setup(run_strategy: RunFastAPIStrategy, database: str) -> App:
    store_distributor = SQLiteStoreDistributor(database)

    api = APIUsingFastAPI(run_strategy)

    return DefaultApp(store_distributor).with_api(api)


def mock_setup(run_strategy: RunFastAPIStrategy, distributor: StoreDistributor) -> App:
    api = APIUsingFastAPI(run_strategy)

    return DefaultApp(distributor).with_api(api)
