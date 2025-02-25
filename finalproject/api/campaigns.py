from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.campaigns import ComboItem, Combo, ProductDiscount, BuyNGetN, ReceiptDiscount
from finalproject.service.campaigns import CampaignService
from finalproject.service.exceptions import ComboNotFound, ProductDiscountNotFound, BuyNGetNNotFound, \
    ReceiptDiscountNotFound
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt_discount import ReceiptDiscountStore

campaigns_api = APIRouter()

class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass

    def combos(self) -> ComboStore:
        pass

    def combo_items(self) -> ComboItemStore:
        pass

    def product_discount(self) -> ProductDiscountStore:
        pass

    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass

class ComboRequest(BaseModel):
    name: str
    items: list[ComboItem]
    discount: float

class SingleComboResponse(BaseModel):
    combo: Combo

class ListCombosResponse(BaseModel):
    combos: list[Combo]

class ProductDiscountRequest(BaseModel):
    product_id: str
    discount: float

class SingleProductDiscountResponse(BaseModel):
    product_discount: ProductDiscount

class ListProductDiscountsResponse(BaseModel):
    product_discounts: list[ProductDiscount]

class BuyNGetNRequest(BaseModel):
    buy_product_id: str
    buy_product_n: int
    get_product_id: str
    get_product_n: int

class SingleBuyNGetNResponse(BaseModel):
    buy_n_get_n: BuyNGetN

class ListBuyNGetNsResponse(BaseModel):
    buy_n_get_ns: list[BuyNGetN]

class ReceiptDiscountRequest(BaseModel):
    minimum_total: float
    discount: float

class SingleReceiptDiscountResponse(BaseModel):
    receipt_discount: ReceiptDiscount

class ListReceiptDiscountsResponse(BaseModel):
    receipt_discounts: list[ReceiptDiscount]

def get_campaign_service(request: Request) -> CampaignService:
    distributor: _Distributor = request.app.state.distributor
    return CampaignService(
        distributor.products(),
        distributor.buy_n_get_n(),
        distributor.combos(),
        distributor.combo_items(),
        distributor.product_discount(),
        distributor.receipt_discounts(),
    )

@campaigns_api.get(
    "/combos",
    status_code=200,
    response_model=ListCombosResponse,
)
def list_combos(
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> ListCombosResponse:
    combos = campaign_service.get_all_combos()
    return ListCombosResponse(combos=combos)

@campaigns_api.post(
    "/combos",
    status_code=201,
    response_model=SingleComboResponse,
)
def add_combo(
    combo_request: ComboRequest,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleComboResponse:
    combo = Combo(id='', name=combo_request.name, items=combo_request.items, discount=combo_request.discount)
    campaign_service.add_combo(combo)
    return SingleComboResponse(combo=combo)

@campaigns_api.get(
    "/combos/{combo_id}",
    status_code=200,
    response_model=SingleComboResponse,
)
def get_combo(
    combo_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleComboResponse:
    try:
        combo = campaign_service.get_combo(combo_id)
        return SingleComboResponse(combo=combo)
    except ComboNotFound:
        raise HTTPException(status_code=404, detail="Combo not found")

@campaigns_api.patch(
    "/combos/{combo_id}",
    status_code=200,
    response_model=None,
)
def remove_combo(
    combo_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> None:
    try:
        campaign_service.remove_combo(combo_id)
    except ComboNotFound:
        raise HTTPException(status_code=404, detail="Combo not found")

@campaigns_api.post(
    "/product_discounts",
    status_code=201,
    response_model=SingleProductDiscountResponse,
)
def add_product_discount(
    product_discount_request: ProductDiscountRequest,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleProductDiscountResponse:
    product_discount = ProductDiscount(id='', product_id=product_discount_request.product_id, discount=product_discount_request.discount)
    campaign_service.add_product_discount(product_discount)
    return SingleProductDiscountResponse(product_discount=product_discount)

@campaigns_api.get(
    "/product_discounts/{product_discount_id}",
    status_code=200,
    response_model=SingleProductDiscountResponse,
)
def get_product_discount(
    product_discount_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleProductDiscountResponse:
    try:
        product_discount = campaign_service.get_product_discount(product_discount_id)
        return SingleProductDiscountResponse(product_discount=product_discount)
    except ProductDiscountNotFound:
        raise HTTPException(status_code=404, detail="Product discount not found")

@campaigns_api.patch(
    "/product_discounts/{product_discount_id}",
    status_code=200,
    response_model=None,
)
def remove_product_discount(
    product_discount_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> None:
    try:
        campaign_service.remove_product_discount(product_discount_id)
    except ProductDiscountNotFound:
        raise HTTPException(status_code=404, detail="Product discount not found")

@campaigns_api.get(
    "/product_discounts",
    status_code=200,
    response_model=ListProductDiscountsResponse,
)
def list_product_discounts(
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> ListProductDiscountsResponse:
    product_discounts = campaign_service.get_all_product_discounts()
    return ListProductDiscountsResponse(product_discounts=product_discounts)

@campaigns_api.post(
    "/buy_n_get_n",
    status_code=201,
    response_model=SingleBuyNGetNResponse,
)
def add_buy_n_get_n(
    buy_n_get_n_request: BuyNGetNRequest,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleBuyNGetNResponse:
    buy_n_get_n = BuyNGetN(id='',
                           buy_product_id=buy_n_get_n_request.buy_product_id,
                           buy_product_n=buy_n_get_n_request.buy_product_n,
                           get_product_id=buy_n_get_n_request.get_product_id,
                           get_product_n=buy_n_get_n_request.get_product_n
                           )
    campaign_service.add_buy_n_get_n(buy_n_get_n)
    return SingleBuyNGetNResponse(buy_n_get_n=buy_n_get_n)

@campaigns_api.get(
    "/buy_n_get_n/{buy_n_get_n_id}",
    status_code=200,
    response_model=SingleBuyNGetNResponse,
)
def get_buy_n_get_n(
    buy_n_get_n_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleBuyNGetNResponse:
    try:
        buy_n_get_n = campaign_service.get_buy_n_get_n(buy_n_get_n_id)
        return SingleBuyNGetNResponse(buy_n_get_n=buy_n_get_n)
    except BuyNGetNNotFound:
        raise HTTPException(status_code=404, detail="Buy N Get N not found")

@campaigns_api.patch(
    "/buy_n_get_n/{buy_n_get_n_id}",
    status_code=200,
    response_model=None,
)
def remove_buy_n_get_n(
    buy_n_get_n_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> None:
    try:
        campaign_service.remove_buy_n_get_n(buy_n_get_n_id)
    except BuyNGetNNotFound:
        raise HTTPException(status_code=404, detail="Buy N Get N not found")

@campaigns_api.get(
    "/buy_n_get_n",
    status_code=200,
    response_model=ListBuyNGetNsResponse,
)
def list_buy_n_get_ns(
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> ListBuyNGetNsResponse:
    buy_n_get_ns = campaign_service.get_all_buy_n_get_ns()
    return ListBuyNGetNsResponse(buy_n_get_ns=buy_n_get_ns)

@campaigns_api.post(
    "/receipt_discounts",
    status_code=201,
    response_model=SingleReceiptDiscountResponse,
)
def add_receipt_discount(
    receipt_discount_request: ReceiptDiscountRequest,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleReceiptDiscountResponse:
    receipt_discount = ReceiptDiscount(id='',
                                       minimum_total=receipt_discount_request.minimum_total,
                                       discount=receipt_discount_request.discount
                                       )
    campaign_service.add_receipt_discount(receipt_discount)
    return SingleReceiptDiscountResponse(receipt_discount=receipt_discount)

@campaigns_api.get(
    "/receipt_discounts/{receipt_discount_id}",
    status_code=200,
    response_model=SingleReceiptDiscountResponse,
)
def get_receipt_discount(
    receipt_discount_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> SingleReceiptDiscountResponse:
    try:
        receipt_discount = campaign_service.get_receipt_discount(receipt_discount_id)
        return SingleReceiptDiscountResponse(receipt_discount=receipt_discount)
    except ReceiptDiscountNotFound:
        raise HTTPException(status_code=404, detail="Receipt discount not found")

@campaigns_api.patch(
    "/receipt_discounts/{receipt_discount_id}",
    status_code=200,
    response_model=None,
)
def remove_receipt_discount(
    receipt_discount_id: str,
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> None:
    try:
        campaign_service.remove_receipt_discount(receipt_discount_id)
    except ReceiptDiscountNotFound:
        raise HTTPException(status_code=404, detail="Receipt discount not found")

@campaigns_api.get(
    "/receipt_discounts",
    status_code=200,
    response_model=ListReceiptDiscountsResponse,
)
def list_receipt_discounts(
    campaign_service: CampaignService = Depends(get_campaign_service),
) -> ListReceiptDiscountsResponse:
    receipt_discounts = campaign_service.get_all_receipt_discounts()
    return ListReceiptDiscountsResponse(receipt_discounts=receipt_discounts)