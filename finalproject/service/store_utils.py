import uuid

from finalproject.service.exceptions import ProductNotFound
from finalproject.store.product import ProductStore
from finalproject.store.store import RecordNotFound


def generate_id() -> str:
    return str(uuid.uuid4())


def check_correct_currency_name(currency_name: str) -> bool:
    return currency_name in ["USD", "EUR", "GEL"]

def _validate_product(product_store: ProductStore, product_id: str) -> None:
    try:
        product_store.get_by_id(product_id)
    except RecordNotFound:
        raise ProductNotFound(product_id)
