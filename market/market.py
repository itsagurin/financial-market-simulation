"""Market module that coordinates events, instruments, and transactions."""

from __future__ import annotations

import random

from event import BubbleEvent, CrashEvent, DeclineEvent, GrowthEvent
from market.financial_instrument import FinancialInstrument
from market.transaction import Transaction


class _LiquidityProvider:
    """Simple internal counterparty used for sell-side transaction settlement."""

    def __init__(self) -> None:
        """Initializes a large-capital internal counterparty."""
        self.__capital = 10**15

    @property
    def capital(self) -> float:
        """Returns available liquidity capital."""
        return self.__capital

    @capital.setter
    def capital(self, value: float) -> None:
        """Updates available liquidity capital."""
        self.__capital = value

    @property
    def name(self) -> str:
        """Returns counterparty display name."""
        return "Market"

    def add_to_portfolio(self, symbol: str, quantity: int) -> None:
        """Consumes purchased units without tracking holdings."""
        _ = symbol
        _ = quantity

    def remove_from_portfolio(self, symbol: str, quantity: int) -> None:
        """No-op removal to satisfy transaction interface."""
        _ = symbol
        _ = quantity


class Market:
    """Represents the shared market state for all investors."""

    def __init__(self) -> None:
        """Initializes an empty market."""
        self.__instruments: list[FinancialInstrument] = []
        self.__transaction_history: list[Transaction] = []
        self.__sentiment: float = 0.0
        self.__current_epoch: int = 0

    def add_instrument(self, instrument: FinancialInstrument) -> None:
        """Adds a financial instrument to the market.

        Args:
            instrument: Instrument instance to register.
        """
        self.__instruments.append(instrument)

    def add_transaction(self, transaction: Transaction) -> None:
        """Adds a settled transaction to history.

        Args:
            transaction: Transaction to record.
        """
        self.__transaction_history.append(transaction)

    def simulate_epoch(self, investors: list) -> object:
        """Executes a full simulation epoch.

        Args:
            investors: Investors participating in this epoch.

        Returns:
            The generated event instance for this epoch.
        """
        self.__current_epoch += 1
        event = self.generate_event()
        self.apply_event(event)

        for investor in investors:
            investor.notify_market_state(self, event)
            action = investor.decide_action(self)
            print(f"  {investor.name} -> {action}")

        return event

    def generate_event(self) -> object:
        """Randomly generates a market event based on configured probabilities.

        Returns:
            Instance of a specific Event subclass.
        """
        roll = random.random()
        if roll < 0.40:
            return GrowthEvent()
        if roll < 0.75:
            return DeclineEvent()
        if roll < 0.85:
            return CrashEvent()
        return BubbleEvent()

    def apply_event(self, event) -> None:
        """Applies event effect to all instruments and updates sentiment.

        Args:
            event: Event object to apply.
        """
        for instrument in self.__instruments:
            event.apply(instrument)
        self.__sentiment = max(-1.0, min(1.0, self.__sentiment + event.impact * 0.5))

    def execute_transaction(self, buyer, seller, instrument, quantity: int, price: float):
        """Creates, settles, and records a transaction.

        Args:
            buyer: Buying party or None.
            seller: Selling party or None.
            instrument: Traded instrument.
            quantity: Number of units.
            price: Price per unit.

        Returns:
            Settled Transaction instance or None if settlement fails.
        """
        buyer_party = buyer if buyer is not None else _LiquidityProvider()
        transaction = Transaction(
            buyer=buyer_party,
            seller=seller,
            instrument=instrument,
            quantity=quantity,
            price=price,
            epoch=self.__current_epoch,
        )
        if transaction.settle():
            self.add_transaction(transaction)
            return transaction
        return None

    def get_instrument_by_symbol(self, symbol: str):
        """Finds an instrument by symbol.

        Args:
            symbol: Instrument symbol.

        Returns:
            FinancialInstrument instance or None if absent.
        """
        for instrument in self.__instruments:
            if instrument.symbol == symbol:
                return instrument
        return None

    @property
    def instruments(self) -> list[FinancialInstrument]:
        """Returns a copy of the instrument list."""
        return self.__instruments.copy()

    @property
    def transaction_history(self) -> list[Transaction]:
        """Returns a copy of transaction history."""
        return self.__transaction_history.copy()

    @property
    def sentiment(self) -> float:
        """Returns current market sentiment."""
        return self.__sentiment

    @sentiment.setter
    def sentiment(self, value: float) -> None:
        """Sets sentiment clamped to the range [-1.0, 1.0].

        Args:
            value: New sentiment value.
        """
        self.__sentiment = max(-1.0, min(1.0, value))

    @property
    def current_epoch(self) -> int:
        """Returns the current epoch number."""
        return self.__current_epoch

    def get_total_transaction_count(self) -> int:
        """Returns total number of recorded transactions."""
        return len(self.__transaction_history)
