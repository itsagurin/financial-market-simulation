"""Implementacja strategii konserwatywnego inwestora."""

from __future__ import annotations

from investor.investor import Investor
from market.financial_instrument import InstrumentType


class ConservativeInvestor(Investor):
    """Ostrożny inwestor preferujący zachowania niskiego ryzyka i wyczekiwanie."""

    def __init__(self, name: str, capital: float) -> None:
        """Inicjalizuje konserwatywnego inwestora z niską tolerancją ryzyka.
        
        Args:
            name: Nazwa inwestora.
            capital: Kapitał początkowy.
        """
        super().__init__(name, capital, risk_tolerance=0.2)

    def decide_action(self, market) -> str:
        """Podejmuje konserwatywną decyzję na podstawie nastrojów rynkowych.
        
        Args:
            market: Instancja rynku.
            
        Returns:
            Ciąg opisujący akcję.
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
        """Znajduje instrument obligacyjny o najniższej zmienności.
        
        Args:
            market: Instancja rynku.
            
        Returns:
            Instancja FinancialInstrument lub None.
        """
        bonds = [
            instrument
            for instrument in market.instruments
            if instrument.instrument_type == InstrumentType.BOND
        ]
        if not bonds:
            return None
        return min(bonds, key=lambda item: item.volatility)
