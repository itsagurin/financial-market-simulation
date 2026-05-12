"""Abstract base investor with common trading behavior."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Investor(ABC):
    """Abstract investor defining common state and behavior for all strategies."""

    def __init__(self, name: str, capital: float, risk_tolerance: float) -> None:
        """Initializes base investor state.

        Args:
            name: Investor display name.
            capital: Available cash capital.
            risk_tolerance: Relative risk tolerance in range [0.0, 1.0].

        Raises:
            ValueError: If capital is negative or risk_tolerance is outside [0.0, 1.0].
        """
        if capital < 0:
            raise ValueError(f"Capital cannot be negative, got {capital}")
        if not 0.0 <= risk_tolerance <= 1.0:
            raise ValueError(
                f"Risk tolerance must be in range [0.0, 1.0], got {risk_tolerance}"
            )

        self._name: str = name
        self._capital: float = capital
        self._risk_tolerance: float = risk_tolerance
        self._portfolio: dict[str, int] = {}
        self._action_history: list[str] = []

    @abstractmethod
    def decide_action(self, market) -> str:
        """Decides and executes an action for the current epoch.

        Args:
            market: Current market state.

        Returns:
            Action description string.
        """

    def buy(self, market, instrument, quantity: int) -> object:
        """Attempts to buy instrument units from market liquidity.

        Args:
            market: Market instance for execution.
            instrument: Instrument to buy.
            quantity: Number of units to buy.

        Returns:
            Settled Transaction object, or None when unsuccessful.
        """
        if quantity <= 0:
            return None
        transaction = market.execute_transaction(
            buyer=self,
            seller=None,
            instrument=instrument,
            quantity=quantity,
            price=instrument.price,
        )
        if transaction is not None:
            self._action_history.append(f"BUY {instrument.symbol} x{quantity}")
        return transaction

    def sell(self, market, instrument, quantity: int) -> object:
        """Attempts to sell instrument units to market liquidity.

        Args:
            market: Market instance for execution.
            instrument: Instrument to sell.
            quantity: Number of units to sell.

        Returns:
            Settled Transaction object, or None when unsuccessful.
        """
        if quantity <= 0:
            return None
        if self.get_portfolio_quantity(instrument.symbol) < quantity:
            return None
        transaction = market.execute_transaction(
            buyer=None,
            seller=self,
            instrument=instrument,
            quantity=quantity,
            price=instrument.price,
        )
        if transaction is not None:
            self._action_history.append(f"SELL {instrument.symbol} x{quantity}")
        return transaction

    def wait_(self) -> None:
        """Logs a wait action for the current epoch."""
        self._action_history.append("WAIT")

    def notify_market_state(self, market, event) -> None:
        """Receives market event notification.

        Args:
            market: Current market state.
            event: Event occurring in the current epoch.
        """
        _ = market
        self._action_history.append(f"EVENT {event.event_type}")

    def get_portfolio_value(self, market) -> float:
        """Calculates net worth as cash capital plus instrument holdings.

        Args:
            market: Market used to obtain instrument prices.

        Returns:
            Total portfolio value.
        """
        total = self._capital
        for symbol, quantity in self._portfolio.items():
            instrument = market.get_instrument_by_symbol(symbol)
            if instrument is not None:
                total += quantity * instrument.price
        return total

    def add_to_portfolio(self, symbol: str, quantity: int) -> None:
        """Adds quantity of symbol to portfolio.

        Args:
            symbol: Instrument symbol.
            quantity: Units to add.
        """
        if quantity <= 0:
            return
        self._portfolio[symbol] = self._portfolio.get(symbol, 0) + quantity

    def remove_from_portfolio(self, symbol: str, quantity: int) -> None:
        """Removes quantity of symbol from portfolio.

        Args:
            symbol: Instrument symbol.
            quantity: Units to remove.

        Raises:
            ValueError: If resulting quantity would be negative.
        """
        if quantity <= 0:
            return
        current = self._portfolio.get(symbol, 0)
        new_value = current - quantity
        if new_value < 0:
            raise ValueError(
                f"Cannot remove {quantity} of {symbol}; current holding is {current}"
            )
        if new_value == 0:
            self._portfolio.pop(symbol, None)
            return
        self._portfolio[symbol] = new_value

    def get_portfolio_quantity(self, symbol: str) -> int:
        """Returns held quantity for symbol."""
        return self._portfolio.get(symbol, 0)

    def is_bankrupt(self) -> bool:
        """Returns whether investor has no remaining cash capital."""
        return self._capital <= 0.0

    @property
    def name(self) -> str:
        """Returns investor name."""
        return self._name

    @property
    def capital(self) -> float:
        """Returns available cash capital."""
        return self._capital

    @capital.setter
    def capital(self, value: float) -> None:
        """Sets available capital after validation.

        Args:
            value: New capital value.

        Raises:
            ValueError: If value is negative.
        """
        if value < 0:
            raise ValueError(f"Capital cannot be negative, got {value}")
        self._capital = value

    @property
    def risk_tolerance(self) -> float:
        """Returns risk tolerance value."""
        return self._risk_tolerance

    @property
    def portfolio(self) -> dict:
        """Returns a copy of the current portfolio mapping."""
        return self._portfolio.copy()

    @property
    def action_history(self) -> list[str]:
        """Returns a copy of logged investor actions."""
        return self._action_history.copy()

    def __repr__(self) -> str:
        """Returns a compact textual representation of investor."""
        return (
            f"Investor(name='{self._name}', capital={self._capital}, "
            f"risk_tolerance={self._risk_tolerance})"
        )
