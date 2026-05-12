"""Conservative investor strategy implementation."""

from __future__ import annotations

from investor.investor import Investor
from market.financial_instrument import InstrumentType


class ConservativeInvestor(Investor):
    """Cautious investor preferring low-risk behavior and waiting."""

    def __init__(self, name: str, capital: float) -> None:
        """Initializes conservative investor with low risk tolerance.

        Args:
            name: Investor name.
            capital: Starting capital.
        """
        super().__init__(name, capital, risk_tolerance=0.2)

    def decide_action(self, market) -> str:
        """Makes a conservative decision based on market sentiment.

        Args:
            market: The market instance.

        Returns:
            Action description string.
        """
        if market.sentiment > 0.3:
            instrument = self.__find_safest_instrument(market)
            if instrument is not None and self.capital >= instrument.price:
                if self.buy(market, instrument, 1) is not None:
                    return f"BUY {instrument.symbol} x1"

        if market.sentiment < -0.5:
            for instrument in market.instruments:
                if instrument.instrument_type in (InstrumentType.STOCK, InstrumentType.CRYPTOCURRENCY):
                    if self.get_portfolio_quantity(instrument.symbol) > 0:
                        if self.sell(market, instrument, 1) is not None:
                            return f"SELL {instrument.symbol} x1"

        self.wait_()
        return "WAIT"

    def __find_safest_instrument(self, market) -> object:
        """Finds the lowest-volatility bond instrument.

        Args:
            market: The market instance.

        Returns:
            FinancialInstrument instance or None.
        """
        bonds = [
            instrument
            for instrument in market.instruments
            if instrument.instrument_type == InstrumentType.BOND
        ]
        if not bonds:
            return None
        return min(bonds, key=lambda item: item.volatility)
