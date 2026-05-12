"""Implementacja zdarzenia spadku."""

from __future__ import annotations

import random

from event.event import Event


class DeclineEvent(Event):
    """Zdarzenie, które umiarkowanie obniża ceny rynkowe."""

    def __init__(self) -> None:
        """Inicjalizuje losowe, negatywne zdarzenie spadku."""
        super().__init__("DECLINE", -random.uniform(0.01, 0.05))

    def apply(self, instrument) -> None:
        """Stosuje efekt spadku na instrumencie.
        
        Args:
            instrument: Instrument finansowy do zaktualizowania.
        """
        instrument.update_price(self._impact * (1 + instrument.volatility * 0.3))
