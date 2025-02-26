import uuid


def generate_id() -> str:
    return str(uuid.uuid4())


def check_correct_currency_name(currency_name: str) -> bool:
    return currency_name in ["USD", "EUR", "GEL"]
