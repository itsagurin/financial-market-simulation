"""Testy jednostkowe dla klas inwestorów i ich zachowań."""

import unittest
from market.financial_instrument import FinancialInstrument, InstrumentType
from investor.conservative_investor import ConservativeInvestor
from investor.aggressive_investor import AggressiveInvestor
from investor.algorithmic_investor import AlgorithmicInvestor
from investor.investor import Investor


class DummyTransaction:
    """Prosta atrapa udanej transakcji dla celów testowych."""
    def __init__(self, settled: bool = True) -> None:
        self.settled = settled


class MockMarket:
    """Atrapa rynku do kontrolowania cen, nastrojów i transakcji."""

    def __init__(self) -> None:
        self.sentiment = 0.0
        self.instruments = []
        self.transactions = []

    def get_instrument_by_symbol(self, symbol: str):
        for instrument in self.instruments:
            if instrument.symbol == symbol:
                return instrument
        return None

    def execute_transaction(self, buyer, seller, instrument, quantity: int, price: float):
        total_cost = quantity * price
        
        # Prosta emulacja rozliczenia
        if buyer is not None:
            if buyer.capital < total_cost:
                return None
            buyer.capital -= total_cost
            buyer.add_to_portfolio(instrument.symbol, quantity)
        if seller is not None:
            seller.capital += total_cost
            seller.remove_from_portfolio(instrument.symbol, quantity)
            
        transaction = DummyTransaction()
        self.transactions.append(transaction)
        return transaction


class TestInvestors(unittest.TestCase):
    """Zestaw testów dla klas reprezentujących inwestorów."""

    def setUp(self) -> None:
        """Przygotowanie testowego rynku i instrumentów przed każdym testem."""
        self.market = MockMarket()
        self.aapl = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        self.obl = FinancialInstrument("OBL2028", "Polish Bond", 10.0, 0.02, InstrumentType.BOND)
        self.market.instruments = [self.aapl, self.obl]

    def test_investor_base_validation(self) -> None:
        """Testuje sprawdzanie poprawności przy inicjalizacji bazowego inwestora."""
        with self.assertRaises(ValueError):
            ConservativeInvestor("Anna", -500.0)
        
        # Bezpośrednie wywołanie klasy bazowej z niepoprawną tolerancją ryzyka
        with self.assertRaises(ValueError):
            class BadInvestor(Investor):
                def decide_action(self, market):
                    return "WAIT"
            BadInvestor("Złe", 1000.0, risk_tolerance=1.5)

    def test_portfolio_operations(self) -> None:
        """Testuje dodawanie i usuwanie instrumentów z portfela."""
        investor = ConservativeInvestor("Anna", 10000.0)
        self.assertEqual(investor.get_portfolio_quantity("AAPL"), 0)
        
        investor.add_to_portfolio("AAPL", 5)
        self.assertEqual(investor.get_portfolio_quantity("AAPL"), 5)
        
        investor.remove_from_portfolio("AAPL", 3)
        self.assertEqual(investor.get_portfolio_quantity("AAPL"), 2)
        
        # Próba usunięcia większej liczby jednostek niż posiadana
        with self.assertRaises(ValueError):
            investor.remove_from_portfolio("AAPL", 5)

    def test_portfolio_value_calculation(self) -> None:
        """Testuje obliczanie całkowitej wartości portfela (Net Worth)."""
        investor = ConservativeInvestor("Anna", 1000.0)
        investor.add_to_portfolio("AAPL", 2)  # 2 * 100.0 = 200.0
        investor.add_to_portfolio("OBL2028", 10)  # 10 * 10.0 = 100.0
        # Wycena: 1000.0 (gotówka) + 200.0 + 100.0 = 1300.0
        self.assertEqual(investor.get_portfolio_value(self.market), 1300.0)

    def test_conservative_investor_buy(self) -> None:
        """Testuje decyzję zakupową konserwatywnego inwestora przy dobrych nastrojach."""
        investor = ConservativeInvestor("Anna", 500.0)
        self.market.sentiment = 0.1  # Powinno triggerować zakup (> -0.15)
        
        action = investor.decide_action(self.market)
        self.assertEqual(action, "BUY OBL2028 x10")
        self.assertEqual(investor.get_portfolio_quantity("OBL2028"), 10)
        self.assertEqual(investor.capital, 500.0 - 10 * 10.0)

    def test_conservative_investor_sell(self) -> None:
        """Testuje decyzję sprzedażową konserwatywnego inwestora przy bardzo złych nastrojach."""
        investor = ConservativeInvestor("Anna", 500.0)
        investor.add_to_portfolio("OBL2028", 20)
        
        self.market.sentiment = -0.4  # Powinno triggerować panic-sell (< -0.3)
        action = investor.decide_action(self.market)
        self.assertEqual(action, "SELL OBL2028 x5")
        self.assertEqual(investor.get_portfolio_quantity("OBL2028"), 15)
        self.assertEqual(investor.capital, 500.0 + 5 * 10.0)

    def test_aggressive_investor_decide_action(self) -> None:
        """Testuje, czy agresywny inwestor podejmuje losowe decyzje o poprawnym wolumenie."""
        investor = AggressiveInvestor("Bartek", 50000.0)
        investor.add_to_portfolio("AAPL", 20)
        investor.add_to_portfolio("OBL2028", 20)
        
        # Uruchamiamy decide_action kilka razy, aby upewnić się, że ilości są w przedziale [5, 15]
        # oraz wolumeny nie przekraczają dostępności kapitału.
        for _ in range(20):
            action = investor.decide_action(self.market)
            if "BUY" in action:
                parts = action.split(" x")
                qty = int(parts[1])
                self.assertTrue(5 <= qty <= 15)
                # Sprawdzenie czy buy_qty nie przekroczył dopuszczalnego budżetu
                instrument = self.market.get_instrument_by_symbol(parts[0].split("BUY ")[1])
                self.assertTrue(qty * instrument.price <= investor.capital + (qty * instrument.price))
            elif "SELL" in action:
                parts = action.split(" x")
                qty = int(parts[1])
                self.assertTrue(5 <= qty <= 15)

    def test_algorithmic_investor_trend_buy(self) -> None:
        """Testuje podążanie za trendem przez AlgorithmicInvestor."""
        investor = AlgorithmicInvestor("Algo1", 2000.0)
        
        # Symulujemy trend wzrostowy dla AAPL. Okno 3 elementów.
        # AAPL price_history: [100.0]. Dodajmy wzrost:
        self.aapl.update_price(0.06)  # 106.0
        self.aapl.update_price(0.08)  # 114.48
        # Historia: [100.0, 106.0, 114.48]
        # Trend: (114.48 - 100.0)/100.0 = 0.1448 (> 0.05) -> Kupuje!
        
        action = investor.decide_action(self.market)
        self.assertEqual(action, "BUY AAPL x10")
        self.assertEqual(investor.get_portfolio_quantity("AAPL"), 10)


if __name__ == "__main__":
    unittest.main()
