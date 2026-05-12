"""Abstract base class for market events."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Event(ABC):
    """Base class for all market events."""

    def __init__(self, event_type: str, impact: float) -> None:
        """Initializes common event fields.

        Args:
            event_type: Event type identifier.
            impact: Relative event impact.
        """
        self._event_type: str = event_type
        self._impact: float = impact

    @abstractmethod
    def apply(self, instrument) -> None:
        """Applies this event to a specific instrument.

        Args:
            instrument: Target financial instrument.
        """

    @property
    def event_type(self) -> str:
        """Returns event type label."""
        return self._event_type

    @property
    def impact(self) -> float:
        """Returns event impact value."""
        return self._impact

    def __repr__(self) -> str:
        """Returns compact event representation."""
        return f"Event(type='{self._event_type}', impact={self._impact})"
