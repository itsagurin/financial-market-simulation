"""Implementacja zdarzenia wzrostu."""

from __future__ import annotations

import random

from event.event import Event


class GrowthEvent(Event):
    """Zdarzenie, które podnosi ceny rynkowe z uwzględnieniem zmienności."""

    def __init__(self) -> None:
        """Inicjalizuje losowe, pozytywne zdarzenie wzrostu."""
        super().__init__("GROWTH", random.uniform(0.02, 0.08))

    def apply(self, instrument) -> None:
        """Stosuje efekt wzrostu na instrumencie.
        
        Args:
            instrument: Instrument finansowy do zaktualizowania.
        """
        instrument.update_price(self._impact * (1 + instrument.volatility * 0.5))
