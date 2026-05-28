"""Testy jednostkowe dla klas Market i Transaction."""

import unittest
from market.financial_instrument import FinancialInstrument, InstrumentType
from market.market import Market
from market.transaction import Transaction
from investor.conservative_investor import ConservativeInvestor
from event.growth_event import GrowthEvent
from event.crash_event import CrashEvent


class TestMarketAndTransaction(unittest.TestCase):
    """Zestaw testów dla infrastruktury rynkowej i zawierania transakcji."""

    def setUp(self) -> None:
        """Przygotowanie rynku i obiektów do każdego testu."""
        self.market = Market()
        self.aapl = FinancialInstrument("AAPL", "Apple Inc.", 100.0, 0.15, InstrumentType.STOCK)
        self.obl = FinancialInstrument("OBL2028", "Polish Bond", 50.0, 0.02, InstrumentType.BOND)
        self.market.add_instrument(self.aapl)
        self.market.add_instrument(self.obl)

    def test_market_sentiment_bounds(self) -> None:
        """Testuje, czy sentyment rynkowy mieści się w dopuszczalnym zakresie [-1.0, 1.0]."""
        self.assertEqual(self.market.sentiment, 0.0)

        # Ręcznie ustawiamy sentyment ponad granice
        self.market.sentiment = 1.5
        self.assertEqual(self.market.sentiment, 1.0)

        self.market.sentiment = -2.0
        self.assertEqual(self.market.sentiment, -1.0)

    def test_apply_event(self) -> None:
        """Testuje wpływ wydarzeń na ceny instrumentów rynkowych oraz sentyment."""
        event = GrowthEvent()  # Dodatni wpływ
        self.market.apply_event(event)

        # Ceny instrumentów powinny pójść w górę
        self.assertTrue(self.aapl.price > 100.0)
        self.assertTrue(self.obl.price > 50.0)
        # Sentyment rynkowy powinien wzrosnąć
        self.assertTrue(self.market.sentiment > 0.0)

    def test_transaction_success_with_liquidity_provider(self) -> None:
        """Testuje transakcję zakupu od płynności rynkowej (brak sprzedawcy)."""
        buyer = ConservativeInvestor("Anna", 1000.0)
        
        # Kupujemy 5 sztuk AAPL po cenie 100.0 -> koszt 500.0
        transaction = Transaction(
            buyer=buyer,
            seller=None,
            instrument=self.aapl,
            quantity=5,
            price=100.0,
            epoch=1
        )
        self.assertFalse(transaction.settled)
        
        success = transaction.settle()
        self.assertTrue(success)
        self.assertTrue(transaction.settled)
        
        # Sprawdzamy portfel i kapitał kupującego
        self.assertEqual(buyer.capital, 500.0)
        self.assertEqual(buyer.get_portfolio_quantity("AAPL"), 5)

    def test_transaction_failed_insufficient_funds(self) -> None:
        """Testuje odrzucenie transakcji przy braku wystarczających środków u kupującego."""
        buyer = ConservativeInvestor("Anna", 300.0)
        
        # Próba kupna 4 sztuk AAPL po 100.0 -> koszt 400.0 (za drogo)
        transaction = Transaction(
            buyer=buyer,
            seller=None,
            instrument=self.aapl,
            quantity=4,
            price=100.0,
            epoch=1
        )
        success = transaction.settle()
        self.assertFalse(success)
        self.assertFalse(transaction.settled)
        
        # Kapitał i portfel bez zmian
        self.assertEqual(buyer.capital, 300.0)
        self.assertEqual(buyer.get_portfolio_quantity("AAPL"), 0)

    def test_transaction_between_investors_success(self) -> None:
        """Testuje udaną transakcję bezpośrednią między dwoma inwestorami."""
        buyer = ConservativeInvestor("Anna", 1000.0)
        seller = ConservativeInvestor("Marek", 500.0)
        seller.add_to_portfolio("AAPL", 10)
        
        # Transakcja: Anna kupuje od Marka 3 sztuki AAPL po 100.0
        transaction = Transaction(
            buyer=buyer,
            seller=seller,
            instrument=self.aapl,
            quantity=3,
            price=100.0,
            epoch=1
        )
        success = transaction.settle()
        self.assertTrue(success)
        
        self.assertEqual(buyer.capital, 700.0)
        self.assertEqual(buyer.get_portfolio_quantity("AAPL"), 3)
        self.assertEqual(seller.capital, 800.0)
        self.assertEqual(seller.get_portfolio_quantity("AAPL"), 7)

    def test_transaction_between_investors_insufficient_seller_assets(self) -> None:
        """Testuje odrzucenie transakcji bezpośredniej z powodu braku aktywów u sprzedawcy."""
        buyer = ConservativeInvestor("Anna", 1000.0)
        seller = ConservativeInvestor("Marek", 500.0)
        seller.add_to_portfolio("AAPL", 2)  # Tylko 2 sztuki
        
        # Próba zakupu 3 sztuk AAPL
        transaction = Transaction(
            buyer=buyer,
            seller=seller,
            instrument=self.aapl,
            quantity=3,
            price=100.0,
            epoch=1
        )
        success = transaction.settle()
        self.assertFalse(success)
        self.assertFalse(transaction.settled)
        
        # Nic się nie zmienia
        self.assertEqual(buyer.capital, 1000.0)
        self.assertEqual(buyer.get_portfolio_quantity("AAPL"), 0)
        self.assertEqual(seller.capital, 500.0)
        self.assertEqual(seller.get_portfolio_quantity("AAPL"), 2)


if __name__ == "__main__":
    unittest.main()
