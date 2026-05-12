"""Moduł rynkowy, który koordynuje zdarzenia, instrumenty i transakcje."""

from __future__ import annotations

import random

from event import BubbleEvent, CrashEvent, DeclineEvent, GrowthEvent
from market.financial_instrument import FinancialInstrument
from market.transaction import Transaction


class _LiquidityProvider:
    """Prosta wewnętrzna strona przeciwna używana do rozliczania transakcji po stronie sprzedaży."""

    def __init__(self) -> None:
        """Inicjalizuje wewnętrzną stronę przeciwną z dużym kapitałem."""
        self.__capital = 10**15

    @property
    def capital(self) -> float:
        """Zwraca dostępny kapitał płynności."""
        return self.__capital

    @capital.setter
    def capital(self, value: float) -> None:
        """Aktualizuje dostępny kapitał płynności."""
        self.__capital = value

    @property
    def name(self) -> str:
        """Zwraca nazwę wyświetlaną strony przeciwnej."""
        return "Market"

    def add_to_portfolio(self, symbol: str, quantity: int) -> None:
        """Konsumuje zakupione jednostki bez śledzenia posiadanych zasobów."""
        _ = symbol
        _ = quantity

    def remove_from_portfolio(self, symbol: str, quantity: int) -> None:
        """Operacja pusta (no-op) usunięcia, aby spełnić interfejs transakcji."""
        _ = symbol
        _ = quantity


class Market:
    """Reprezentuje wspólny stan rynku dla wszystkich inwestorów."""

    def __init__(self) -> None:
        """Inicjalizuje pusty rynek."""
        self.__instruments: list[FinancialInstrument] = []
        self.__transaction_history: list[Transaction] = []
        self.__sentiment: float = 0.0
        self.__current_epoch: int = 0

    def add_instrument(self, instrument: FinancialInstrument) -> None:
        """Dodaje instrument finansowy do rynku.
        
        Args:
            instrument: Instancja instrumentu do zarejestrowania.
        """
        self.__instruments.append(instrument)

    def add_transaction(self, transaction: Transaction) -> None:
        """Dodaje rozliczoną transakcję do historii.
        
        Args:
            transaction: Transakcja do zarejestrowania.
        """
        self.__transaction_history.append(transaction)

    def simulate_epoch(self, investors: list) -> object:
        """Wykonuje pełną epokę symulacji.
        
        Args:
            investors: Inwestorzy uczestniczący w tej epoce.
            
        Returns:
            Wygenerowana instancja zdarzenia dla tej epoki.
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
        """Losowo generuje zdarzenie rynkowe na podstawie skonfigurowanych prawdopodobieństw.
        
        Returns:
            Instancja konkretnej podklasy Event.
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
        """Stosuje efekt zdarzenia do wszystkich instrumentów i aktualizuje nastroje.
        
        Args:
            event: Obiekt zdarzenia do zastosowania.
        """
        for instrument in self.__instruments:
            event.apply(instrument)
        self.__sentiment = max(-1.0, min(1.0, self.__sentiment + event.impact * 0.5))

    def execute_transaction(self, buyer, seller, instrument, quantity: int, price: float):
        """Tworzy, rozlicza i rejestruje transakcję.
        
        Args:
            buyer: Kupująca strona lub None.
            seller: Sprzedająca strona lub None.
            instrument: Handlowany instrument.
            quantity: Liczba jednostek.
            price: Cena za jednostkę.
            
        Returns:
            Instancja rozliczonej transakcji lub None, jeśli rozliczenie się nie powiedzie.
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
        """Znajduje instrument po symbolu.
        
        Args:
            symbol: Symbol instrumentu.
            
        Returns:
            Instancja FinancialInstrument lub None w przypadku braku.
        """
        for instrument in self.__instruments:
            if instrument.symbol == symbol:
                return instrument
        return None

    @property
    def instruments(self) -> list[FinancialInstrument]:
        """Zwraca kopię listy instrumentów."""
        return self.__instruments.copy()

    @property
    def transaction_history(self) -> list[Transaction]:
        """Zwraca kopię historii transakcji."""
        return self.__transaction_history.copy()

    @property
    def sentiment(self) -> float:
        """Zwraca bieżący nastrój rynkowy."""
        return self.__sentiment

    @sentiment.setter
    def sentiment(self, value: float) -> None:
        """Ustawia nastrój ograniczony do zakresu [-1.0, 1.0].
        
        Args:
            value: Nowa wartość nastroju.
        """
        self.__sentiment = max(-1.0, min(1.0, value))

    @property
    def current_epoch(self) -> int:
        """Zwraca numer bieżącej epoki."""
        return self.__current_epoch

    def get_total_transaction_count(self) -> int:
        """Zwraca całkowitą liczbę zarejestrowanych transakcji."""
        return len(self.__transaction_history)
