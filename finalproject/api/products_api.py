from typing import Protocol

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.store.product import ProductRecord, ProductStore

products_api = APIRouter()


class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


class SingleProductResponse(BaseModel):
    product: ProductResponse


class ListProductsResponse(BaseModel):
    products: list[ProductResponse]


def get_product_store(request: Request) -> ProductStore:
    distributor: _Distributor = request.app.state.distributor

    return distributor.products()


def get_product_response(product: ProductRecord) -> ProductResponse:
    return ProductResponse(id=product.id, name=product.name, price=product.price)


@products_api.get(
    "",
    status_code=200,
    response_model=ProductResponse,
)
def list_products(
    product_store: ProductStore = Depends(get_product_store),
) -> ListProductsResponse:
    products = product_store.list_all()
    return ListProductsResponse(
        products=[get_product_response(product) for product in products]
    )
