"""Crash event implementation."""

from __future__ import annotations

import random

from event.event import Event
from market.financial_instrument import InstrumentType


class CrashEvent(Event):
    """Event that applies a severe market downturn."""

    def __init__(self) -> None:
        """Initializes a random severe negative crash event."""
        super().__init__("CRASH", -random.uniform(0.08, 0.20))

    def apply(self, instrument) -> None:
        """Applies crash severity based on instrument type.

        Args:
            instrument: Financial instrument to update.
        """
        if instrument.instrument_type == InstrumentType.CRYPTOCURRENCY:
            factor = 2.0
        elif instrument.instrument_type == InstrumentType.BOND:
            factor = 0.3
        else:
            factor = 1.0
        instrument.update_price(self._impact * factor)
