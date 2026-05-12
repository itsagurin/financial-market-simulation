"""Aggressive investor strategy implementation."""

from __future__ import annotations

import random

from investor.investor import Investor


class AggressiveInvestor(Investor):
    """Risk-seeking investor with frequent randomized trading."""

    def __init__(self, name: str, capital: float) -> None:
        """Initializes aggressive investor with high risk tolerance.

        Args:
            name: Investor name.
            capital: Starting capital.
        """
        super().__init__(name, capital, risk_tolerance=0.8)

    def decide_action(self, market) -> str:
        """Makes a random aggressive decision.

        Args:
            market: The market instance.

        Returns:
            Action description string.
        """
        roll = random.random()

        if roll < 0.5:
            instrument = self.__get_random_instrument(market)
            if instrument is not None and self.capital >= instrument.price:
                if self.buy(market, instrument, 1) is not None:
                    return f"BUY {instrument.symbol} x1"

        elif roll < 0.8:
            held_symbols = [symbol for symbol, qty in self.portfolio.items() if qty > 0]
            if held_symbols:
                symbol = random.choice(held_symbols)
                instrument = market.get_instrument_by_symbol(symbol)
                if instrument is not None:
                    if self.sell(market, instrument, 1) is not None:
                        return f"SELL {instrument.symbol} x1"

        self.wait_()
        return "WAIT"

    def __get_random_instrument(self, market) -> object:
        """Returns a random instrument from the market.

        Args:
            market: The market instance.

        Returns:
            Random FinancialInstrument or None.
        """
        if not market.instruments:
            return None
        return random.choice(market.instruments)
