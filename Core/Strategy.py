class Strategy:
    def __init__(self, dataframe) -> None:
        self.data = dataframe
        self.data["Buy"] = None
        self.data["Sell"] = None
        self.strategyList = []

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data

    def useCrossOver(self, firstLine: str, secondLine: str) -> None:
        for i in range(1, len(self.data), 1):
            if self.data[firstLine][i-1] < self.data[secondLine][i-1]:
                if self.data[firstLine][i] > self.data[secondLine][i]:
                    currentAction = self.data["Buy"][i]
                    newAction = True
                    if currentAction != None:
                        newAction = currentAction and newAction
                    self.data["Buy"][i] = newAction

            if self.data[firstLine][i-1] > self.data[secondLine][i-1]:
                if self.data[firstLine][i] < self.data[secondLine][i]:
                    currentAction = self.data["Sell"][i]
                    newAction = True
                    if currentAction != None:
                        newAction = currentAction and newAction
                    self.data["Sell"][i] = newAction
        self.strategyList.append("Cross Over")
    
    def useUpperLowerBoundary(self, line: str, upperBoundary: float, lowerBoundary: float) -> None:
        for i in range(len(self.data)):
            if self.data[line][i-1] < lowerBoundary:
                currentAction = self.data["Buy"][i]
                newAction = True
                if currentAction != None:
                    newAction = currentAction and newAction
                self.data["Buy"][i] = newAction
            
            if self.data[line][i-1] > upperBoundary:
                currentAction = self.data["Buy"][i]
                newAction = True
                if currentAction != None:
                    newAction = currentAction and newAction
                self.data["Sell"][i] = newAction

if __name__ == "__main__":
    pass