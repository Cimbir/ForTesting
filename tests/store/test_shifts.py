import pytest

from finalproject.store.distributor import StoreDistributor
from finalproject.store.shift import ShiftRecord
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_should_add_and_get_shift(distributor: StoreDistributor) -> None:
    shift_store = distributor.shifts()

    shift = ShiftRecord(
        id="unique-id-1",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )
    shift_store.add(shift)

    assert shift_store.get_by_id("unique-id-1") == shift


def test_should_list_all_shifts(distributor: StoreDistributor) -> None:
    shift_store = distributor.shifts()

    assert len(shift_store.list_all()) == 0

    shift1 = ShiftRecord(
        id="unique-id-1",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )
    shift2 = ShiftRecord(
        id="unique-id-2",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )

    shift_store.add(shift1)
    shift_store.add(shift2)

    assert shift1 in shift_store.list_all()
    assert shift2 in shift_store.list_all()
    assert len(shift_store.list_all()) == 2


def test_should_update_shift(distributor: StoreDistributor) -> None:
    shift_store = distributor.shifts()

    shift = ShiftRecord(
        id="unique-id-1",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )
    shift_store.add(shift)

    updated_shift = ShiftRecord(
        id="unique-id-1",
        status="inactive",
        start_time="2021-01-01 00:00:00",
        end_time="2022-01-01 00:00:00",
    )
    shift_store.update(updated_shift)

    assert shift_store.get_by_id("unique-id-1") == updated_shift


def test_should_raise_error_when_adding_shift_with_same_id(
    distributor: StoreDistributor,
) -> None:
    shift_store = distributor.shifts()

    shift = ShiftRecord(
        id="unique-id-1",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )
    shift_store.add(shift)

    with pytest.raises(RecordAlreadyExists):
        shift_store.add(shift)


def test_should_raise_error_in_get_when_shift_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    shift_store = distributor.shifts()

    with pytest.raises(RecordNotFound):
        shift_store.get_by_id("unique-id-1")


def test_should_raise_error_in_update_when_shift_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    shift_store = distributor.shifts()

    shift = ShiftRecord(
        id="unique-id-1",
        status="active",
        start_time="2021-01-01 00:00:00",
        end_time="2021-01-01 00:00:00",
    )

    with pytest.raises(RecordNotFound):
        shift_store.update(shift)
