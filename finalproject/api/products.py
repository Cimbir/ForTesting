from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.product import Product
from finalproject.service.exceptions import ProductNotFound
from finalproject.service.products import ProductService
from finalproject.store.product import ProductStore
from finalproject.store.store import RecordAlreadyExists, RecordNotFound

products_api = APIRouter()


class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass

class ProductRequest(BaseModel):
    name: str
    price: float


class SingleProductResponse(BaseModel):
    product: Product


class ListProductsResponse(BaseModel):
    products: list[Product]


def get_product_service(request: Request) -> ProductService:
    distributor: _Distributor = request.app.state.distributor

    return ProductService(distributor.products())


@products_api.get(
    "",
    status_code=200,
    response_model=ListProductsResponse,
)
def list_products(
    product_service: ProductService = Depends(get_product_service),
) -> ListProductsResponse:
    products = product_service.get_all_products()
    return ListProductsResponse(products=products)

@products_api.post(
    "",
    status_code=201,
    response_model=SingleProductResponse,
)
def add_product(
    product_request: ProductRequest,
    product_service: ProductService = Depends(get_product_service),
) -> SingleProductResponse:
    product = Product(id='', name=product_request.name, price=product_request.price)
    product_service.add_product(product)
    return SingleProductResponse(product=product)

@products_api.get(
    "/{product_id}",
    status_code=200,
    response_model=SingleProductResponse,
)
def get_product(
    product_id: str,
    product_service: ProductService = Depends(get_product_service),
) -> SingleProductResponse:
    try:
        product = product_service.get_product(product_id)
    except ProductNotFound:
        raise HTTPException(status_code=404, detail=f"Product with id={product_id} not found")
    return SingleProductResponse(product=product)

@products_api.patch(
    "/{product_id}",
    status_code=200,
    response_model=SingleProductResponse,
)
def update_product(
    product_id: str,
    product_request: ProductRequest,
    product_service: ProductService = Depends(get_product_service),
) -> SingleProductResponse:
    product = Product(id=product_id, name=product_request.name, price=product_request.price)
    try:
        product_service.update_product(product)
    except ProductNotFound:
        raise HTTPException(status_code=404, detail=f"Product with id={product_id} not found")
    return SingleProductResponse(product=product
)