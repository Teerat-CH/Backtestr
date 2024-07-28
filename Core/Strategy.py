class Strategy:
    def __init__(self, dataframe) -> None:
        self.data = dataframe
        strategyList = []

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data

    def useCrossOver(self, firstLine: str, secondLine: str) -> None:
        for time in range(len(self.data)):
            if self.data[firstLine][time-1] < self.data[secondLine][time-1]:
                if self.data[firstLine][time] > self.data[secondLine][time]:
                    currentAction = self.data["Buy"][i]
                    newAction = True
                    if currentAction != None:
                        newAction = currentAction and newAction
                    self.data["Buy"][time] = newAction

            if self.data[firstLine][time-1] > self.data[secondLine][time-1]:
                if self.data[firstLine][time] < self.data[secondLine][time]:
                    currentAction = self.data["Sell"][i]
                    newAction = True
                    if currentAction != None:
                        newAction = currentAction and newAction
                    self.data["Sell"][time] = newAction
        self.strategyList.append("Cross Over")
    
    def useRSI(self):
        pass