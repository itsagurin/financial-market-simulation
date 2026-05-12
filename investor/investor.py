"""Abstrakcyjny inwestor bazowy z typowymi zachowaniami handlowymi."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Investor(ABC):
    """Abstrakcyjny inwestor definiujący wspólny stan i zachowanie dla wszystkich strategii."""

    def __init__(self, name: str, capital: float, risk_tolerance: float) -> None:
        """Inicjalizuje bazowy stan inwestora.
        
        Args:
            name: Nazwa wyświetlana inwestora.
            capital: Dostępny kapitał gotówkowy.
            risk_tolerance: Relatywna tolerancja ryzyka w zakresie [0.0, 1.0].
            
        Raises:
            ValueError: Jeśli kapitał jest ujemny lub tolerancja ryzyka jest poza zakresem [0.0, 1.0].
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
        """Podejmuje decyzję i wykonuje akcję w bieżącej epoce.
        
        Args:
            market: Bieżący stan rynku.
            
        Returns:
            Ciąg opisujący akcję.
        """

    def buy(self, market, instrument, quantity: int) -> object:
        """Próbuje kupić jednostki instrumentu z płynności rynkowej.
        
        Args:
            market: Instancja rynku do wykonania.
            instrument: Instrument do kupienia.
            quantity: Liczba jednostek do kupienia.
            
        Returns:
            Rozliczony obiekt Transaction lub None w przypadku niepowodzenia.
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
        """Próbuje sprzedać jednostki instrumentu do płynności rynkowej.
        
        Args:
            market: Instancja rynku do wykonania.
            instrument: Instrument do sprzedania.
            quantity: Liczba jednostek do sprzedania.
            
        Returns:
            Rozliczony obiekt Transaction lub None w przypadku niepowodzenia.
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
        """Loguje akcję oczekiwania w bieżącej epoce."""
        self._action_history.append("WAIT")

    def notify_market_state(self, market, event) -> None:
        """Otrzymuje powiadomienie o zdarzeniu rynkowym.
        
        Args:
            market: Bieżący stan rynku.
            event: Zdarzenie występujące w bieżącej epoce.
        """
        _ = market
        self._action_history.append(f"EVENT {event.event_type}")

    def get_portfolio_value(self, market) -> float:
        """Oblicza wartość netto jako kapitał gotówkowy plus posiadane instrumenty.
        
        Args:
            market: Rynek użyty do uzyskania cen instrumentów.
            
        Returns:
            Całkowita wartość portfela.
        """
        total = self._capital
        for symbol, quantity in self._portfolio.items():
            instrument = market.get_instrument_by_symbol(symbol)
            if instrument is not None:
                total += quantity * instrument.price
        return total

    def add_to_portfolio(self, symbol: str, quantity: int) -> None:
        """Dodaje ilość symbolu do portfela.
        
        Args:
            symbol: Symbol instrumentu.
            quantity: Jednostki do dodania.
        """
        if quantity <= 0:
            return
        self._portfolio[symbol] = self._portfolio.get(symbol, 0) + quantity

    def remove_from_portfolio(self, symbol: str, quantity: int) -> None:
        """Usuwa ilość symbolu z portfela.
        
        Args:
            symbol: Symbol instrumentu.
            quantity: Jednostki do usunięcia.
            
        Raises:
            ValueError: Jeśli wynikowa ilość byłaby ujemna.
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
        """Zwraca posiadaną ilość symbolu."""
        return self._portfolio.get(symbol, 0)

    def is_bankrupt(self) -> bool:
        """Zwraca informację, czy inwestor nie ma już kapitału gotówkowego."""
        return self._capital <= 0.0

    @property
    def name(self) -> str:
        """Zwraca nazwę inwestora."""
        return self._name

    @property
    def capital(self) -> float:
        """Zwraca dostępny kapitał gotówkowy."""
        return self._capital

    @capital.setter
    def capital(self, value: float) -> None:
        """Ustawia dostępny kapitał po walidacji.
        
        Args:
            value: Nowa wartość kapitału.
            
        Raises:
            ValueError: Jeśli wartość jest ujemna.
        """
        if value < 0:
            raise ValueError(f"Capital cannot be negative, got {value}")
        self._capital = value

    @property
    def risk_tolerance(self) -> float:
        """Zwraca wartość tolerancji ryzyka."""
        return self._risk_tolerance

    @property
    def portfolio(self) -> dict:
        """Zwraca kopię bieżącego mapowania portfela."""
        return self._portfolio.copy()

    @property
    def action_history(self) -> list[str]:
        """Zwraca kopię zalogowanych akcji inwestora."""
        return self._action_history.copy()

    def __repr__(self) -> str:
        """Zwraca zwartą reprezentację tekstową inwestora."""
        return (
            f"Investor(name='{self._name}', capital={self._capital}, "
            f"risk_tolerance={self._risk_tolerance})"
        )
