import pytest

from finalproject.models.campaigns import BuyNGetN
from finalproject.service.campaigns.buy_n_get_n import BuyNGetNService
from finalproject.service.exceptions import BuyNGetNNotFound, ProductNotFound
from finalproject.store.product import ProductRecord


def test_should_add_and_get_buy_n_get_n(buy_n_get_n_service: BuyNGetNService) -> None:
    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_response = buy_n_get_n_service.add_buy_n_get_n(buy_n_get_n)
    assert buy_n_get_n_response.compare_without_id(buy_n_get_n)
    assert buy_n_get_n_service.get_buy_n_get_n(buy_n_get_n_response.id).compare_without_id(
        buy_n_get_n
    )


def test_should_get_all_buy_n_get_ns(buy_n_get_n_service: BuyNGetNService) -> None:
    assert len(buy_n_get_n_service.get_all_buy_n_get_ns()) == 0

    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    buy_n_get_n_1 = BuyNGetN(
        id="1",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_2 = BuyNGetN(
        id="2",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_service.add_buy_n_get_n(buy_n_get_n_1)
    buy_n_get_n_service.add_buy_n_get_n(buy_n_get_n_2)

    assert len(buy_n_get_n_service.get_all_buy_n_get_ns()) == 2
    assert buy_n_get_n_service.get_all_buy_n_get_ns()[0].compare_without_id(buy_n_get_n_1)
    assert buy_n_get_n_service.get_all_buy_n_get_ns()[1].compare_without_id(buy_n_get_n_2)


def test_should_not_add_buy_n_get_n_with_invalid_product_id(
        buy_n_get_n_service: BuyNGetNService,
) -> None:
    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, buy_n_get_n_service.add_buy_n_get_n, buy_n_get_n)


def test_should_raise_buy_n_get_n_not_found_when_getting_non_existent_buy_n_get_n(
        buy_n_get_n_service: BuyNGetNService,
) -> None:
    pytest.raises(BuyNGetNNotFound, buy_n_get_n_service.get_buy_n_get_n, "1")


def test_should_remove_buy_n_get_n(buy_n_get_n_service: BuyNGetNService) -> None:
    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_response = buy_n_get_n_service.add_buy_n_get_n(buy_n_get_n)
    buy_n_get_n_service.remove_buy_n_get_n(buy_n_get_n_response.id)
    pytest.raises(
        BuyNGetNNotFound, buy_n_get_n_service.get_buy_n_get_n, buy_n_get_n_response.id
    )


def test_should_not_remove_non_existent_buy_n_get_n(
        buy_n_get_n_service: BuyNGetNService,
) -> None:
    pytest.raises(BuyNGetNNotFound, buy_n_get_n_service.remove_buy_n_get_n, "1")


def test_should_not_add_buy_n_get_n_with_invalid_get_product_id(
        buy_n_get_n_service: BuyNGetNService,
) -> None:
    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, buy_n_get_n_service.add_buy_n_get_n, buy_n_get_n)


def test_should_not_add_buy_n_get_n_with_invalid_buy_product_id(
        buy_n_get_n_service: BuyNGetNService,
) -> None:
    buy_n_get_n_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, buy_n_get_n_service.add_buy_n_get_n, buy_n_get_n)
