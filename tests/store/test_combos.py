import pytest

from finalproject.store.combo import ComboRecord
from finalproject.store.distributor import StoreDistributor
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_should_add_and_get_combo(distributor: StoreDistributor) -> None:
    combo_store = distributor.combos()

    combo = ComboRecord(
        id="unique-id-1",
        name="Combo 1",
        discount=0.1,
    )
    combo_store.add(combo)

    assert combo_store.get_by_id("unique-id-1") == combo


def test_should_list_all_combos(distributor: StoreDistributor) -> None:
    combo_store = distributor.combos()

    combo1 = ComboRecord(
        id="unique-id-1",
        name="Combo 1",
        discount=0.1,
    )
    combo2 = ComboRecord(
        id="unique-id-2",
        name="Combo 2",
        discount=0.2,
    )

    combo_store.add(combo1)
    combo_store.add(combo2)

    all_combos = combo_store.list_all()
    assert combo1 in all_combos
    assert combo2 in all_combos
    assert len(all_combos) == 2


def test_should_remove_combo(distributor: StoreDistributor) -> None:
    combo_store = distributor.combos()

    combo = ComboRecord(
        id="unique-id-1",
        name="Combo 1",
        discount=0.1,
    )
    combo_store.add(combo)

    combo_store.remove("unique-id-1")

    pytest.raises(RecordNotFound, combo_store.get_by_id, "unique-id-1")


def test_should_raise_error_when_adding_combo_with_same_id(
    distributor: StoreDistributor,
) -> None:
    combo_store = distributor.combos()

    combo1 = ComboRecord(id="unique-id-1", name="Combo 1", discount=0.1)
    combo2 = ComboRecord(id="unique-id-1", name="Combo 2", discount=0.2)

    combo_store.add(combo1)
    pytest.raises(RecordAlreadyExists, combo_store.add, combo2)


def test_should_raise_error_in_get_when_combo_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    combo_store = distributor.combos()

    pytest.raises(RecordNotFound, combo_store.get_by_id, "unique-id-1")
