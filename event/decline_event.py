"""Decline event implementation."""

from __future__ import annotations

import random

from event.event import Event


class DeclineEvent(Event):
    """Event that moderately decreases market prices."""

    def __init__(self) -> None:
        """Initializes a random negative decline event."""
        super().__init__("DECLINE", -random.uniform(0.01, 0.05))

    def apply(self, instrument) -> None:
        """Applies decline effect to instrument.

        Args:
            instrument: Financial instrument to update.
        """
        instrument.update_price(self._impact * (1 + instrument.volatility * 0.3))
