"""Growth event implementation."""

from __future__ import annotations

import random

from event.event import Event


class GrowthEvent(Event):
    """Event that increases market prices with volatility sensitivity."""

    def __init__(self) -> None:
        """Initializes a random positive growth event."""
        super().__init__("GROWTH", random.uniform(0.02, 0.08))

    def apply(self, instrument) -> None:
        """Applies growth effect to instrument.

        Args:
            instrument: Financial instrument to update.
        """
        instrument.update_price(self._impact * (1 + instrument.volatility * 0.5))
