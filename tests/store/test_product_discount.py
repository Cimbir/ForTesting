import pytest

from finalproject.store.distributor import StoreDistributor
from finalproject.store.product_discount import ProductDiscountRecord
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_add_and_get_product_discount(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()

    product_discount = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    product_discount_store.add(product_discount)

    assert product_discount_store.get_by_id("unique-id-1") == product_discount


def test_list_all_product_discount(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()

    assert len(product_discount_store.list_all()) == 0

    product_discount1 = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    product_discount2 = ProductDiscountRecord(
        id="unique-id-2",
        product_id="product-id",
        discount=0.1,
    )

    product_discount_store.add(product_discount1)
    product_discount_store.add(product_discount2)

    assert product_discount1 in product_discount_store.list_all()
    assert product_discount2 in product_discount_store.list_all()
    assert len(product_discount_store.list_all()) == 2


def test_remove_product_discount(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()

    product_discount1 = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    product_discount2 = ProductDiscountRecord(
        id="unique-id-2",
        product_id="product-id",
        discount=0.1,
    )

    product_discount_store.add(product_discount1)
    product_discount_store.add(product_discount2)

    product_discount_store.remove("unique-id-1")

    assert product_discount1 not in product_discount_store.list_all()
    assert product_discount2 in product_discount_store.list_all()
    assert len(product_discount_store.list_all()) == 1


def test_get_by_product_id_product_discount(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()

    product_discount1 = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    product_discount2 = ProductDiscountRecord(
        id="unique-id-2",
        product_id="product-id",
        discount=0.1,
    )

    product_discount_store.add(product_discount1)
    product_discount_store.add(product_discount2)

    assert product_discount_store.get_by_product_id("product-id") == [
        product_discount1,
        product_discount2,
    ]
    assert product_discount_store.get_by_product_id("product-id-2") == []


def test_add_when_id_already_exists(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()

    product_discount = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    product_discount_store.add(product_discount)

    product_discount = ProductDiscountRecord(
        id="unique-id-1",
        product_id="product-id",
        discount=0.1,
    )
    pytest.raises(RecordAlreadyExists, product_discount_store.add, product_discount)


def test_get_when_id_does_not_exist(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()
    pytest.raises(RecordNotFound, product_discount_store.get_by_id, "unique-id-1")


def test_remove_when_id_does_not_exist(distributor: StoreDistributor) -> None:
    product_discount_store = distributor.product_discount()
    pytest.raises(RecordNotFound, product_discount_store.remove, "unique-id-1")
