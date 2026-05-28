"""Testy jednostkowe dla klasy FinancialInstrument."""

import unittest
from market.financial_instrument import FinancialInstrument, InstrumentType


class TestFinancialInstrument(unittest.TestCase):
    """Zestaw testów dla instrumentów finansowych."""

    def test_initialization_valid(self) -> None:
        """Testuje poprawną inicjalizację instrumentu."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        self.assertEqual(instrument.symbol, "AAPL")
        self.assertEqual(instrument.name, "Apple Inc.")
        self.assertEqual(instrument.price, 100.0)
        self.assertEqual(instrument.initial_price, 100.0)
        self.assertEqual(instrument.volatility, 0.15)
        self.assertEqual(instrument.instrument_type, InstrumentType.STOCK)
        self.assertEqual(len(instrument.price_history), 1)
        self.assertEqual(instrument.price_history[0], 100.0)

    def test_initialization_invalid_price(self) -> None:
        """Testuje rzucenie wyjątku przy ujemnej lub zerowej cenie początkowej."""
        with self.assertRaises(ValueError):
            FinancialInstrument("AAPL", "Apple", -10.0, 0.15, InstrumentType.STOCK)
        with self.assertRaises(ValueError):
            FinancialInstrument("AAPL", "Apple", 0.0, 0.15, InstrumentType.STOCK)

    def test_initialization_invalid_volatility(self) -> None:
        """Testuje rzucenie wyjątku przy zmienności poza zakresem [0, 1]."""
        with self.assertRaises(ValueError):
            FinancialInstrument("AAPL", "Apple", 100.0, -0.01, InstrumentType.STOCK)
        with self.assertRaises(ValueError):
            FinancialInstrument("AAPL", "Apple", 100.0, 1.01, InstrumentType.STOCK)

    def test_update_price_positive(self) -> None:
        """Testuje poprawny wzrost ceny o współczynnik."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        instrument.update_price(0.10)  # +10%
        self.assertAlmostEqual(instrument.price, 110.0)
        self.assertEqual(len(instrument.price_history), 2)
        self.assertAlmostEqual(instrument.price_history[-1], 110.0)

    def test_update_price_negative_with_floor(self) -> None:
        """Testuje spadek ceny oraz ograniczenie dolne do 0.01."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 1.0, 0.15, InstrumentType.STOCK)
        instrument.update_price(-0.50)  # -50% -> 0.50
        self.assertAlmostEqual(instrument.price, 0.50)

        instrument.update_price(-0.99)  # -99% -> powinien uderzyć w podłogę 0.01
        self.assertEqual(instrument.price, 0.01)

    def test_apply_shock(self) -> None:
        """Testuje bezwzględny szok cenowy."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        instrument.apply_shock(15.50)  # +15.5
        self.assertAlmostEqual(instrument.price, 115.50)
        instrument.apply_shock(-120.0)  # -120 -> uderza w podłogę 0.01
        self.assertEqual(instrument.price, 0.01)

    def test_get_price_change_percent(self) -> None:
        """Testuje obliczanie procentowej zmiany ceny."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        instrument.update_price(0.25)  # +25%
        self.assertAlmostEqual(instrument.get_price_change_percent(), 25.0)

    def test_get_average_price(self) -> None:
        """Testuje obliczanie średniej arytmetycznej z historii cen."""
        instrument = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        instrument.update_price(0.10)  # 110.0
        instrument.update_price(-0.20)  # 110.0 * 0.8 = 88.0
        # Historia: [100.0, 110.0, 88.0] -> średnia: 99.3333...
        self.assertAlmostEqual(instrument.get_average_price(), 99.33333333)


if __name__ == "__main__":
    unittest.main()
