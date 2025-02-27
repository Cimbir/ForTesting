from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.campaigns import BuyNGetN
from finalproject.service.campaigns.buy_n_get_n import BuyNGetNService
from finalproject.service.exceptions import BuyNGetNNotFound
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.product import ProductStore

buy_n_get_n_api = APIRouter()


class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass


class BuyNGetNRequest(BaseModel):
    buy_product_id: str
    buy_product_n: int
    get_product_id: str
    get_product_n: int


class SingleBuyNGetNResponse(BaseModel):
    buy_n_get_n: BuyNGetN


class ListBuyNGetNsResponse(BaseModel):
    buy_n_get_ns: list[BuyNGetN]


def get_buy_n_get_n_service(request: Request) -> BuyNGetNService:
    distributor: _Distributor = request.app.state.distributor
    return BuyNGetNService(
        distributor.products(),
        distributor.buy_n_get_n(),
    )


@buy_n_get_n_api.post(
    "/",
    status_code=201,
    response_model=SingleBuyNGetNResponse,
)
def add_buy_n_get_n(
    buy_n_get_n_request: BuyNGetNRequest,
    campaign_service: BuyNGetNService = Depends(get_buy_n_get_n_service),
) -> SingleBuyNGetNResponse:
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id=buy_n_get_n_request.buy_product_id,
        buy_product_n=buy_n_get_n_request.buy_product_n,
        get_product_id=buy_n_get_n_request.get_product_id,
        get_product_n=buy_n_get_n_request.get_product_n,
    )
    campaign_service.add_buy_n_get_n(buy_n_get_n)
    return SingleBuyNGetNResponse(buy_n_get_n=buy_n_get_n)


@buy_n_get_n_api.get(
    "/{buy_n_get_n_id}",
    status_code=200,
    response_model=SingleBuyNGetNResponse,
)
def get_buy_n_get_n(
    buy_n_get_n_id: str,
    campaign_service: BuyNGetNService = Depends(get_buy_n_get_n_service),
) -> SingleBuyNGetNResponse:
    try:
        buy_n_get_n = campaign_service.get_buy_n_get_n(buy_n_get_n_id)
        return SingleBuyNGetNResponse(buy_n_get_n=buy_n_get_n)
    except BuyNGetNNotFound:
        raise HTTPException(status_code=404, detail="Buy N Get N not found")


@buy_n_get_n_api.patch(
    "/{buy_n_get_n_id}",
    status_code=200,
    response_model=None,
)
def remove_buy_n_get_n(
    buy_n_get_n_id: str,
    campaign_service: BuyNGetNService = Depends(get_buy_n_get_n_service),
) -> None:
    try:
        campaign_service.remove_buy_n_get_n(buy_n_get_n_id)
    except BuyNGetNNotFound:
        raise HTTPException(status_code=404, detail="Buy N Get N not found")


@buy_n_get_n_api.get(
    "/",
    status_code=200,
    response_model=ListBuyNGetNsResponse,
)
def list_buy_n_get_ns(
    campaign_service: BuyNGetNService = Depends(get_buy_n_get_n_service),
) -> ListBuyNGetNsResponse:
    buy_n_get_ns = campaign_service.get_all_buy_n_get_ns()
    return ListBuyNGetNsResponse(buy_n_get_ns=buy_n_get_ns)
