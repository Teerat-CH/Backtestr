from Core.Portfolio import Portfolio
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
    
    def runTest(self, initialFund: float, stockAmountBuy: float, stockAmountSell: float, usePercentBuy: bool = False, usePercentSell: bool = False, minimumStockPerPosition: float = 100):
        self.portfolio.addFund(initialFund)
        for i in range(len(self.data)):
            if self.data.loc[i, "Buy"] == True:
                if usePercentBuy == False:
                    self.portfolio.buy(stockName=self.stockName, stockAmount=stockAmountBuy, stockPrice=self.data.Open[i])
                else:
                    numberOfStocks = percentToStockAmountBuy(cash=self.portfolio.getCash(), percent=stockAmountBuy, currentPrice=self.data.Open[i], minimumStockPerPosition=minimumStockPerPosition)
                    print(self.portfolio.buy(stockName=self.stockName, stockAmount=numberOfStocks, stockPrice=self.data.Open[i]))
            if self.data.loc[i, "Sell"] == True:
                if usePercentSell == False:
                    if self.data.loc[i, "Terminate"] == True:
                        self.portfolio.sell(stockName=self.stockName, stockAmount=self.portfolio.getStockAmount(self.stockName), stockPrice=self.data.Open[i])
                    else:
                        self.portfolio.sell(stockName=self.stockName, stockAmount=stockAmountSell, stockPrice=self.data.Open[i])
                else:
                    numberOfStocks = percentToStockAmountSell(self.portfolio.getStockAmount(self.stockName), percent=stockAmountSell, minimumStockPerPosition=minimumStockPerPosition)
            self.data["netValue"] = self.data["netValue"].astype(float)
            self.data.loc[i, "netValue"] = self.portfolio.getNetValue()         
        return self.portfolio.getNetValue()
    
def percentToStockAmountBuy(cash: float, percent: float, currentPrice: float, minimumStockPerPosition: float) -> float:
    cashToSpend = cash * percent/100
    rawPossibleStockBuy = cashToSpend/currentPrice
    if minimumStockPerPosition == 0:
        return round(rawPossibleStockBuy, 4)
    roundedAmount = rawPossibleStockBuy - (rawPossibleStockBuy % minimumStockPerPosition)
    return round(roundedAmount, 4)

def percentToStockAmountSell(currentStockAmount: float, percent: float, minimumStockPerPosition: float) -> float:
    stockToSell = currentStockAmount * percent/100
    if minimumStockPerPosition == 0:
        return round(stockToSell, 4)
    roundedAmount = stockToSell - (stockToSell % minimumStockPerPosition)
    return round(roundedAmount, 4)