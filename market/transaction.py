"""Transaction model describing a single trade operation."""

from __future__ import annotations

from market.financial_instrument import FinancialInstrument


class Transaction:
    """Represents one transaction between a buyer and a seller."""

    def __init__(
        self,
        buyer,
        seller,
        instrument: FinancialInstrument,
        quantity: int,
        price: float,
        epoch: int,
    ) -> None:
        """Initializes a transaction object.

        Args:
            buyer: Investor-like object that buys the instrument.
            seller: Investor-like object that sells the instrument or None.
            instrument: Financial instrument being traded.
            quantity: Number of units traded.
            price: Per-unit price used for settlement.
            epoch: Epoch index when transaction occurred.

        Raises:
            ValueError: If quantity is not positive or price is not positive.
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
        """Executes settlement by transferring capital and portfolio units.

        Returns:
            True if settlement succeeded, otherwise False.
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
            try:
                self.__seller.remove_from_portfolio(self.__instrument.symbol, self.__quantity)
            except ValueError:
                return False

        self.__settled = True
        return True

    def get_total_value(self) -> float:
        """Returns total transaction value: quantity multiplied by price."""
        return self.__quantity * self.__price

    @property
    def buyer(self):
        """Returns the buyer reference."""
        return self.__buyer

    @property
    def seller(self):
        """Returns the seller reference."""
        return self.__seller

    @property
    def instrument(self) -> FinancialInstrument:
        """Returns the traded instrument."""
        return self.__instrument

    @property
    def quantity(self) -> int:
        """Returns the traded quantity."""
        return self.__quantity

    @property
    def price(self) -> float:
        """Returns the per-unit transaction price."""
        return self.__price

    @property
    def epoch(self) -> int:
        """Returns the epoch when transaction occurred."""
        return self.__epoch

    @property
    def settled(self) -> bool:
        """Returns whether transaction was settled successfully."""
        return self.__settled

    def __repr__(self) -> str:
        """Returns a compact transaction representation."""
        buyer_name = getattr(self.__buyer, "name", "None")
        seller_name = getattr(self.__seller, "name", "None")
        return (
            "Transaction("
            f"buyer={buyer_name}, seller={seller_name}, "
            f"symbol={self.__instrument.symbol}, quantity={self.__quantity}, "
            f"price={self.__price:.2f}, epoch={self.__epoch}, settled={self.__settled}"
            ")"
        )
