"""Bubble event implementation."""

from __future__ import annotations

import random

from event.event import Event
from market.financial_instrument import InstrumentType


class BubbleEvent(Event):
    """Event that applies speculative growth by asset class."""

    def __init__(self) -> None:
        """Initializes a random strong positive bubble event."""
        super().__init__("BUBBLE", random.uniform(0.10, 0.25))

    def apply(self, instrument) -> None:
        """Applies bubble severity based on instrument type.

        Args:
            instrument: Financial instrument to update.
        """
        if instrument.instrument_type == InstrumentType.CRYPTOCURRENCY:
            factor = 3.0
        elif instrument.instrument_type == InstrumentType.BOND:
            factor = 0.1
        else:
            factor = 1.5
        instrument.update_price(self._impact * factor)
