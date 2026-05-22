"""Model transakcji opisujący pojedynczą operację handlową."""

from __future__ import annotations

from market.financial_instrument import FinancialInstrument


class Transaction:
    """Reprezentuje jedną transakcję między kupującym a sprzedającym."""

    def __init__(
        self,
        buyer,
        seller,
        instrument: FinancialInstrument,
        quantity: int,
        price: float,
        epoch: int,
    ) -> None:
        """Inicjalizuje obiekt transakcji.
        
        Args:
            buyer: Obiekt podobny do inwestora, który kupuje instrument.
            seller: Obiekt podobny do inwestora, który sprzedaje instrument lub None.
            instrument: Instrument finansowy będący przedmiotem obrotu.
            quantity: Liczba wymienionych jednostek.
            price: Cena za jednostkę użyta do rozliczenia.
            epoch: Indeks epoki, w której wystąpiła transakcja.
            
        Raises:
            ValueError: Jeśli ilość lub cena nie są dodatnie.
        """
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}")

        self.__buyer = buyer
        self.__seller = seller
        self.__instrument: FinancialInstrument = instrument
        self.__quantity: int = quantity
        self.__price: float = price
        self.__epoch: int = epoch
        self.__settled: bool = False

    def settle(self) -> bool:
        """Wykonuje rozliczenie poprzez transfer kapitału i jednostek portfela.
        
        Returns:
            True, jeśli rozliczenie powiodło się, w przeciwnym razie False.
        """
        total_value = self.get_total_value()
        if self.__buyer is None or self.__buyer.capital < total_value:
            return False
        if self.__seller is not None and hasattr(self.__seller, "get_portfolio_quantity"):
            if self.__seller.get_portfolio_quantity(self.__instrument.symbol) < self.__quantity:
                return False

        self.__buyer.capital = self.__buyer.capital - total_value
        if self.__seller is not None:
            self.__seller.capital = self.__seller.capital + total_value

        self.__buyer.add_to_portfolio(self.__instrument.symbol, self.__quantity)
        if self.__seller is not None:
            self.__seller.remove_from_portfolio(self.__instrument.symbol, self.__quantity)

        self.__settled = True
        return True

    def get_total_value(self) -> float:
        """Zwraca całkowitą wartość transakcji: ilość pomnożona przez cenę."""
        return self.__quantity * self.__price

    @property
    def buyer(self):
        """Zwraca odniesienie do kupującego."""
        return self.__buyer

    @property
    def seller(self):
        """Zwraca odniesienie do sprzedającego."""
        return self.__seller

    @property
    def instrument(self) -> FinancialInstrument:
        """Zwraca handlowany instrument."""
        return self.__instrument

    @property
    def quantity(self) -> int:
        """Zwraca wymienioną ilość."""
        return self.__quantity

    @property
    def price(self) -> float:
        """Zwraca cenę jednostkową transakcji."""
        return self.__price

    @property
    def epoch(self) -> int:
        """Zwraca epokę, w której wystąpiła transakcja."""
        return self.__epoch

    @property
    def settled(self) -> bool:
        """Zwraca informację, czy transakcja została pomyślnie rozliczona."""
        return self.__settled

    def __repr__(self) -> str:
        """Zwraca zwartą reprezentację transakcji."""
        buyer_name = getattr(self.__buyer, "name", "None")
        seller_name = getattr(self.__seller, "name", "None")
        return (
            "Transaction("
            f"buyer={buyer_name}, seller={seller_name}, "
            f"symbol={self.__instrument.symbol}, quantity={self.__quantity}, "
            f"price={self.__price:.2f}, epoch={self.__epoch}, settled={self.__settled}"
            ")"
        )
