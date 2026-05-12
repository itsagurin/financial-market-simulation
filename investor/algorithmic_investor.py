"""Algorithmic investor strategy implementation."""

from __future__ import annotations

from investor.investor import Investor


class AlgorithmicInvestor(Investor):
    """Trend-following investor based on short price windows."""

    def __init__(self, name: str, capital: float) -> None:
        """Initializes algorithmic investor with medium risk tolerance.

        Args:
            name: Investor name.
            capital: Starting capital.
        """
        super().__init__(name, capital, risk_tolerance=0.5)
        self.__trend_window_size: int = 3

    def decide_action(self, market) -> str:
        """Decides action based on trend analysis.

        Args:
            market: The market instance.

        Returns:
            Action description string.
        """
        for instrument in market.instruments:
            trend = self.analyze_trend(instrument)
            if trend > 0.05 and self.capital >= instrument.price:
                if self.buy(market, instrument, 1) is not None:
                    return f"BUY {instrument.symbol} x1"
            elif trend < -0.05 and self.get_portfolio_quantity(instrument.symbol) > 0:
                if self.sell(market, instrument, 1) is not None:
                    return f"SELL {instrument.symbol} x1"

        self.wait_()
        return "WAIT"

    def analyze_trend(self, instrument) -> float:
        """Computes normalized trend using the latest price window.

        Args:
            instrument: Instrument to evaluate.

        Returns:
            Positive value for uptrend, negative for downtrend.
        """
        history = instrument.price_history
        if len(history) < 2:
            return 0.0

        window = history[-self.__trend_window_size :]
        if len(window) < 2:
            return 0.0

        first_price = window[0]
        last_price = window[-1]
        if first_price <= 0:
            return 0.0
        return (last_price - first_price) / first_price

    @property
    def trend_window_size(self) -> int:
        """Returns number of data points used in trend analysis."""
        return self.__trend_window_size

    @trend_window_size.setter
    def trend_window_size(self, value: int) -> None:
        """Sets trend window size.

        Args:
            value: Positive number of points to analyze.

        Raises:
            ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError(f"trend_window_size must be positive, got {value}")
        self.__trend_window_size = value
