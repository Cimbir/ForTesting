import pytest

from finalproject.store.buy_n_get_n import BuyNGetNRecord
from finalproject.store.distributor import StoreDistributor
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_should_add_and_get_buy_get(distributor: StoreDistributor) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()

    buy_n_get_n = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )
    buy_n_get_n_store.add(buy_n_get_n)

    assert buy_n_get_n_store.get_by_id("unique-id-1") == buy_n_get_n


def test_should_list_all_buy_get(distributor: StoreDistributor) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()

    assert len(buy_n_get_n_store.list_all()) == 0

    buy_n_get_n1 = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )
    buy_n_get_n2 = BuyNGetNRecord(
        id="unique-id-2",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )

    buy_n_get_n_store.add(buy_n_get_n1)
    buy_n_get_n_store.add(buy_n_get_n2)

    assert buy_n_get_n1 in buy_n_get_n_store.list_all()
    assert buy_n_get_n2 in buy_n_get_n_store.list_all()
    assert len(buy_n_get_n_store.list_all()) == 2


def test_should_remove_buy_get_and_leave_others_untouched(
    distributor: StoreDistributor,
) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()

    buy_n_get_n1 = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )
    buy_n_get_n2 = BuyNGetNRecord(
        id="unique-id-2",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )

    buy_n_get_n_store.add(buy_n_get_n1)
    buy_n_get_n_store.add(buy_n_get_n2)

    assert buy_n_get_n1 in buy_n_get_n_store.list_all()
    assert buy_n_get_n2 in buy_n_get_n_store.list_all()

    buy_n_get_n_store.remove("unique-id-1")

    assert buy_n_get_n_store.list_all() == [buy_n_get_n2]
    assert buy_n_get_n_store.get_by_id("unique-id-2") == buy_n_get_n2


def test_should_raise_error_when_adding_buy_get_with_same_id(
    distributor: StoreDistributor,
) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()

    buy_n_get_n1 = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )
    buy_n_get_n2 = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="buy-product-id",
        buy_product_n=1,
        get_product_id="get-product-id",
        get_product_n=1,
    )

    buy_n_get_n_store.add(buy_n_get_n1)
    pytest.raises(RecordAlreadyExists, buy_n_get_n_store.add, buy_n_get_n2)


def test_should_raise_error_in_get_when_buy_get_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()
    pytest.raises(RecordNotFound, buy_n_get_n_store.get_by_id, "unique-id-1")


def test_should_raise_error_in_remove_when_buy_get_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()
    pytest.raises(RecordNotFound, buy_n_get_n_store.remove, "unique-id-1")


def test_should_get_buy_get_by_product_id(distributor: StoreDistributor) -> None:
    buy_n_get_n_store = distributor.buy_n_get_n()

    buy_n_get_n1 = BuyNGetNRecord(
        id="unique-id-1",
        buy_product_id="a-product-id",
        buy_product_n=1,
        get_product_id="b-product-id",
        get_product_n=1,
    )
    buy_n_get_n2 = BuyNGetNRecord(
        id="unique-id-2",
        buy_product_id="a-product-id",
        buy_product_n=1,
        get_product_id="a-product-id",
        get_product_n=1,
    )
    buy_n_get_n3 = BuyNGetNRecord(
        id="unique-id-3",
        buy_product_id="b-product-id",
        buy_product_n=1,
        get_product_id="a-product-id",
        get_product_n=1,
    )

    buy_n_get_n_store.add(buy_n_get_n1)
    buy_n_get_n_store.add(buy_n_get_n2)
    buy_n_get_n_store.add(buy_n_get_n3)

    assert buy_n_get_n_store.get_by_product_id("a-product-id") == [
        buy_n_get_n1,
        buy_n_get_n2,
    ]
    assert buy_n_get_n_store.get_by_product_id("b-product-id") == [buy_n_get_n3]
    assert buy_n_get_n_store.get_by_product_id("non-existent-product-id") == []
