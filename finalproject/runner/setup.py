from finalproject.api.api import (
    APIUsingFastAPI,
    RunFastAPIStrategy,
)
from finalproject.app.app import App, DefaultApp
from finalproject.store.distributor import SQLiteStoreDistributor

PERSISTENT_DATABASE_PATH = "pos.db"


def setup(run_strategy: RunFastAPIStrategy) -> App:
    store_distributor = SQLiteStoreDistributor(PERSISTENT_DATABASE_PATH)

    api = APIUsingFastAPI(run_strategy)

    return DefaultApp(store_distributor).with_api(api)
