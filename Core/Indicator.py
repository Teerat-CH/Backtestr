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

    def makeMA(self, averageInterval: int) -> str:

        strategyType = "MA"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):
        
            self.data[strategyName] = self.data.Close.rolling(averageInterval, adjust = False, min_periods=averageInterval).mean()

        return str(strategyName)

    def makeEMA(self, averageInterval: int) -> str:
        
        strategyType = "EMA"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):

            self.data[strategyName] = self.data.Close.ewm(span=averageInterval, adjust=False, min_periods=averageInterval).mean()

        return str(strategyName)

    def makeMACD(self, firstAverageInterval: int, secondAverageInterval: int, signalAverageInterval: int) -> str|str:

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

    def makeRSI(self, averageInterval: int) -> None:

        strategyType = "RSI"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):

            # Calculate gain and loss
            for i in range(len(self.data)):
                if i > 0:
                    if self.data.iloc[i]['Close'] > self.data.iloc[i-1]['Close']:
                        self.data.at[i, 'gain'] = self.data.iloc[i]['CLose'] - self.data.iloc[i-1]['Close']
                        self.data.at[i, 'loss'] = 0
                    elif self.data.iloc[i]['Close'] < self.data.iloc[i-1]['Close']:
                        self.data.at[i, 'loss'] = self.data.iloc[i-1]['Close'] - self.data.iloc[i]['Close']
                        self.data.at[i, 'gain'] = 0
                    else:
                        self.data.at[i, 'gain'] = 0
                        self.data.at[i, 'loss'] = 0

            self.data['averageGain' + str(averageInterval)] = self.data.gain.ewm(span=averageInterval, adjust=False, min_periods=averageInterval).mean()
            self.data['averageLoss' + str(averageInterval)] = self.data.loss.ewm(span=averageInterval, adjust=False, min_periods=averageInterval).mean()
            self.data['rs' + str(averageInterval)] = self.data['averageGain' + str(averageInterval)] / self.data['averageLoss' + str(averageInterval)]
            self.data['RSI'+ str(averageInterval)] = 100 - (100 / (1 + self.data['rs' + str(averageInterval)]))

        return str(strategyName)

    def makeStochRSI(self, averageInterval):

        strategyType = "StochRSI"
        strategyName = str(strategyType) + str(averageInterval)

        if not self.hasStrategy(strategyType, strategyName):

            RSIName = "RSI" + str(averageInterval)
            
            if not self.hasStrategy("RSI", RSIName):
                self.makeRSI(averageInterval=averageInterval)

            maxName = "max" + str(averageInterval)
            minName = "min" + str(averageInterval)

            self.data[maxName] = self.data[RSIName].rolling(window=averageInterval, min_periods=averageInterval).max()
            self.data[minName] = self.data[RSIName].rolling(window=averageInterval, min_periods=averageInterval).min()
            self.data['StochRSI' + str(averageInterval)] = (self.data[RSIName] - self.data[minName]) / (self.data[maxName] - self.data[minName])

        return str(strategyName)
        
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
