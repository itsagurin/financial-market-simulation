"""Testy jednostkowe dla klasy Simulation."""

import csv
import os
import unittest
from simulation import Simulation


class TestSimulation(unittest.TestCase):
    """Zestaw testów dla orkiestracji symulacji rynku."""

    def setUp(self) -> None:
        """Inicjalizacja nowej symulacji przed każdym testem."""
        self.simulation = Simulation(total_epochs=5)
        self.temp_csv = "temp_test_results.csv"

    def tearDown(self) -> None:
        """Czyszczenie tymczasowych plików po testach."""
        if os.path.exists(self.temp_csv):
            try:
                os.remove(self.temp_csv)
            except OSError:
                pass

    def test_simulation_initialization(self) -> None:
        """Testuje poprawną konfigurację początkową symulacji."""
        self.assertEqual(len(self.simulation.investors), 3)
        self.assertEqual(len(self.simulation.market.instruments), 3)
        
        # Sprawdzamy czy poprawnie wczytano określonych inwestorów
        names = [inv.name for inv in self.simulation.investors]
        self.assertIn("Anna", names)
        self.assertIn("Bartek", names)
        self.assertIn("Algo1", names)

    def test_simulation_step_updates_history(self) -> None:
        """Testuje pojedynczy krok symulacji (step) i poprawność logowania historii."""
        self.assertEqual(len(self.simulation.history), 0)
        
        self.simulation.step()
        self.assertEqual(len(self.simulation.history), 1)
        
        row = self.simulation.history[0]
        self.assertEqual(row["epoch"], 1)
        self.assertIn("event_type", row)
        self.assertIn("event_impact", row)
        
        # Sprawdzenie obecności kluczy wyceny portfela oraz wolnych środków cash
        self.assertIn("capital_Anna", row)
        self.assertIn("cash_Anna", row)
        self.assertIn("capital_Bartek", row)
        self.assertIn("cash_Bartek", row)
        self.assertIn("capital_Algo1", row)
        self.assertIn("cash_Algo1", row)

    def test_run_simulation_completes(self) -> None:
        """Testuje pełne uruchomienie symulacji o określonej liczbie epok."""
        self.simulation.run()
        self.assertEqual(len(self.simulation.history), 5)
        self.assertEqual(self.simulation.market.current_epoch, 5)

    def test_export_csv_headers_and_rows(self) -> None:
        """Testuje eksportowanie wyników symulacji do pliku CSV z nowymi kolumnami."""
        self.simulation.step()
        self.simulation.step()
        
        self.simulation.export_csv(self.temp_csv)
        self.assertTrue(os.path.exists(self.temp_csv))
        
        with open(self.temp_csv, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            # Weryfikacja nagłówków pliku CSV
            self.assertIn("epoch", headers)
            self.assertIn("event_type", headers)
            self.assertIn("capital_Anna", headers)
            self.assertIn("cash_Anna", headers)
            self.assertIn("capital_Bartek", headers)
            self.assertIn("cash_Bartek", headers)
            self.assertIn("capital_Algo1", headers)
            self.assertIn("cash_Algo1", headers)
            
            # Weryfikacja liczby wierszy danych
            rows = list(reader)
            self.assertEqual(len(rows), 2)


if __name__ == "__main__":
    unittest.main()
