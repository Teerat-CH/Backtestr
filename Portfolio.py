from StockTracker import StockTracker

class Portfolio:
    def __init__(self, cash: float = 0, fee: float = 0.25) -> None:
        self.cash = cash
        self.fee = fee
        self.stockDirectory = {}
        self.log = []

    def buy(self, stockName: str, stockAmount: int, stockPrice: float) -> bool:
        if self.cash > stockPrice * stockAmount * (100 + self.fee) / 100:
            self.cash -= stockPrice * stockAmount * (100 + self.fee) / 100
            if (stockName in self.stockDirectory):
                stockTracker = self.stockDirectory[stockName]
                stockTracker.add(stockAmount, stockPrice)
            else:
                stockTracker = StockTracker()
                self.stockDirectory[stockName] = stockTracker
                stockTracker = self.stockDirectory[stockName]
                stockTracker.add(stockAmount, stockPrice)
            return True
        return False

    def sell(self, stockName: str, stockPrice: float) -> bool:
        if (stockName in self.stockDirectory):
                stockTracker = self.stockDirectory[stockName]
                if stockTracker.getStockAmount() > 0:
                    self.cash += stockTracker.getStockAmount() * stockPrice * (100 - self.fee) / 100
                    stockTracker.remove()
                    return True
        return False

    def getCash(self) -> float:
        return self.cash
    
    def addFund(self, fund: float) -> None:
        self.cash += fund

    def cashOut(self, cashAmout: float) -> bool:
        if cashAmout <= self.cash:
            self.cash -= cashAmout
            return True
        return False
    
    def getStockAmount(self, stockName: str) -> int:
        if stockName in self.stockDirectory:
            return self.stockDirectory[stockName].getStockAmount()
        return -1

    def getStockValue(self, *args) -> float:
        if len(args) == 0:
            stockValue = 0
            for stock in self.stockDirectory:
                stockValue += self.stockDirectory[stock].getStockValue()
            return stockValue
        if len(args) == 1:
            if args[0] in self.stockDirectory:
                return self.stockDirectory[args[0]].getStockValue()
            return -1

    def getNetValue(self) -> float:
        return self.cash + self.getStockValue()
    
    def getFee(self) -> float:
        return self.fee
    
    def setFee(self, fee) -> None:
        self.fee = fee

    def addLog(self, action: str, stockName: str, amount: int, price: float, date: object) -> None:
        self.log.append(action + " " + str(amount) + str(stockName) + " stocks at " + str(price) + " on " + str(date))

    def getLog(self) -> list:
        return self.log
    
    def getStockDirectory(self) -> dict:
        return self.stockDirectory

    def __str__(self) -> str:
        portfolioSummary = ""
        netStockValue = 0
        for stock in self.stockDirectory:
            portfolioSummary += " => " + str(stock) + " | Amount: " + str(self.stockDirectory[stock].getStockAmount()) + " | Value: " + str(self.stockDirectory[stock].getStockValue()) + "\n"
            netStockValue += self.stockDirectory[stock].getStockValue()
        return "Portfolio Summary:\n" + portfolioSummary + "\n" + "Cash: " + str(self.getCash()) + "\n" + "Stock Value: " + str(netStockValue) + "\n" + "Net Value: " + str(netStockValue + self.getCash())
    
class portfolio:
    def __init__(self, cash = 0, stock_amount = 0, stock_value = 0, fee = 0.25):
        self.cash = cash
        self.stock_amount = stock_amount
        self.stock_value = stock_value
        self.net_value = self.cash + self.stock_value
        self.fee = fee
        self.log = []

    def buy(self, stock_amount, stock_price):
        if self.cash > stock_price * stock_amount:
          self.cash -= stock_price * stock_amount * (100+self.fee)/100
          self.stock_amount += stock_amount
          self.stock_value += stock_price * stock_amount
          self.net_value = self.cash + self.stock_value
          return "buy"
        else:
          return "do nothing"

    def sell(self, stock_price):
        if self.stock_amount > 0:
          self.stock_value = 0
          self.cash += self.stock_amount * stock_price * (100-self.fee)/100
          self.stock_amount = 0
          self.net_value = self.cash + self.stock_value
          return "sell"
        else:
          return "do nothing"

    def addFund(self, fund):
        self.cash += fund
        self.net_value += fund

    def getCash(self):
        return self.cash

    def getStockAmount(self):
        return self.stock_amount

    def getStockValue(self):
        return self.stock_value

    def getNetValue(self):
        return self.net_value

    def addLog(self, action, amount, price, date):
        self.log.append(action + " " + str(amount) + " stocks at " + str(price) + " on " + str(date))

    def getLog(self):
        return self.log

    def __str__(self) -> str:
        string = "Cash: " + str(self.cash) + "\nStock Amount: " + str(self.stock_amount) + "\nStock Value: " + str(self.stock_value) + "\nNet Value: " + str(self.net_value)
        return string
    
if __name__ == "__main__":
    port = Portfolio()
    print(port)
    print("----------")

    port.addFund(1000)
    print(port)
    print("----------")

    port.buy("APPL", 100, 5)
    print(port)
    print("----------")

    port.buy("MSFT", 20, 10)
    print(port)
    print("----------")

    print(port.getStockValue("MSFT"))
    print(port.getStockValue("NVIDIA"))