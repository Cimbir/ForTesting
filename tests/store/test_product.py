import pytest

from finalproject.store.distributor import StoreDistributor
from finalproject.store.product import ProductRecord
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_should_add_and_get_product(distributor: StoreDistributor) -> None:
    product_store = distributor.products()

    product = ProductRecord(id="unique-id-1", name="Product 1", price=9.99)
    product_store.add(product)

    assert product_store.get_by_id("unique-id-1") == product


def test_should_list_all_products(distributor: StoreDistributor) -> None:
    product_store = distributor.products()

    product1 = ProductRecord(id="unique-id-1", name="Product 1", price=9.99)
    product2 = ProductRecord(id="unique-id-2", name="Product 2", price=19.99)

    product_store.add(product1)
    product_store.add(product2)

    assert product1 in product_store.list_all()
    assert product2 in product_store.list_all()
    assert len(product_store.list_all()) == 2


def test_should_update_product_and_leave_others_untouched(
    distributor: StoreDistributor,
) -> None:
    product_store = distributor.products()

    product1 = ProductRecord(id="unique-id-1", name="Product 1", price=9.99)
    product2 = ProductRecord(id="unique-id-2", name="Product 2", price=19.99)

    product_store.add(product1)
    product_store.add(product2)

    updated_product_1 = ProductRecord(id="unique-id-1", name="Product 1", price=19.99)
    product_store.update(updated_product_1)

    assert product_store.get_by_id("unique-id-1") == updated_product_1
    assert product_store.get_by_id("unique-id-2") == product2


def test_should_raise_error_when_adding_product_with_same_id(
    distributor: StoreDistributor,
) -> None:
    product_store = distributor.products()

    product1 = ProductRecord(id="unique-id-1", name="Product 1", price=9.99)
    product2 = ProductRecord(id="unique-id-1", name="Product 2", price=19.99)

    product_store.add(product1)
    pytest.raises(RecordAlreadyExists, product_store.add, product2)


def test_should_raise_error_in_get_when_product_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    product_store = distributor.products()

    pytest.raises(RecordNotFound, product_store.get_by_id, "unique-id-1")


def test_should_raise_error_in_update_when_product_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    product_store = distributor.products()

    product = ProductRecord(id="unique-id-1", name="Product 1", price=9.99)

    pytest.raises(RecordNotFound, product_store.update, product)
