from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.campaigns import ReceiptDiscount
from finalproject.service.exceptions import ReceiptDiscountNotFound
from finalproject.service.campaigns.receipt_discounts import ReceiptDiscountService
from finalproject.store.receipt_discount import ReceiptDiscountStore

receipt_discount_api = APIRouter()

class _Distributor(Protocol):
    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass
    
class ReceiptDiscountRequest(BaseModel):
    minimum_total: float
    discount: float


class SingleReceiptDiscountResponse(BaseModel):
    receipt_discount: ReceiptDiscount


class ListReceiptDiscountsResponse(BaseModel):
    receipt_discounts: list[ReceiptDiscount]
    
def get_receipt_discount_service(
        request: Request
) -> ReceiptDiscountService:
    distributor: _Distributor = request.app.state.distributor
    return ReceiptDiscountService(
        distributor.receipt_discounts(),
    )

@receipt_discount_api.post(
    "/",
    status_code=201,
    response_model=SingleReceiptDiscountResponse,
)
def add_receipt_discount(
    receipt_discount_request: ReceiptDiscountRequest,
    receipt_discount_service: ReceiptDiscountService = Depends(get_receipt_discount_service),
) -> SingleReceiptDiscountResponse:
    receipt_discount = ReceiptDiscount(
        id="",
        minimum_total=receipt_discount_request.minimum_total,
        discount=receipt_discount_request.discount,
    )
    receipt_discount_service.add_receipt_discount(receipt_discount)
    return SingleReceiptDiscountResponse(receipt_discount=receipt_discount)


@receipt_discount_api.get(
    "/{receipt_discount_id}",
    status_code=200,
    response_model=SingleReceiptDiscountResponse,
)
def get_receipt_discount(
    receipt_discount_id: str,
    receipt_discount_service: ReceiptDiscountService = Depends(get_receipt_discount_service),
) -> SingleReceiptDiscountResponse:
    try:
        receipt_discount = receipt_discount_service.get_receipt_discount(receipt_discount_id)
        return SingleReceiptDiscountResponse(receipt_discount=receipt_discount)
    except ReceiptDiscountNotFound:
        raise HTTPException(status_code=404, detail="Receipt discount not found")


@receipt_discount_api.patch(
    "/{receipt_discount_id}",
    status_code=200,
    response_model=None,
)
def remove_receipt_discount(
    receipt_discount_id: str,
    receipt_discount_service: ReceiptDiscountService = Depends(get_receipt_discount_service),
) -> None:
    try:
        receipt_discount_service.remove_receipt_discount(receipt_discount_id)
    except ReceiptDiscountNotFound:
        raise HTTPException(status_code=404, detail="Receipt discount not found")


@receipt_discount_api.get(
    "/",
    status_code=200,
    response_model=ListReceiptDiscountsResponse,
)
def list_receipt_discounts(
    receipt_discount_service: ReceiptDiscountService = Depends(get_receipt_discount_service),
) -> ListReceiptDiscountsResponse:
    receipt_discounts = receipt_discount_service.get_all_receipt_discounts()
    return ListReceiptDiscountsResponse(receipt_discounts=receipt_discounts)