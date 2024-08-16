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
    
    def clearStrategy(self) -> None:
        self.data["Buy"] = None
        self.data["Sell"] = None
        self.strategyList = {
            "Buy" : [],
            "Sell" : []
        }

    def useCrossOver(self, action: str, logic: bool, firstLine: str, secondLine: str) -> None:
        if action == "buy":
            for i in range(1, len(self.data)-1, 1):
                if (self.data.loc[i-1, firstLine] < self.data.loc[i-1, secondLine]) and (self.data.loc[i, firstLine] > self.data.loc[i, secondLine]):
                    if self.data.loc[i, "Buy"] == None:
                        self.data.loc[i, "Buy"] = True
                    else:
                        if logic:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] and True
                        else:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] or True
                else:
                    if self.data.loc[i, "Buy"] == None:
                        self.data.loc[i, "Buy"] = False
                    else:
                        if logic:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] and False
                        else:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] or False
            self.strategyList["Buy"].append(firstLine + " cross up " + secondLine)
        
        if action == "sell":
            for i in range(1, len(self.data)-1, 1):
                if (self.data.loc[i-1, firstLine] > self.data.loc[i-1, secondLine]) and (self.data.loc[i, firstLine] < self.data.loc[i, secondLine]):
                    if self.data.loc[i, "Sell"] == None:
                        self.data.loc[i, "Sell"] = True
                    else:
                        if logic:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] and True
                        else:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] or True
                else:
                    if self.data.loc[i, "Sell"] == None:
                        self.data.loc[i, "Sell"] = False
                    else:
                        if logic:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] and False
                        else:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] or False
            self.strategyList["Sell"].append(firstLine + " cross down " + secondLine)
    
    def useUpperLowerBoundary(self, action: str, logic: bool, line: str, upperBoundary: float, lowerBoundary: float) -> None:
        if action == "buy":
            for i in range(1, len(self.data), 1):
                if self.data.loc[i-1, line] < lowerBoundary:
                    if self.data.loc[i, "Buy"] == None:
                        self.data.loc[i, "Buy"] = True
                    else:
                        if logic == True:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] and True
                        else:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] or True
                else:
                    if self.data.loc[i, "Buy"] == None:
                        self.data.loc[i, "Buy"] = False
                    else:
                        if logic == True:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] and False
                        else:
                            self.data.loc[i, "Buy"] = self.data.loc[i, "Buy"] or False
            self.strategyList["Buy"].append(line + " below " + str(lowerBoundary))
            
        if action == "sell":
            for i in range(1, len(self.data), 1):
                if self.data.loc[i-1, line] > upperBoundary:
                    if self.data.loc[i, "Sell"] == None:
                        self.data.loc[i, "Sell"] = True
                    else:
                        if logic == True:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] and True
                        else:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] or True
                else:
                    if self.data.loc[i, "Sell"] == None:
                        self.data.loc[i, "Sell"] = False
                    else:
                        if logic == True:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] and False
                        else:
                            self.data.loc[i, "Sell"] = self.data.loc[i, "Sell"] or False
            self.strategyList["Sell"].append(line + " above " + str(upperBoundary))

if __name__ == "__main__":
    pass