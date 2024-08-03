from Core.StockTracker import StockTracker
from Core.Portfolio import Portfolio
from Core.Indicator import Indicator
from Core.Strategy import Strategy

class Backtestr:
    def __init__(self, data, stockName) -> None:
        self.data = data
        self.data["netValue"] = 0
        self.portfolio = Portfolio()

        self.stockName = stockName

    def setStock(self, stockName: str) -> None:
        self.stockName = stockName

    def getPortfolio(self):
        return self.Portfolio
    
    def runTest(self, initialFund: float, stockAmountBuy: int):
        self.portfolio.addFund(initialFund)
        for i in range(len(self.data)):
            if self.data["Buy"][i] == True:
                self.portfolio.buy(stockName=self.stockName, stockAmount=stockAmountBuy, stockPrice=self.data.Open[i])
            if self.data["Sell"][i] == True:
                self.portfolio.sell(stockName=self.stockName, stockPrice=self.data.Open[i])
            self.data["netValue"][i] = self.portfolio.getNetValue()            
        return self.portfolio.getNetValue()