class SingleStockPortfolio:
    def __init__(self, cash: float = 0, stockAmount: int = 0, stockValue: float = 0, fee: float = 0.25) -> None:
        self.cash = cash
        self.stockAmount = stockAmount
        self.stockValue = stockValue
        self.fee = fee
        self.log = []

    def buy(self, stockAmount: int, stockPrice: float) -> bool:
        if self.cash > stockPrice * stockAmount * (100 + self.fee) / 100:
          self.cash -= stockPrice * stockAmount * (100 + self.fee) / 100
          self.stockAmount += stockAmount
          self.stockValue += stockPrice * stockAmount
          return True
        return False

    def sell(self, stockPrice: float) -> bool:
        if self.stockAmount > 0:
          self.stockValue = 0
          self.cash += self.stockAmount * stockPrice * (100 - self.fee) / 100
          self.stockAmount = 0
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

    def getStockAmount(self) -> int:
        return self.stockAmount

    def getStockValue(self) -> float:
        return self.stockValue

    def getNetValue(self) -> float:
        return self.cash + self.stockValue
    
    def getFee(self) -> float:
        return self.fee
    
    def setFee(self, fee) -> None:
        self.fee = fee

    def addLog(self, action: str, amount: int, price: float, date: object) -> None:
        self.log.append(action + " " + str(amount) + " stocks at " + str(price) + " on " + str(date))

    def getLog(self) -> list:
        return self.log

    def __str__(self) -> str:
        string = "Cash: " + str(self.cash) + "\n" + "Stock Amount: " + str(self.stockAmount) + "\n" + "Stock Value: " + str(self.stockValue) + "\n" + "Net Value: " + str(self.getNetValue())
        return string
    
if __name__ == "__main__":
    port = SingleStockPortfolio()
    print(port)
    print("----------")

    port.addFund(1000)
    print(port)
    print("----------")

    port.buy(100, 5)
    print(port)
    print("----------")
