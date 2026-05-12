"""Domain model for financial instruments traded on the market."""

from __future__ import annotations

from enum import Enum, auto


class InstrumentType(Enum):
    """Enumeration of supported financial instrument categories."""

    STOCK = auto()
    BOND = auto()
    CRYPTOCURRENCY = auto()


class FinancialInstrument:
    """Represents a single financial instrument with price dynamics."""

    def __init__(
        self,
        symbol: str,
        name: str,
        initial_price: float,
        volatility: float,
        instrument_type: InstrumentType,
    ) -> None:
        """Initializes a financial instrument.

        Args:
            symbol: Unique instrument symbol.
            name: Full instrument name.
            initial_price: Starting market price.
            volatility: Relative volatility in the range [0.0, 1.0].
            instrument_type: Category of the instrument.

        Raises:
            ValueError: If initial_price is not positive or volatility is outside [0.0, 1.0].
        """
        if initial_price <= 0:
            raise ValueError(f"Initial price must be positive, got {initial_price}")
        if not 0.0 <= volatility <= 1.0:
            raise ValueError(f"Volatility must be in range [0.0, 1.0], got {volatility}")

        self.__symbol: str = symbol
        self.__name: str = name
        self.__price: float = initial_price
        self.__initial_price: float = initial_price
        self.__volatility: float = volatility
        self.__type: InstrumentType = instrument_type
        self.__price_history: list[float] = [initial_price]

    def update_price(self, change_factor: float) -> None:
        """Updates price by a relative change factor.

        Args:
            change_factor: Relative change value, e.g. 0.05 means +5%.
        """
        self.__price = max(0.01, self.__price * (1.0 + change_factor))
        self.__price_history.append(self.__price)

    def apply_shock(self, absolute_change: float) -> None:
        """Updates price by an absolute value shock.

        Args:
            absolute_change: Absolute price delta, can be negative.
        """
        self.__price = max(0.01, self.__price + absolute_change)
        self.__price_history.append(self.__price)

    def get_price_change_percent(self) -> float:
        """Returns percentage change from initial price."""
        return ((self.__price - self.__initial_price) / self.__initial_price) * 100.0

    def get_average_price(self) -> float:
        """Returns the arithmetic average of all recorded prices."""
        return sum(self.__price_history) / len(self.__price_history)

    @property
    def symbol(self) -> str:
        """Returns the instrument symbol."""
        return self.__symbol

    @property
    def name(self) -> str:
        """Returns the instrument name."""
        return self.__name

    @property
    def price(self) -> float:
        """Returns the current instrument price."""
        return self.__price

    @property
    def initial_price(self) -> float:
        """Returns the initial instrument price."""
        return self.__initial_price

    @property
    def volatility(self) -> float:
        """Returns the configured volatility."""
        return self.__volatility

    @property
    def instrument_type(self) -> InstrumentType:
        """Returns the instrument type."""
        return self.__type

    @property
    def price_history(self) -> list[float]:
        """Returns a copy of the full price history."""
        return self.__price_history.copy()

    def __repr__(self) -> str:
        """Returns a compact text representation of the instrument."""
        return (
            f"FinancialInstrument(symbol='{self.__symbol}', "
            f"price={self.__price:.2f}, type={self.__type.name})"
        )
