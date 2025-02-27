import pytest

from finalproject.models.campaigns import ProductDiscount
from finalproject.service.campaigns.product_discounts import ProductDiscountService
from finalproject.service.exceptions import ProductNotFound, ProductDiscountNotFound
from finalproject.store.product import ProductRecord


def test_should_add_and_get_product_discount(product_discount_service: ProductDiscountService) -> None:
    product_discount_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    product_discount_response = product_discount_service.add_product_discount(product_discount)
    assert product_discount_response.compare_without_id(product_discount)
    assert product_discount_service.get_product_discount(
        product_discount_response.id
    ).compare_without_id(product_discount)


def test_should_get_all_product_discounts(product_discount_service: ProductDiscountService) -> None:
    assert len(product_discount_service.get_all_product_discounts()) == 0

    product_discount_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    product_discount_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    product_discount_1 = ProductDiscount(
        id="1",
        product_id="1",
        discount=10,
    )
    product_discount_2 = ProductDiscount(
        id="2",
        product_id="2",
        discount=10,
    )
    product_discount_service.add_product_discount(product_discount_1)
    product_discount_service.add_product_discount(product_discount_2)

    assert len(product_discount_service.get_all_product_discounts()) == 2
    assert product_discount_service.get_all_product_discounts()[0].compare_without_id(
        product_discount_1
    )
    assert product_discount_service.get_all_product_discounts()[1].compare_without_id(
        product_discount_2
    )


def test_should_not_add_product_discount_with_invalid_product_id(
    product_discount_service: ProductDiscountService,
) -> None:
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    pytest.raises(
        ProductNotFound, product_discount_service.add_product_discount, product_discount
    )


def test_should_raise_product_discount_not_found_when_getting_non_existent_discount(
    product_discount_service: ProductDiscountService,
) -> None:
    pytest.raises(ProductDiscountNotFound, product_discount_service.get_product_discount, "1")


def test_should_remove_product_discount(product_discount_service: ProductDiscountService) -> None:
    product_discount_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    product_discount_response = product_discount_service.add_product_discount(product_discount)
    product_discount_service.remove_product_discount(product_discount_response.id)
    pytest.raises(
        ProductDiscountNotFound,
        product_discount_service.get_product_discount,
        product_discount_response.id,
    )


def test_should_not_remove_non_existent_product_discount(
    product_discount_service: ProductDiscountService,
) -> None:
    pytest.raises(
        ProductDiscountNotFound, product_discount_service.remove_product_discount, "1"
    )