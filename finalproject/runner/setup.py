from fastapi import FastAPI

from finalproject.api.products_api import products_api
from finalproject.store.distributor import SQLiteStoreDistributor


def setup() -> FastAPI:
    api = FastAPI()

    api.state.distributor = SQLiteStoreDistributor("pos.db")

    api.include_router(products_api, prefix="/products", tags=["Products"])

    return api
