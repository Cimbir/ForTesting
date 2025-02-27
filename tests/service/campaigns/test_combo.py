import pytest

from finalproject.models.campaigns import Combo, ComboItem
from finalproject.service.campaigns.combos import ComboService
from finalproject.service.exceptions import ComboNotFound, ProductNotFound
from finalproject.store.product import ProductRecord


def test_should_add_and_get_combo(combo_service: ComboService) -> None:
    combo_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    combo_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    combo_response = combo_service.add_combo(combo)
    assert combo_response.compare_without_id_and_items_id(combo)
    assert combo_service.get_combo(combo_response.id).compare_without_id(combo)


def test_should_get_all_combos(combo_service: ComboService) -> None:
    assert len(combo_service.get_all_combos()) == 0

    combo_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    combo_service.product_store.add(ProductRecord("2", "product 2", 2.0))
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
    combo_service.add_combo(combo_1)
    combo_service.add_combo(combo_2)

    assert len(combo_service.get_all_combos()) == 2
    assert combo_service.get_all_combos()[0].compare_without_id_and_items_id(combo_1)
    assert combo_service.get_all_combos()[1].compare_without_id_and_items_id(combo_2)


def test_should_not_add_combo_with_invalid_product_id(
    combo_service: ComboService,
) -> None:
    combo_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    combo_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="3", quantity=2),
        ],
        discount=10,
    )
    pytest.raises(ProductNotFound, combo_service.add_combo, combo)


def test_should_raise_combo_not_found_when_getting_non_existent_combo(
    combo_service: ComboService,
) -> None:
    pytest.raises(ComboNotFound, combo_service.get_combo, "1")


def test_should_remove_combo(combo_service: ComboService) -> None:
    combo_service.product_store.add(ProductRecord("1", "product 1", 1.0))
    combo_service.product_store.add(ProductRecord("2", "product 2", 2.0))
    combo = Combo(
        id="",
        name="Combo 1",
        items=[
            ComboItem(id="", product_id="1", quantity=1),
            ComboItem(id="", product_id="2", quantity=2),
        ],
        discount=10,
    )
    combo_response = combo_service.add_combo(combo)
    combo_service.remove_combo(combo_response.id)
    pytest.raises(ComboNotFound, combo_service.get_combo, combo_response.id)


def test_should_not_remove_non_existent_combo(
    combo_service: ComboService,
) -> None:
    pytest.raises(ComboNotFound, combo_service.remove_combo, "1")
