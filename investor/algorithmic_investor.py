"""Implementacja strategii inwestora algorytmicznego."""

from __future__ import annotations

from investor.investor import Investor


class AlgorithmicInvestor(Investor):
    """Inwestor podążający za trendem opartym na krótkich oknach cenowych."""

    def __init__(self, name: str, capital: float) -> None:
        """Inicjalizuje inwestora algorytmicznego ze średnią tolerancją ryzyka.
        
        Args:
            name: Nazwa inwestora.
            capital: Kapitał początkowy.
        """
        super().__init__(name, capital, risk_tolerance=0.5)
        self.__trend_window_size: int = 3

    def decide_action(self, market) -> str:
        """Podejmuje decyzję na podstawie analizy trendu.
        
        Args:
            market: Instancja rynku.
            
        Returns:
            Ciąg opisujący akcję.
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
        """Oblicza znormalizowany trend przy użyciu najnowszego okna cenowego.
        
        Args:
            instrument: Instrument do oceny.
            
        Returns:
            Wartość dodatnia dla trendu wzrostowego, ujemna dla spadkowego.
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
        """Zwraca liczbę punktów danych używanych w analizie trendu."""
        return self.__trend_window_size

    @trend_window_size.setter
    def trend_window_size(self, value: int) -> None:
        """Ustawia rozmiar okna trendu.
        
        Args:
            value: Dodatnia liczba punktów do analizy.
            
        Raises:
            ValueError: Jeśli wartość nie jest dodatnia.
        """
        if value <= 0:
            raise ValueError(f"trend_window_size must be positive, got {value}")
        self.__trend_window_size = value
