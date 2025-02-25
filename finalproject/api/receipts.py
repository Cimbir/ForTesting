from typing import Protocol

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request

from finalproject.models.models import Receipt
from finalproject.service.currency_conversion import CurrencyConversionService
from finalproject.service.receipts import ReceiptService
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt import ReceiptStore
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.receipt_item import ReceiptItemStore
from finalproject.store.shift import ShiftStore

receipts_api = APIRouter()

class _Distributor(Protocol):
    def receipts(self) -> ReceiptStore:
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
    def product_discounts(self) -> ProductDiscountStore:
        pass
    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass
    def buy_n_get_ns(self) -> BuyNGetNStore:
        pass



class CreateReceiptRequest(BaseModel):
    shift_id: str

class AddItemRequest(BaseModel):
    product_id: str
    quantity: int



class ReceiptItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    price: float
    total: float

class ReceiptResponse(BaseModel):
    id: str
    open: bool
    paid: float
    shift_id: str
    items: list[ReceiptItemResponse]

class SingleReceiptResponse(BaseModel):
    receipt: ReceiptResponse

class ListReceiptsResponse(BaseModel):
    receipts: list[ReceiptResponse]

class ReceiptCostResponse(BaseModel):
    GEL: float
    USD: float
    EUR: float



def get_receipt_service(request: Request) -> ReceiptService:
    distributor: _Distributor = request.app.state.distributor

    return ReceiptService(
        distributor.receipts(),
        distributor.receipt_items(),
        distributor.shifts(),
        distributor.products(),
        distributor.combos(),
        distributor.combo_items(),
        distributor.product_discounts(),
        distributor.receipt_discounts(),
        distributor.buy_n_get_ns(),
    )

# !!! CURRENCY CONVERSION !!!


@receipts_api.post(
    "",
    status_code=201,
    response_model=SingleReceiptResponse,
)
def create_receipt(
    request: CreateReceiptRequest,
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> SingleReceiptResponse:
    receipt = Receipt(
        id="",
        open=True,
        paid=0,
        shift_id=request.shift_id,
        items=[],
    )
    receipt = receipt_service.add_receipt(receipt)
    return SingleReceiptResponse(receipt=ReceiptResponse(
        id=receipt.id,
        open=receipt.open,
        paid=receipt.paid,
        shift_id=receipt.shift_id,
        items=[],
    )
)

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
    receipt = receipt_service.update_product_in_receipt(receipt_id, request.product_id, request.quantity)
    return SingleReceiptResponse(receipt=ReceiptResponse(
        id=receipt.id,
        open=receipt.open,
        paid=receipt.paid,
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