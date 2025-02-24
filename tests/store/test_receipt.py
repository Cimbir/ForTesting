# import pytest
#
# from finalproject.store.distributor import StoreDistributor
# from finalproject.store.store import RecordNotFound
#
#
# def test_should_add_empty_receipt(distributor: StoreDistributor) -> None:
#     receipt = distributor.receipt().add(
#         ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1")
#     )
#
#     assert receipt == ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1")
#
#
# def test_should_add_receipt_with_items(distributor: StoreDistributor) -> None:
#     receipt = distributor.receipt().add(
#         ReceiptRecord(
#             id="1",
#             open=True,
#             items=[
#                 ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#                 ReceiptItemRecord(id="2", product_id="2", quantity=2, price=2.0),
#             ],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     assert receipt == ReceiptRecord(
#         id="1",
#         open=True,
#         items=[
#             ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#             ReceiptItemRecord(id="2", product_id="2", quantity=2, price=2.0),
#         ],
#         paid=0,
#         shift_id="1",
#     )
#
#
# def test_should_get_empty_receipt(distributor: StoreDistributor) -> None:
#     receipt = distributor.receipt().add(
#         ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1")
#     )
#
#     assert distributor.receipt().get_by_id("1") == receipt
#
#
# def test_should_get_receipt_with_items(distributor: StoreDistributor) -> None:
#     receipt = distributor.receipt().add(
#         ReceiptRecord(
#             id="1",
#             open=True,
#             items=[
#                 ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#                 ReceiptItemRecord(id="2", product_id="2", quantity=2, price=2.0),
#             ],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     assert distributor.receipt().get_by_id("1") == receipt
#
#
# def test_should_get_all_receipts(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     assert len(receipt_store.list_all()) == 0
#
#     receipt_1 = receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#     receipt_2 = receipt_store.add(
#         ReceiptRecord(
#             id="2",
#             open=True,
#             items=[
#                 ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#                 ReceiptItemRecord(id="2", product_id="2", quantity=2, price=2.0),
#             ],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     assert len(receipt_store.list_all()) == 2
#     assert receipt_1 in receipt_store.list_all()
#     assert receipt_2 in receipt_store.list_all()
#
#
# def test_should_raise_error_when_getting_non_existent_receipt(
#     distributor: StoreDistributor,
# ) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     pytest.raises(RecordNotFound, receipt_store.get_by_id, "2")
#
#
# def test_should_close_receipt(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     receipt_store.close_receipt_by_id("1", 10)
#
#     assert not receipt_store.get_by_id("1").open
#     assert receipt_store.get_by_id("1").paid == 10
#
#
# def test_should_raise_error_on_closing_non_existent_receipt(
#     distributor: StoreDistributor,
# ) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     pytest.raises(RecordNotFound, receipt_store.close_receipt_by_id, "2", 10)
#
#
# def test_should_add_item_to_receipt(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     receipt_store.add_item_to_receipt(
#         receipt_id="1",
#         item=ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#     )
#
#     assert receipt_store.get_by_id("1") == ReceiptRecord(
#         id="1",
#         open=True,
#         items=[ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0)],
#         paid=0,
#         shift_id="1",
#     )
#
#
# def test_should_raise_error_when_adding_item_to_non_existent_receipt(
#     distributor: StoreDistributor,
# ) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     pytest.raises(
#         RecordNotFound,
#         receipt_store.add_item_to_receipt,
#         "2",
#         ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#     )
#
#
# def test_should_update_item_in_receipt(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(
#         ReceiptRecord(
#             id="1",
#             open=True,
#             items=[ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0)],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     receipt_store.update_item_in_receipt(
#         receipt_id="1",
#         item=ReceiptItemRecord(id="1", product_id="1", quantity=2, price=1.0),
#     )
#
#     assert receipt_store.get_by_id("1") == ReceiptRecord(
#         id="1",
#         open=True,
#         items=[ReceiptItemRecord(id="1", product_id="1", quantity=2, price=1.0)],
#         paid=0,
#         shift_id="1",
#     )
#
#
# def test_should_raise_error_when_updating_non_existent_item(
#     distributor: StoreDistributor,
# ) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt = receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     pytest.raises(
#         RecordNotFound,
#         receipt_store.update_item_in_receipt,
#         receipt.id,
#         ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0),
#     )
#
#
# def test_should_remove_item_from_receipt(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(
#         ReceiptRecord(
#             id="1",
#             open=True,
#             items=[ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0)],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     receipt_store.remove_item_from_receipt(item_id="1")
#
#     assert receipt_store.get_by_id("1") == ReceiptRecord(
#         id="1",
#         open=True,
#         items=[],
#         paid=0,
#         shift_id="1",
#     )
#
#
# def test_should_raise_error_when_removing_non_existent_item(
#     distributor: StoreDistributor,
# ) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(ReceiptRecord(id="1", open=True, items=[], paid=0, shift_id="1"))
#
#     pytest.raises(
#         RecordNotFound,
#         receipt_store.remove_item_from_receipt,
#         "1",
#     )
#
# def test_should_get_receipts_by_shift_id(distributor: StoreDistributor) -> None:
#     receipt_store = distributor.receipt()
#
#     receipt_store.add(
#         ReceiptRecord(
#             id="1",
#             open=True,
#             items=[ReceiptItemRecord(id="1", product_id="1", quantity=1, price=1.0)],
#             paid=0,
#             shift_id="1",
#         )
#     )
#
#     assert len(receipt_store.get_by_shift_id("1")) == 1
#     assert len(receipt_store.get_by_shift_id("2")) == 0
#
#     receipt_store.add(
#         ReceiptRecord(
#             id="2",
#             open=True,
#             items=[ReceiptItemRecord(id="2", product_id="2", quantity=1, price=1.0)],
#             paid=0,
#             shift_id="2",
#         )
#     )
#
#     assert len(receipt_store.get_by_shift_id("1")) == 1
#     assert len(receipt_store.get_by_shift_id("2")) == 1
#     assert len(receipt_store.get_by_shift_id("3")) == 0
