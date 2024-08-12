class Strategy:
    def __init__(self, dataframe) -> None:
        self.data = dataframe
        self.data["Buy"] = None
        self.data["Sell"] = None
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

    def useCrossOver(self, action: str, logic: bool, firstLine: str, secondLine: str) -> None:
        if action == "buy":
            for i in range(1, len(self.data)-1, 1):
                if (self.data[firstLine][i-1] < self.data[secondLine][i-1]) and (self.data[firstLine][i] > self.data[secondLine][i]):
                    if self.data["Buy"][i] == None:
                        self.data["Buy"][i] = True
                    else:
                        if logic:
                            self.data["Buy"][i] = self.data["Buy"][i] and True
                        else:
                            self.data["Buy"][i] = self.data["Buy"][i] or True
                else:
                    if self.data["Buy"][i] == None:
                        self.data["Buy"][i] = False
                    else:
                        if logic:
                            self.data["Buy"][i] = self.data["Buy"][i] and False
                        else:
                            self.data["Buy"][i] = self.data["Buy"][i] or False
            self.strategyList["Buy"].append(firstLine + " cross up " + secondLine)
        
        if action == "sell":
            for i in range(1, len(self.data)-1, 1):
                if (self.data[firstLine][i-1] > self.data[secondLine][i-1]) and (self.data[firstLine][i] < self.data[secondLine][i]):
                    if self.data["Sell"][i] == None:
                        self.data["Sell"][i] = True
                    else:
                        if logic:
                            self.data["Sell"][i] = self.data["Sell"][i] and True
                        else:
                            self.data["Sell"][i] = self.data["Sell"][i] or True
                else:
                    if self.data["Sell"][i] == None:
                        self.data["Sell"][i] = False
                    else:
                        if logic:
                            self.data["Sell"][i] = self.data["Sell"][i] and False
                        else:
                            self.data["Sell"][i] = self.data["Sell"][i] or False
            self.strategyList["Sell"].append(firstLine + " cross down " + secondLine)
    
    def useUpperLowerBoundary(self, action: str, logic: bool, line: str, upperBoundary: float, lowerBoundary: float) -> None:
        if action == "buy":
            for i in range(1, len(self.data), 1):
                if self.data[line][i-1] < lowerBoundary:
                    if self.data["Buy"][i] == None:
                        self.data["Buy"][i] = True
                    else:
                        if logic == True:
                            self.data["Buy"][i] = self.data["Buy"][i] and True
                        else:
                            self.data["Buy"][i] = self.data["Buy"][i] or True
                else:
                    if self.data["Buy"][i] == None:
                        self.data["Buy"][i] = False
                    else:
                        if logic == True:
                            self.data["Buy"][i] = self.data["Buy"][i] and False
                        else:
                            self.data["Buy"][i] = self.data["Buy"][i] or False
            self.strategyList["Buy"].append(line + " below " + str(lowerBoundary))
            
        if action == "sell":
            for i in range(1, len(self.data), 1):
                if self.data[line][i-1] > upperBoundary:
                    if self.data["Sell"][i] == None:
                        self.data["Sell"][i] = True
                    else:
                        if logic == True:
                            self.data["Sell"][i] = self.data["Sell"][i] and True
                        else:
                            self.data["Sell"][i] = self.data["Sell"][i] or True
                else:
                    if self.data["Sell"][i] == None:
                        self.data["Sell"][i] = False
                    else:
                        if logic == True:
                            self.data["Sell"][i] = self.data["Sell"][i] and False
                        else:
                            self.data["Sell"][i] = self.data["Sell"][i] or False
            self.strategyList["Sell"].append(line + " above " + str(upperBoundary))

if __name__ == "__main__":
    pass