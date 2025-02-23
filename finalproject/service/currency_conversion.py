from typing import Protocol


class MidExchangeRateRetriever(Protocol):
    def get_mid_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Returns the mid exchange rate between two currencies.
        Returns 1 if from_currency == to_currency.
        Raises ConversionError if something went wrong.
        """
        pass


class CurrencyConversionService(Protocol):
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Converts amount from one currency to another.
        Raises ConversionError if something went wrong.
        """
        pass


class ConversionError(Exception):
    pass


class DefaultCurrencyConversionService:
    def __init__(self, strategy: MidExchangeRateRetriever) -> None:
        self._exchange_rate_finder_strategy = strategy

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        return amount * self._exchange_rate_finder_strategy.get_mid_rate(
            from_currency, to_currency
        )
