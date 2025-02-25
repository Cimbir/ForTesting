from finalproject.models.campaigns import BuyNGetN
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.buy_n_get_n_decorator import BuyNGetNDecorator
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from tests.service.receipt_close.utils import get_receipt


def test_should_not_add_anything(def_rec_close: ReceiptClose) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=1,
            get_product_id="1",
            get_product_n=1,
        ),
    )

    receipt = get_receipt([])

    result = bngn.close(receipt)

    assert result.price == 0.0
    assert len(result.added_products) == 0


def test_should_add_free_product(def_rec_close: ReceiptClose) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=1,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt([ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)])

    result = bngn.close(receipt)

    assert result.price == 1.0
    assert result.added_products["2"] == 1


def test_should_not_add_free_product(def_rec_close: ReceiptClose) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt([ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)])

    result = bngn.close(receipt)

    assert result.price == 1.0
    assert result.added_products["2"] == 0


def test_should_add_free_items_with_other_items(
    def_rec_close: ReceiptClose,
) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt(
        [
            ReceiptItem(id="1", product_id="1", quantity=3, price=3.0),
            ReceiptItem(id="2", product_id="3", quantity=2, price=2.0),
        ]
    )

    result = bngn.close(receipt)

    assert result.price == 9.0 + 4.0
    assert result.added_products["2"] == 1


def test_should_add_free_product_multiple_times(
    def_rec_close: ReceiptClose,
) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt([ReceiptItem(id="1", product_id="1", quantity=5, price=5.0)])

    result = bngn.close(receipt)

    assert result.price == 5.0 * 5
    assert result.added_products["2"] == 2


def test_should_get_only_one_free_product(def_rec_close: ReceiptClose) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=4,
            get_product_id="2",
            get_product_n=1,
        ),
    )
    bngn = BuyNGetNDecorator(
        bngn,
        BuyNGetN(
            id="2",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt(
        [
            ReceiptItem(id="1", product_id="1", quantity=3, price=3.0),
            ReceiptItem(id="2", product_id="3", quantity=2, price=2.0),
        ]
    )

    result = bngn.close(receipt)

    assert result.price == 9.0 + 4.0
    assert result.added_products["2"] == 1


def test_should_get_multiple_free_products_from_multiple_sources(
    def_rec_close: ReceiptClose,
) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=4,
            get_product_id="2",
            get_product_n=1,
        ),
    )
    bngn = BuyNGetNDecorator(
        bngn,
        BuyNGetN(
            id="2",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )

    receipt = get_receipt(
        [
            ReceiptItem(id="1", product_id="1", quantity=4, price=3.0),
            ReceiptItem(id="2", product_id="2", quantity=2, price=2.0),
        ]
    )

    result = bngn.close(receipt)

    assert result.price == 12.0 + 4.0
    assert result.added_products["2"] == 2 + 1


def test_should_get_different_free_products(def_rec_close: ReceiptClose) -> None:
    bngn = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="2",
            get_product_n=1,
        ),
    )
    bngn = BuyNGetNDecorator(
        bngn,
        BuyNGetN(
            id="2",
            buy_product_id="1",
            buy_product_n=2,
            get_product_id="3",
            get_product_n=1,
        ),
    )

    receipt = get_receipt([ReceiptItem(id="1", product_id="1", quantity=2, price=4.0)])

    result = bngn.close(receipt)

    assert result.price == 4.0 * 2
    assert result.added_products["2"] == 1
    assert result.added_products["3"] == 1


def test_got_items_have_no_effect_on_price(def_rec_close: ReceiptClose) -> None:
    receipt = get_receipt([ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)])

    result = def_rec_close.close(receipt)

    assert result.price == 1.0
    assert len(result.added_products) == 0

    def_rec_close = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            id="1",
            buy_product_id="1",
            buy_product_n=1,
            get_product_id="1",
            get_product_n=1,
        ),
    )

    result = def_rec_close.close(receipt)

    assert result.price == 1.0
    assert len(result.added_products) == 1
    assert result.added_products["1"] == 1
