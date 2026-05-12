"""Simulation orchestration for the financial market project."""

from __future__ import annotations

import csv

from investor import AggressiveInvestor, AlgorithmicInvestor, ConservativeInvestor, Investor
from market import FinancialInstrument, InstrumentType, Market


class Simulation:
    """Controls simulation epochs, state history, and CSV result export."""

    def __init__(self, total_epochs: int = 20) -> None:
        """Initializes simulation with market, instruments, and investors.

        Args:
            total_epochs: Number of epochs to run.

        Raises:
            ValueError: If total_epochs is not positive.
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
        """Runs all epochs in sequence by calling step for each epoch."""
        print("=== Financial Market Simulation ===")
        print(f"Starting simulation with {self.__total_epochs} epochs...\n")

        for _ in range(self.__total_epochs):
            self.step()

        print("=== Simulation Complete ===")
        print(f"Total epochs: {self.__total_epochs}")
        print(f"Total transactions: {self.__market.get_total_transaction_count()}")

    def step(self) -> None:
        """Executes one simulation epoch and appends summary row to history."""
        next_epoch = self.__market.current_epoch + 1
        print(f"--- Epoch {next_epoch} ---")

        event = self.__market.simulate_epoch(self.__investors)
        print(f"Event: {event.event_type} (impact: {event.impact:+.2%})\n")

        aapl = self.__market.get_instrument_by_symbol("AAPL")
        obl = self.__market.get_instrument_by_symbol("OBL2028")
        btc = self.__market.get_instrument_by_symbol("BTC")

        self.__history.append(
            {
                "epoch": self.__market.current_epoch,
                "event_type": event.event_type,
                "event_impact": round(event.impact, 4),
                "total_transactions": self.__market.get_total_transaction_count(),
                "avg_price_AAPL": round(aapl.get_average_price(), 2) if aapl else 0.0,
                "avg_price_OBL2028": round(obl.get_average_price(), 2) if obl else 0.0,
                "avg_price_BTC": round(btc.get_average_price(), 2) if btc else 0.0,
                "capital_Anna": round(self.__investors[0].capital, 2),
                "capital_Bartek": round(self.__investors[1].capital, 2),
                "capital_Algo1": round(self.__investors[2].capital, 2),
            }
        )

    def export_csv(self, filename: str) -> None:
        """Exports simulation history rows to CSV.

        Args:
            filename: Output CSV file path.
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
        """Returns a copy of simulation history."""
        return [row.copy() for row in self.__history]

    @property
    def market(self) -> Market:
        """Returns the market instance used by the simulation."""
        return self.__market

    @property
    def investors(self) -> list[Investor]:
        """Returns a copy of the investor list."""
        return self.__investors.copy()
