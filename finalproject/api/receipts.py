from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from finalproject.models.models import Receipt
from finalproject.service.currency_conversion.currency_conversion import (
    CurrencyConversionService,
)
from finalproject.service.currency_conversion.exchangerate_api_adapter import (
    ExchangeRateAPIFacade,
)
from finalproject.service.exceptions import (
    ProductNotFound,
    ReceiptNotFound,
    ShiftNotFound,
)
from finalproject.service.receipts import ReceiptService
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.paid_receipt import PaidReceiptStore
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt import ReceiptStore
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.receipt_item import ReceiptItemStore
from finalproject.store.shift import ShiftStore

receipts_api = APIRouter()


class _Distributor(Protocol):
    def receipt(self) -> ReceiptStore:
        pass

    def receipt_items(self) -> ReceiptItemStore:
        pass

    def products(self) -> ProductStore:
        pass

    def shifts(self) -> ShiftStore:
        pass

    def combos(self) -> ComboStore:
        pass

    def combo_items(self) -> ComboItemStore:
        pass

    def product_discount(self) -> ProductDiscountStore:
        pass

    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass

    def paid_receipts(self) -> PaidReceiptStore:
        pass


class CreateReceiptRequest(BaseModel):
    shift_id: str


class AddItemRequest(BaseModel):
    product_id: str
    quantity: int


class PayReceiptRequest(BaseModel):
    currency: str


class ReceiptItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    price: float
    total: float


class ReceiptResponse(BaseModel):
    id: str
    open: bool
    shift_id: str
    items: list[ReceiptItemResponse]


class SingleReceiptResponse(BaseModel):
    receipt: ReceiptResponse


class ListReceiptsResponse(BaseModel):
    receipts: list[ReceiptResponse]


class ReceiptCostResponse(BaseModel):
    receipt_id: str
    GEL: float
    USD: float
    EUR: float


class DiscountResponse(BaseModel):
    receipt_id: str
    discount_in_GEL: float
    final_cost_in_GEL: float


def get_receipt_service(request: Request) -> ReceiptService:
    distributor: _Distributor = request.app.state.distributor

    return ReceiptService(
        distributor.receipt(),
        distributor.receipt_items(),
        distributor.shifts(),
        distributor.products(),
        distributor.paid_receipts(),
        distributor.combos(),
        distributor.combo_items(),
        distributor.product_discount(),
        distributor.receipt_discounts(),
        distributor.buy_n_get_n(),
        ExchangeRateAPIFacade(),
    )


def get_currency_conversion_service(request: Request) -> CurrencyConversionService:
    return ExchangeRateAPIFacade()


@receipts_api.post(
    "",
    status_code=201,
    response_model=SingleReceiptResponse,
)
def create_receipt(
    request: CreateReceiptRequest,
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> SingleReceiptResponse:
    try:
        receipt = Receipt(shift_id=request.shift_id)
        receipt = receipt_service.add_receipt(receipt)
        return SingleReceiptResponse(
            receipt=ReceiptResponse(
                id=receipt.id,
                open=receipt.open,
                shift_id=receipt.shift_id,
                items=[],
            )
        )
    except ShiftNotFound:
        raise HTTPException(status_code=404, detail="Shift not found")


@receipts_api.post(
    "/{receipt_id}/products",
    status_code=201,
    response_model=SingleReceiptResponse,
)
def add_item(
    receipt_id: str,
    request: AddItemRequest,
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> SingleReceiptResponse:
    try:
        receipt = receipt_service.update_product_in_receipt(
            receipt_id, request.product_id, request.quantity
        )
        return SingleReceiptResponse(
            receipt=ReceiptResponse(
                id=receipt.id,
                open=receipt.open,
                shift_id=receipt.shift_id,
                items=[
                    ReceiptItemResponse(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        total=item.quantity * item.price,
                    )
                    for item in receipt.items
                ],
            )
        )
    except ProductNotFound:
        raise HTTPException(status_code=404, detail="Product not found")
    except ReceiptNotFound:
        raise HTTPException(status_code=404, detail="Receipt not found")


@receipts_api.get(
    "/{receipt_id}/quotes",
    status_code=200,
    response_model=ReceiptCostResponse,
)
def calculate_payment(
    receipt_id: str,
    receipt_service: ReceiptService = Depends(get_receipt_service),
    currency_conversion_service: CurrencyConversionService = Depends(
        get_currency_conversion_service
    ),
) -> ReceiptCostResponse:
    try:
        receipt_cost = receipt_service.get_receipt_cost(receipt_id)
        return ReceiptCostResponse(
            receipt_id=receipt_id,
            GEL=receipt_cost,
            USD=currency_conversion_service.convert(receipt_cost, "GEL", "USD"),
            EUR=currency_conversion_service.convert(receipt_cost, "GEL", "EUR"),
        )
    except ReceiptNotFound:
        raise HTTPException(status_code=404, detail="Receipt not found")


@receipts_api.get(
    "/{receipt_id}/discount",
    status_code=200,
    response_model=DiscountResponse,
)
def calculate_discount(
    receipt_id: str,
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> DiscountResponse:
    try:
        discount = receipt_service.get_receipt_discount_amount(receipt_id)
        return DiscountResponse(
            receipt_id=receipt_id,
            discount_in_GEL=discount,
            final_cost_in_GEL=receipt_service.get_receipt_cost(receipt_id),
        )
    except ReceiptNotFound:
        raise HTTPException(status_code=404, detail="Receipt not found")


@receipts_api.post(
    "/{receipt_id}/payments",
    status_code=201,
    response_model=SingleReceiptResponse,
)
def pay_receipt(
    receipt_id: str,
    request: PayReceiptRequest,
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> SingleReceiptResponse:
    try:
        closed = receipt_service.close_receipt(receipt_id, request.currency)
        return SingleReceiptResponse(
            receipt=ReceiptResponse(
                id=closed.id,
                open=closed.open,
                shift_id=closed.shift_id,
                items=[
                    ReceiptItemResponse(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        total=item.quantity * item.price,
                    )
                    for item in closed.items
                ],
            )
        )
    except ReceiptNotFound:
        raise HTTPException(status_code=404, detail="Receipt not found")
