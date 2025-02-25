import pytest

from finalproject.models.campaigns import (
    BuyNGetN,
    Combo,
    ComboItem,
    ProductDiscount,
    ReceiptDiscount,
)
from finalproject.service.campaigns import CampaignService
from finalproject.service.exceptions import (
    BuyNGetNNotFound,
    ComboNotFound,
    ProductDiscountNotFound,
    ProductNotFound,
    ReceiptDiscountNotFound,
)
from finalproject.store.product import ProductRecord


def test_should_add_and_get_combo(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    combo_response = campaign_service.add_combo(combo)
    assert combo_response.compare_without_id_and_items_id(combo)
    assert campaign_service.get_combo(combo_response.id).compare_without_id(combo)


def test_should_get_all_combos(campaign_service: CampaignService) -> None:
    assert len(campaign_service.get_all_combos()) == 0

    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo_1 = Combo(
        id="1",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    combo_2 = Combo(
        id="2",
        name="Combo 2",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    campaign_service.add_combo(combo_1)
    campaign_service.add_combo(combo_2)

    assert len(campaign_service.get_all_combos()) == 2
    assert campaign_service.get_all_combos()[0].compare_without_id_and_items_id(combo_1)
    assert campaign_service.get_all_combos()[1].compare_without_id_and_items_id(combo_2)


def test_should_not_add_combo_with_invalid_product_id(
    campaign_service: CampaignService,
) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="3", quantity=2),
        ],
        discount=10,
    )
    pytest.raises(ProductNotFound, campaign_service.add_combo, combo)


def test_should_raise_combo_not_found_when_getting_non_existent_combo(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(ComboNotFound, campaign_service.get_combo, "1")


def test_should_remove_combo(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    combo_response = campaign_service.add_combo(combo)
    campaign_service.remove_combo(combo_response.id)
    pytest.raises(ComboNotFound, campaign_service.get_combo, combo_response.id)


def test_should_not_remove_non_existent_combo(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(ComboNotFound, campaign_service.remove_combo, "1")


def test_should_add_and_get_product_discount(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    product_discount_response = campaign_service.add_product_discount(product_discount)
    assert product_discount_response.compare_without_id(product_discount)
    assert campaign_service.get_product_discount(
        product_discount_response.id
    ).compare_without_id(product_discount)


def test_should_get_all_product_discounts(campaign_service: CampaignService) -> None:
    assert len(campaign_service.get_all_product_discounts()) == 0

    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
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
    campaign_service.add_product_discount(product_discount_1)
    campaign_service.add_product_discount(product_discount_2)

    assert len(campaign_service.get_all_product_discounts()) == 2
    assert campaign_service.get_all_product_discounts()[0].compare_without_id(
        product_discount_1
    )
    assert campaign_service.get_all_product_discounts()[1].compare_without_id(
        product_discount_2
    )


def test_should_not_add_product_discount_with_invalid_product_id(
    campaign_service: CampaignService,
) -> None:
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    pytest.raises(
        ProductNotFound, campaign_service.add_product_discount, product_discount
    )


def test_should_raise_product_discount_not_found_when_getting_non_existent_discount(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(ProductDiscountNotFound, campaign_service.get_product_discount, "1")


def test_should_remove_product_discount(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    product_discount = ProductDiscount(
        id="",
        product_id="1",
        discount=10,
    )
    product_discount_response = campaign_service.add_product_discount(product_discount)
    campaign_service.remove_product_discount(product_discount_response.id)
    pytest.raises(
        ProductDiscountNotFound,
        campaign_service.get_product_discount,
        product_discount_response.id,
    )


def test_should_not_remove_non_existent_product_discount(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(
        ProductDiscountNotFound, campaign_service.remove_product_discount, "1"
    )


def test_should_add_and_get_receipt_discount(campaign_service: CampaignService) -> None:
    receipt_discount = ReceiptDiscount(
        id="",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_response = campaign_service.add_receipt_discount(receipt_discount)
    assert receipt_discount_response.compare_without_id(receipt_discount)
    assert campaign_service.get_receipt_discount(
        receipt_discount_response.id
    ).compare_without_id(receipt_discount)


def test_should_get_all_receipt_discounts(campaign_service: CampaignService) -> None:
    assert len(campaign_service.get_all_receipt_discounts()) == 0

    receipt_discount_1 = ReceiptDiscount(
        id="1",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_2 = ReceiptDiscount(
        id="2",
        minimum_total=10,
        discount=10,
    )
    campaign_service.add_receipt_discount(receipt_discount_1)
    campaign_service.add_receipt_discount(receipt_discount_2)

    assert len(campaign_service.get_all_receipt_discounts()) == 2
    assert campaign_service.get_all_receipt_discounts()[0].compare_without_id(
        receipt_discount_1
    )
    assert campaign_service.get_all_receipt_discounts()[1].compare_without_id(
        receipt_discount_2
    )


def test_should_remove_receipt_discount(campaign_service: CampaignService) -> None:
    receipt_discount = ReceiptDiscount(
        id="",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_response = campaign_service.add_receipt_discount(receipt_discount)
    campaign_service.remove_receipt_discount(receipt_discount_response.id)
    pytest.raises(
        ReceiptDiscountNotFound,
        campaign_service.get_receipt_discount,
        receipt_discount_response.id,
    )


def test_should_not_remove_non_existent_receipt_discount(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(
        ReceiptDiscountNotFound, campaign_service.remove_receipt_discount, "1"
    )


def test_should_raise_receipt_discount_not_found_when_getting_non_existent_discount(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(ReceiptDiscountNotFound, campaign_service.get_receipt_discount, "1")


def test_should_add_and_get_buy_n_get_n(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_response = campaign_service.add_buy_n_get_n(buy_n_get_n)
    assert buy_n_get_n_response.compare_without_id(buy_n_get_n)
    assert campaign_service.get_buy_n_get_n(buy_n_get_n_response.id).compare_without_id(
        buy_n_get_n
    )


def test_should_get_all_buy_n_get_ns(campaign_service: CampaignService) -> None:
    assert len(campaign_service.get_all_buy_n_get_ns()) == 0

    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
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
    campaign_service.add_buy_n_get_n(buy_n_get_n_1)
    campaign_service.add_buy_n_get_n(buy_n_get_n_2)

    assert len(campaign_service.get_all_buy_n_get_ns()) == 2
    assert campaign_service.get_all_buy_n_get_ns()[0].compare_without_id(buy_n_get_n_1)
    assert campaign_service.get_all_buy_n_get_ns()[1].compare_without_id(buy_n_get_n_2)


def test_should_not_add_buy_n_get_n_with_invalid_product_id(
    campaign_service: CampaignService,
) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, campaign_service.add_buy_n_get_n, buy_n_get_n)


def test_should_raise_buy_n_get_n_not_found_when_getting_non_existent_buy_n_get_n(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(BuyNGetNNotFound, campaign_service.get_buy_n_get_n, "1")


def test_should_remove_buy_n_get_n(campaign_service: CampaignService) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    campaign_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    buy_n_get_n_response = campaign_service.add_buy_n_get_n(buy_n_get_n)
    campaign_service.remove_buy_n_get_n(buy_n_get_n_response.id)
    pytest.raises(
        BuyNGetNNotFound, campaign_service.get_buy_n_get_n, buy_n_get_n_response.id
    )


def test_should_not_remove_non_existent_buy_n_get_n(
    campaign_service: CampaignService,
) -> None:
    pytest.raises(BuyNGetNNotFound, campaign_service.remove_buy_n_get_n, "1")


def test_should_not_add_buy_n_get_n_with_invalid_get_product_id(
    campaign_service: CampaignService,
) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, campaign_service.add_buy_n_get_n, buy_n_get_n)


def test_should_not_add_buy_n_get_n_with_invalid_buy_product_id(
    campaign_service: CampaignService,
) -> None:
    campaign_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    buy_n_get_n = BuyNGetN(
        id="",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="2",
        get_product_n=1,
    )
    pytest.raises(ProductNotFound, campaign_service.add_buy_n_get_n, buy_n_get_n)
