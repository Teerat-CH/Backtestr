class Indicator:
    #dataframe for data
    def __init__(self, data) -> None:
        self.data = data
        self.strategySet = {
            "MA": set(),
            "EMA": set(),
            "MACD": set(),
            "MACD-Signal": set(),
            "RSI": set(),
            "StochRSI": set()
        }

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def hasStrategy(self, strategyType, strategyName: str) -> bool:
        return strategyName in self.strategySet[strategyType] or False

    def makeMA(self, averageInterval: int) -> None:

        strategyType = "MA"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):
        
            self.data[strategyName] = self.data.Close.rolling(averageInterval, adjust = False, min_periods=averageInterval).mean()

        return str(strategyName)

    def makeEMA(self, averageInterval: int) -> None:
        
        strategyType = "EMA"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):

            self.data[strategyName] = self.data.Close.ewm(span=averageInterval, adjust=False, min_periods=averageInterval).mean()

        return str(strategyName)

    def makeMACD(self, firstAverageInterval: int, secondAverageInterval: int, signalAverageInterval: int) -> None:

        MACDName = "MACD(" + str(firstAverageInterval) + ", " + str(secondAverageInterval) + ")"
        signalName = "Signal(" + str(firstAverageInterval) + ", " + str(secondAverageInterval) + ", " + str(signalAverageInterval) + ")" 

        if not self.hasStrategy("MACD-Signal", signalName):

            if not self.hasStrategy("MACD", MACDName):

                EMA1Name = "EMA" + str(firstAverageInterval)
                EMA2Name = "EMA" + str(secondAverageInterval)
        
                if not self.hasStrategy("EMA", EMA1Name):
                    self.makeEMA(firstAverageInterval)
                
                if not self.hasStrategy("EMA", EMA2Name):
                    self.makeEMA(secondAverageInterval)

                self.data[MACDName] = self.data[EMA1Name] - self.data[EMA2Name]

            self.data[signalName] = self.data[MACDName].ewm(span=signalAverageInterval, adjust=False, min_periods=signalAverageInterval).mean()

        return (signalName, MACDName)

    def makeRSI(self, ):
        pass

    def makeStochRSI(self, ):
        pass
        
    def __str__(self) -> str:
        stringToReturn = "List of Strategy: \n\n"
        for strategyType in self.strategySet:
            stringToReturn += str(strategyType) + " => "
            for strategy in self.strategySet[strategyType]:
                stringToReturn += str(strategy) + ", "
            stringToReturn += "\n"

        return stringToReturn
    
if __name__ == "__main__":
    data = "hello"
    strategy = Indicator(data)
    print(strategy)
