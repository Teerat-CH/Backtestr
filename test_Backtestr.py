import unittest
from SingleStockPortfolio import SingleStockPortfolio
from StockTracker import StockTracker
from Portfolio import Portfolio

class Test_SingleStockPortfolio(unittest.TestCase):

    def test_initializeEmptySingleStockPortfolio(self):
        port = SingleStockPortfolio()
        self.assertEqual(0, port.getCash())
        self.assertEqual(0, port.getStockAmount())
        self.assertEqual(0, port.getStockValue())

    def test_initializeNonEmptySingleStockPortfolio(self):
        port = SingleStockPortfolio(cash=500, stockAmount=200, stockValue=1000)
        self.assertEqual(500, port.getCash())
        self.assertEqual(200, port.getStockAmount())
        self.assertEqual(1000, port.getStockValue())

    def test_addFund(self):
        port = SingleStockPortfolio()
        self.assertEqual(0, port.getCash())
        port.addFund(500)
        self.assertEqual(500, port.getCash())

    def test_cashOut(self):
        port = SingleStockPortfolio(500)
        self.assertEqual(500, port.getCash())
        self.assertFalse(port.cashOut(1000))
        self.assertTrue(port.cashOut(400))
        self.assertEqual(100, port.getCash())

    def test_Fee(self):
        port = SingleStockPortfolio(fee=0.25)
        self.assertEqual(0.25, port.getFee())
        port.setFee(0.15)
        self.assertEqual(0.15, port.getFee())

    def test_buy(self):
        port = SingleStockPortfolio(cash=1000)
        self.assertFalse(port.buy(stockAmount=100, stockPrice=20))
        self.assertFalse(port.buy(stockAmount=100, stockPrice=10)) # Take fee into account. Default fee = 0.25%
        self.assertTrue(port.buy(stockAmount=100, stockPrice=5))
        self.assertEqual(498.75, port.getCash())
        self.assertEqual(100, port.getStockAmount())
        self.assertEqual(500, port.getStockValue())
        self.assertEqual(998.75, port.getNetValue())
        
    def test_sell(self):
        port = SingleStockPortfolio(cash=200, stockAmount=300, stockValue=3000)
        port.sell(12)
        self.assertEqual(3791, port.getCash())
        self.assertEqual(0, port.getStockAmount())
        self.assertEqual(0, port.getStockValue())

    def test_addLog(self):
        from datetime import datetime
        port = SingleStockPortfolio()
        self.assertEqual(0, len(port.getLog()))
        port.addLog("Buy", 100, 10, datetime.now())
        self.assertEqual(1, len(port.getLog()))
        self.assertEqual("Buy 100 stocks at 10 on " + str(datetime.now()), port.getLog()[0])

class Test_StockTracker(unittest.TestCase):

    def test_initializeEmptyStockTracker(self):
        tracker = StockTracker()
        self.assertEqual(0, tracker.getStockAmount())
        self.assertEqual(0, tracker.getStockValue())

class Test_Portfolio(unittest.TestCase):

    def test_initializeEmptyPortfolio(self):
        portfolio = Portfolio()
        self.assertEqual(0, portfolio.getCash())
        self.assertEqual(0, portfolio.getStockValue())
        self.assertEqual(0, portfolio.getNetValue())

if __name__ == '__main__':
    unittest.main()