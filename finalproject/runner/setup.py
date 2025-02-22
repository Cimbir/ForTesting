from finalproject.api.api import (
    APIUsingFastAPI,
    RunFastAPIStrategy,
)
from finalproject.app.app import App, DefaultApp
from finalproject.store.distributor import SQLiteStoreDistributor


def setup(run_strategy: RunFastAPIStrategy, database: str) -> App:
    store_distributor = SQLiteStoreDistributor(database)

    api = APIUsingFastAPI(run_strategy)

    return DefaultApp(store_distributor).with_api(api)
