class StockTracker:
    def __init__(self, stockAmount: int = 0, stockValue: float = 0) -> None:
        self.stockAmount = stockAmount
        self.stockValue = stockValue

    def add(self, stockAmount: int = 0, priceBrought: float = 0) -> None:
        self.stockAmount += stockAmount
        self.stockValue += stockAmount * priceBrought

    def remove(self) -> None:
        self.stockAmount = 0
        self.stockValue = 0

    def getStockAmount(self) -> int:
        return self.stockAmount
    
    def setStockAmount(self, stockAmount: int) -> None:
        self.stockAmount = stockAmount

    def getStockValue(self) -> float:
        return self.stockValue
    
    def setStockValue(self, stockValue: float) -> None:
        return self.stockValue
    
    def __str__(self) -> str:
        return "Stock Amount: " + str(self.stockAmount) + "\n" + "Stock Value: " + str(self.stockValue)
    
    def __eq__(self, newTracker: object) -> bool:
        if (self.stockAmount == newTracker.stockAmount) and (self.stockValue == newTracker.stockValue):
            return True
        return False
    
if __name__ == "__main__":
    tracker = StockTracker()
    print(tracker)
    print("----------")

    tracker.add(stockAmount=200, priceBrought=20)
    print(tracker)
    print("----------")

    newTracker = StockTracker(stockAmount=200, stockValue=4000)
    print(tracker == newTracker)
    print("----------")

    tracker.remove() # think about this this might not make sense
    print(tracker)
    print("----------")

    print(tracker == newTracker)
    print("----------")