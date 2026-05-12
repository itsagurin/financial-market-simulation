"""Model domenowy dla instrumentów finansowych będących przedmiotem obrotu rynkowego."""

from __future__ import annotations

from enum import Enum, auto


class InstrumentType(Enum):
    """Wyliczenie obsługiwanych kategorii instrumentów finansowych."""

    STOCK = auto()
    BOND = auto()
    CRYPTOCURRENCY = auto()


class FinancialInstrument:
    """Reprezentuje pojedynczy instrument finansowy z dynamiką cenową."""

    def __init__(
        self,
        symbol: str,
        name: str,
        initial_price: float,
        volatility: float,
        instrument_type: InstrumentType,
    ) -> None:
        """Inicjalizuje instrument finansowy.
        
        Args:
            symbol: Unikalny symbol instrumentu.
            name: Pełna nazwa instrumentu.
            initial_price: Początkowa cena rynkowa.
            volatility: Relatywna zmienność w zakresie [0.0, 1.0].
            instrument_type: Kategoria instrumentu.
            
        Raises:
            ValueError: Jeśli initial_price nie jest dodatnia lub zmienność jest poza zakresem [0.0, 1.0].
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
        """Aktualizuje cenę o relatywny współczynnik zmiany.
        
        Args:
            change_factor: Relatywna wartość zmiany, np. 0.05 oznacza +5%.
        """
        self.__price = max(0.01, self.__price * (1.0 + change_factor))
        self.__price_history.append(self.__price)

    def apply_shock(self, absolute_change: float) -> None:
        """Aktualizuje cenę o szok wartości bezwzględnej.
        
        Args:
            absolute_change: Bezwzględna różnica ceny, może być ujemna.
        """
        self.__price = max(0.01, self.__price + absolute_change)
        self.__price_history.append(self.__price)

    def get_price_change_percent(self) -> float:
        """Zwraca procentową zmianę w stosunku do ceny początkowej."""
        return ((self.__price - self.__initial_price) / self.__initial_price) * 100.0

    def get_average_price(self) -> float:
        """Zwraca średnią arytmetyczną wszystkich zarejestrowanych cen."""
        return sum(self.__price_history) / len(self.__price_history)

    @property
    def symbol(self) -> str:
        """Zwraca symbol instrumentu."""
        return self.__symbol

    @property
    def name(self) -> str:
        """Zwraca nazwę instrumentu."""
        return self.__name

    @property
    def price(self) -> float:
        """Zwraca bieżącą cenę instrumentu."""
        return self.__price

    @property
    def initial_price(self) -> float:
        """Zwraca początkową cenę instrumentu."""
        return self.__initial_price

    @property
    def volatility(self) -> float:
        """Zwraca skonfigurowaną zmienność."""
        return self.__volatility

    @property
    def instrument_type(self) -> InstrumentType:
        """Zwraca typ instrumentu."""
        return self.__type

    @property
    def price_history(self) -> list[float]:
        """Zwraca kopię pełnej historii cen."""
        return self.__price_history.copy()

    def __repr__(self) -> str:
        """Zwraca zwartą reprezentację tekstową instrumentu."""
        return (
            f"FinancialInstrument(symbol='{self.__symbol}', "
            f"price={self.__price:.2f}, type={self.__type.name})"
        )
