"""Implementacja zdarzenia bańki spekulacyjnej."""

from __future__ import annotations

import random

from event.event import Event
from market.financial_instrument import InstrumentType


class BubbleEvent(Event):
    """Zdarzenie, które stosuje spekulacyjny wzrost według klasy aktywów."""

    def __init__(self) -> None:
        """Inicjalizuje losowe, silnie pozytywne zdarzenie bańki."""
        super().__init__("BUBBLE", random.uniform(0.10, 0.25))

    def apply(self, instrument) -> None:
        """Stosuje intensywność bańki w zależności od typu instrumentu.
        
        Args:
            instrument: Instrument finansowy do zaktualizowania.
        """
        if instrument.instrument_type == InstrumentType.CRYPTOCURRENCY:
            factor = 3.0
        elif instrument.instrument_type == InstrumentType.BOND:
            factor = 0.1
        else:
            factor = 1.5
        instrument.update_price(self._impact * factor)
