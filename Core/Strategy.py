class Strategy:
    def __init__(self, dataframe) -> None:
        self.data = dataframe

    def crossOverBuy(self, time: int, firstLine: str, secondLine: str) -> bool:
        if self.data[firstLine][time-1] < self.data[secondLine][time-1]:
            if self.data[firstLine][time] > self.data[secondLine][time]:
                return True
        return False
    
    def crossOverSell(self, time: int, firstLine: str, secondLine: str) -> bool:
        if self.data[firstLine][time-1] > self.data[secondLine][time-1]:
            if self.data[firstLine][time] < self.data[secondLine][time]:
                return True
        return False