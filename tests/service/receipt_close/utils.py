from finalproject.models.models import Receipt, ReceiptItem


def get_receipt(items: list[ReceiptItem]) -> Receipt:
    return Receipt(id="1", open=True, items=items, shift_id="1")
