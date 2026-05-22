"""Abstrakcyjna klasa bazowa dla zdarzeń rynkowych."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Event(ABC):
    """Klasa bazowa dla wszystkich zdarzeń rynkowych."""

    def __init__(self, event_type: str, impact: float) -> None:
        """Inicjalizuje wspólne pola zdarzeń.
        
        Args:
            event_type: Identyfikator typu zdarzenia.
            impact: Relatywny wpływ zdarzenia.
        """
        self._event_type: str = event_type
        self._impact: float = impact

    @abstractmethod
    def apply(self, instrument) -> None:
        """Stosuje to zdarzenie do konkretnego instrumentu.
        
        Args:
            instrument: Docelowy instrument finansowy.
        """

    @property
    def event_type(self) -> str:
        """Zwraca etykietę typu zdarzenia."""
        return self._event_type

    @property
    def impact(self) -> float:
        """Zwraca wartość wpływu zdarzenia."""
        return self._impact

    def __repr__(self) -> str:
        """Zwraca zwartą reprezentację zdarzenia."""
        return f"Event(type='{self._event_type}', impact={self._impact})"
