from abc import abstractmethod
from typing import Protocol


class MidExchangeRateRetriever(Protocol):
    def get_mid_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Returns the mid exchange rate between two currencies.
        Returns 1 if from_currency == to_currency.
        Raises ConversionError if something went wrong.
        """
        pass


class BaseMidExchangeRateRetriever:
    def get_mid_rate(self, from_currency: str, to_currency: str) -> float:
        # We need to enforce this rule for every class that implements this protocol.
        if from_currency == to_currency:
            return 1
        return self._get_mid_rate_between_different_currencies(
            from_currency, to_currency
        )

    @abstractmethod
    def _get_mid_rate_between_different_currencies(
        self, from_currency: str, to_currency: str
    ) -> float:
        pass


class MockMidExchangeRateRetriever(BaseMidExchangeRateRetriever):
    def __init__(self) -> None:
        super().__init__()
        self._rates: dict[tuple[str, str], float] = {}

    def add_rate(self, from_currency: str, to_currency: str, rate: float) -> None:
        self._rates[(from_currency, to_currency)] = rate

    def _get_mid_rate_between_different_currencies(
        self, from_currency: str, to_currency: str
    ) -> float:
        return self._rates[(from_currency, to_currency)]


class CurrencyConversionService(Protocol):
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Converts amount from one currency to another.
        Raises ConversionError if something went wrong.
        """
        pass


class ConversionError(Exception):
    pass


class BaseCurrencyConversionService:
    def __init__(self, strategy: MidExchangeRateRetriever) -> None:
        self._exchange_rate_finder_strategy = strategy

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        return amount * self._exchange_rate_finder_strategy.get_mid_rate(
            from_currency, to_currency
        )
