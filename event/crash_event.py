"""Implementacja zdarzenia krachu rynkowego."""

from __future__ import annotations

import random

from event.event import Event
from market.financial_instrument import InstrumentType


class CrashEvent(Event):
    """Zdarzenie, które stosuje gwałtowny spadek na rynku."""

    def __init__(self) -> None:
        """Inicjalizuje losowe, gwałtowne negatywne zdarzenie krachu."""
        super().__init__("CRASH", -random.uniform(0.08, 0.20))

    def apply(self, instrument) -> None:
        """Stosuje intensywność krachu w zależności od typu instrumentu.
        
        Args:
            instrument: Instrument finansowy do zaktualizowania.
        """
        if instrument.instrument_type == InstrumentType.CRYPTOCURRENCY:
            factor = 2.0
        elif instrument.instrument_type == InstrumentType.BOND:
            factor = 0.3
        else:
            factor = 1.0
        instrument.update_price(self._impact * factor)
