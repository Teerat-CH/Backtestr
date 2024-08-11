class Strategy:
    def __init__(self, dataframe) -> None:
        self.data = dataframe
        self.data["Buy"] = True
        self.data["Sell"] = True
        self.strategyList = {
            "Buy" : [],
            "Sell" : []
        }

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data
    
    def getStrategyList(self):
        return self.strategyList

    def useCrossOver(self, firstLine: str, secondLine: str) -> None:
        pass
        # for i in range(1, len(self.data)-1, 1):
        #     if (self.data[firstLine][i-1] < self.data[secondLine][i-1]) and (self.data[firstLine][i] > self.data[secondLine][i]):
        #         self.data["Buy"][i] = self.data["Buy"][i] and True
        #     else:
        #         self.data["Buy"][i] = False

        #     if (self.data[firstLine][i-1] > self.data[secondLine][i-1]) and (self.data[firstLine][i] < self.data[secondLine][i]):
        #         self.data["Sell"][i] = self.data["Sell"][i] and True
        #     else:
        #         self.data["Sell"][i] = False

        self.strategyList["Buy"].append(firstLine + " cross up " + secondLine)
        self.strategyList["Sell"].append(firstLine + " cross down " + secondLine)
    
    def useUpperLowerBoundary(self, line: str, upperBoundary: float, lowerBoundary: float) -> None:
        pass
        # for i in range(1, len(self.data), 1):
        #     if self.data[line][i-1] < lowerBoundary:
        #         self.data["Buy"][i] = self.data["Buy"][i] and True
        #     else:
        #         self.data["Buy"][i] = False
            
        #     if self.data[line][i-1] > upperBoundary:
        #         self.data["Sell"][i] = self.data["Sell"][i] and True
        #     else:
        #         self.data["Sell"][i] = False
                
        # self.strategyList["Buy"].append(line + " below " + str(lowerBoundary))
        # self.strategyList["Sell"].append(line + " above " + str(upperBoundary))

if __name__ == "__main__":
    pass