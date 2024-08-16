from Core.StockTracker import StockTracker
from Core.Portfolio import Portfolio
from Core.Indicator import Indicator
from Core.Strategy import Strategy

import numpy as np

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
    
    def runTest(self, initialFund: float, stockAmountBuy: float, stockAmountSell: float):
        self.portfolio.addFund(initialFund)
        for i in range(len(self.data)):
            if self.data.loc[i, "Buy"] == True:
                self.portfolio.buy(stockName=self.stockName, stockAmount=stockAmountBuy, stockPrice=self.data.Open[i])
            if self.data.loc[i, "Sell"] == True:
                self.portfolio.sell(stockName=self.stockName, stockAmount=stockAmountSell, stockPrice=self.data.Open[i])
            self.data["netValue"] = self.data["netValue"].astype(float)
            self.data.loc[i, "netValue"] = self.portfolio.getNetValue()         
        return self.portfolio.getNetValue()