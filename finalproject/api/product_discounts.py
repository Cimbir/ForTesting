from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.campaigns import ProductDiscount
from finalproject.service.exceptions import ProductDiscountNotFound
from finalproject.service.product_discounts import ProductDiscountService
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore

product_discounts_api = APIRouter()

class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def product_discount(self) -> ProductDiscountStore:
        pass

class ProductDiscountRequest(BaseModel):
    product_id: str
    discount: float


class SingleProductDiscountResponse(BaseModel):
    product_discount: ProductDiscount


class ListProductDiscountsResponse(BaseModel):
    product_discounts: list[ProductDiscount]

def get_product_discount_service(
        request: Request
) -> ProductDiscountService:
    distributor: _Distributor = request.app.state.distributor
    return ProductDiscountService(
        distributor.products(),
        distributor.product_discount(),
    )

@product_discounts_api.post(
    "/",
    status_code=201,
    response_model=SingleProductDiscountResponse,
)
def add_product_discount(
    product_discount_request: ProductDiscountRequest,
    product_discount_service: ProductDiscountService = Depends(get_product_discount_service),
) -> SingleProductDiscountResponse:
    product_discount = ProductDiscount(
        id="",
        product_id=product_discount_request.product_id,
        discount=product_discount_request.discount,
    )
    product_discount_service.add_product_discount(product_discount)
    return SingleProductDiscountResponse(product_discount=product_discount)


@product_discounts_api.get(
    "/{product_discount_id}",
    status_code=200,
    response_model=SingleProductDiscountResponse,
)
def get_product_discount(
    product_discount_id: str,
    product_discount_service: ProductDiscountService = Depends(get_product_discount_service),
) -> SingleProductDiscountResponse:
    try:
        product_discount = product_discount_service.get_product_discount(product_discount_id)
        return SingleProductDiscountResponse(product_discount=product_discount)
    except ProductDiscountNotFound:
        raise HTTPException(status_code=404, detail="Product discount not found")


@product_discounts_api.patch(
    "/{product_discount_id}",
    status_code=200,
    response_model=None,
)
def remove_product_discount(
    product_discount_id: str,
    product_discount_service: ProductDiscountService = Depends(get_product_discount_service),
) -> None:
    try:
        product_discount_service.remove_product_discount(product_discount_id)
    except ProductDiscountNotFound:
        raise HTTPException(status_code=404, detail="Product discount not found")


@product_discounts_api.get(
    "/",
    status_code=200,
    response_model=ListProductDiscountsResponse,
)
def list_product_discounts(
    product_discount_service: ProductDiscountService = Depends(get_product_discount_service),
) -> ListProductDiscountsResponse:
    product_discounts = product_discount_service.get_all_product_discounts()
    return ListProductDiscountsResponse(product_discounts=product_discounts)