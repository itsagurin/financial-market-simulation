"""Orkiestracja symulacji dla projektu rynku finansowego."""

from __future__ import annotations

import csv

from investor import AggressiveInvestor, AlgorithmicInvestor, ConservativeInvestor, Investor
from market import FinancialInstrument, InstrumentType, Market


class Simulation:
    """Kontroluje epoki symulacji, historię stanów i eksport wyników do CSV."""

    def __init__(self, total_epochs: int = 20) -> None:
        """Inicjalizuje symulację z rynkiem, instrumentami i inwestorami.
        
        Args:
            total_epochs: Liczba epok do uruchomienia.
            
        Raises:
            ValueError: Jeśli total_epochs nie jest dodatnie.
        """
        if total_epochs <= 0:
            raise ValueError(f"total_epochs must be positive, got {total_epochs}")

        self.__market: Market = Market()
        self.__investors: list[Investor] = []
        self.__history: list[dict] = []
        self.__total_epochs: int = total_epochs

        self.__market.add_instrument(
            FinancialInstrument("AAPL", "Apple Inc.", 187.20, 0.15, InstrumentType.STOCK)
        )
        self.__market.add_instrument(
            FinancialInstrument("OBL2028", "Polish Bond 2028", 102.50, 0.03, InstrumentType.BOND)
        )
        self.__market.add_instrument(
            FinancialInstrument(
                "BTC",
                "Bitcoin",
                421000.00,
                0.45,
                InstrumentType.CRYPTOCURRENCY,
            )
        )

        self.__investors.append(ConservativeInvestor("Anna", 15000.0))
        self.__investors.append(AggressiveInvestor("Bartek", 32000.0))
        self.__investors.append(AlgorithmicInvestor("Algo1", 50000.0))

    def run(self) -> None:
        """Uruchamia wszystkie epoki w sekwencji, wywołując step dla każdej epoki."""
        print("=== Financial Market Simulation ===")
        print(f"Starting simulation with {self.__total_epochs} epochs...\n")

        for _ in range(self.__total_epochs):
            self.step()

        print("=== Simulation Complete ===")
        print(f"Total epochs: {self.__total_epochs}")
        print(f"Total transactions: {self.__market.get_total_transaction_count()}")

    def step(self) -> None:
        """Wykonuje jedną epokę symulacji i dołącza wiersz podsumowania do historii."""
        next_epoch = self.__market.current_epoch + 1
        print(f"--- Epoch {next_epoch} ---")

        event = self.__market.simulate_epoch(self.__investors)
        print(f"Event: {event.event_type} (impact: {event.impact:+.2%})\n")

        aapl = self.__market.get_instrument_by_symbol("AAPL")
        obl = self.__market.get_instrument_by_symbol("OBL2028")
        btc = self.__market.get_instrument_by_symbol("BTC")
        investor_capitals = {investor.name: investor.capital for investor in self.__investors}

        self.__history.append(
            {
                "epoch": self.__market.current_epoch,
                "event_type": event.event_type,
                "event_impact": round(event.impact, 4),
                "total_transactions": self.__market.get_total_transaction_count(),
                "avg_price_AAPL": round(aapl.get_average_price(), 2) if aapl else 0.0,
                "avg_price_OBL2028": round(obl.get_average_price(), 2) if obl else 0.0,
                "avg_price_BTC": round(btc.get_average_price(), 2) if btc else 0.0,
                "capital_Anna": round(investor_capitals.get("Anna", 0.0), 2),
                "capital_Bartek": round(investor_capitals.get("Bartek", 0.0), 2),
                "capital_Algo1": round(investor_capitals.get("Algo1", 0.0), 2),
            }
        )

    def export_csv(self, filename: str) -> None:
        """Eksportuje wiersze historii symulacji do pliku CSV.
        
        Args:
            filename: Ścieżka do wyjściowego pliku CSV.
        """
        fieldnames = [
            "epoch",
            "event_type",
            "event_impact",
            "total_transactions",
            "avg_price_AAPL",
            "avg_price_OBL2028",
            "avg_price_BTC",
            "capital_Anna",
            "capital_Bartek",
            "capital_Algo1",
        ]
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.__history:
                writer.writerow(row)
        print(f"Results exported to: {filename}")

    @property
    def history(self) -> list[dict]:
        """Zwraca kopię historii symulacji."""
        return [row.copy() for row in self.__history]

    @property
    def market(self) -> Market:
        """Zwraca instancję rynku używaną przez symulację."""
        return self.__market

    @property
    def investors(self) -> list[Investor]:
        """Zwraca kopię listy inwestorów."""
        return self.__investors.copy()
