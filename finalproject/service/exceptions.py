class ShiftNotFound(Exception):
    def __init__(self, shift_id: str) -> None:
        super().__init__(f"Shift with id {shift_id} not found")


class ReceiptAlreadyExists(Exception):
    def __init__(self, receipt_id: str) -> None:
        super().__init__(f"Receipt with id {receipt_id} already exists")


class ProductNotFound(Exception):
    def __init__(self, product_id: str) -> None:
        super().__init__(f"Product with id {product_id} not found")


class ReceiptNotFound(Exception):
    def __init__(self, receipt_id: str) -> None:
        super().__init__(f"Receipt with id {receipt_id} not found")


class ReceiptItemNotFound(Exception):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Receipt item with id {item_id} not found")


class ComboNotFound(Exception):
    def __init__(self, combo_id: str) -> None:
        super().__init__(f"Combo with id {combo_id} not found")


class ProductDiscountNotFound(Exception):
    def __init__(self, product_discount_id: str) -> None:
        super().__init__(f"Product discount with id {product_discount_id} not found")


class BuyNGetNNotFound(Exception):
    def __init__(self, buy_n_get_n_id: str) -> None:
        super().__init__(f"Buy N Get N with id {buy_n_get_n_id} not found")


class ReceiptDiscountNotFound(Exception):
    def __init__(self, receipt_discount_id: str) -> None:
        super().__init__(f"Receipt discount with id {receipt_discount_id} not found")
