class Indicator:
    def __init__(self, data) -> None:
        self.data = data
        self.indicatorSet = {
            "MA": set(),
            "EMA": set(),
            "MACD": set(),
            "MACD-Signal": set(),
            "RSI": set(),
            "StochRSI": set()
        }
        self.relatedColumn = {}

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data
    
    def getIndicatorSet(self):
        return self.indicatorSet
    
    def getRelatedColumn(self, indicatorName: str) -> None:
        return self.relatedColumn[indicatorName]
    
    def getIndicatorList(self) -> list:
        indicatorList = []
        for indicatorType in self.getIndicatorSet():
            for indicator in self.getIndicatorSet()[indicatorType]:
                indicatorList.append(indicator)
        
        return indicatorList
    
    def addIndicator(self, indicatorType: str, indicatorName: str) -> None:
        self.indicatorSet[indicatorType].add(indicatorName)

    def remove_indicators(self, indicatorsToRemove):
        for indicator in indicatorsToRemove:
            for key in self.indicatorSet:
                if indicator in self.indicatorSet[key]:
                    self.indicatorSet[key].remove(indicator)
                    del self.data[indicator]
                    break

    def hasIndicator(self, indicatorType, indicatorName: str) -> bool:
        return indicatorName in self.indicatorSet[indicatorType] or False

    def makeMA(self, averageInterval: int) -> str:

        indicatorType = "MA"
        indicatorName = str(indicatorType) + str(averageInterval)

        if not self.hasIndicator(indicatorType, indicatorName):
        
            self.data[indicatorName] = self.data.Close.rolling(averageInterval, min_periods=averageInterval).mean()
            self.addIndicator(indicatorType, indicatorName)
            self.relatedColumn[indicatorName] = [indicatorName]

        return str(indicatorName)

    def makeEMA(self, averageInterval: int) -> str:
        
        indicatorType = "EMA"
        indicatorName = str(indicatorType) + str(averageInterval)

        if not self.hasIndicator(indicatorType, indicatorName):

            self.data[indicatorName] = self.data.Close.ewm(span=averageInterval, min_periods=averageInterval).mean()
            self.addIndicator(indicatorType, indicatorName)
            self.relatedColumn[indicatorName] = [indicatorName]

        return str(indicatorName)

    def makeMACD(self, firstAverageInterval: int, secondAverageInterval: int, signalAverageInterval: int) -> str|str:

        MACDName = "MACD(" + str(firstAverageInterval) + ", " + str(secondAverageInterval) + ")"
        signalName = "Signal(" + str(firstAverageInterval) + ", " + str(secondAverageInterval) + ", " + str(signalAverageInterval) + ")"

        if not self.hasIndicator("MACD-Signal", signalName):
            self.relatedColumn[signalName] = [signalName]

            if not self.hasIndicator("MACD", MACDName):
                self.relatedColumn[signalName].append(MACDName)

                EMA1Name = "EMA" + str(firstAverageInterval)
                EMA2Name = "EMA" + str(secondAverageInterval)
        
                if not self.hasIndicator("EMA", EMA1Name):
                    self.relatedColumn[signalName].append(EMA1Name)
                    self.makeEMA(firstAverageInterval)
                
                if not self.hasIndicator("EMA", EMA2Name):
                    self.relatedColumn[signalName].append(EMA2Name)
                    self.makeEMA(secondAverageInterval)

                self.data[MACDName] = self.data[EMA1Name] - self.data[EMA2Name]
                self.addIndicator("MACD", MACDName)

            self.data[signalName] = self.data[MACDName].ewm(span=signalAverageInterval, min_periods=signalAverageInterval).mean()
            self.addIndicator("MACD-Signal", signalName)

        return (signalName, MACDName)

    def makeRSI(self, averageInterval: int) -> None:

        indicatorType = "RSI"
        indicatorName = str(indicatorType) + str(averageInterval)

        if not self.hasIndicator(indicatorType, indicatorName):
            self.relatedColumn[indicatorName] = [indicatorName]

            if "gain" not in self.data or "loss" not in self.data:
                for i in range(1, len(self.data)):
                    if self.data.iloc[i]["Close"] > self.data.iloc[i-1]["Close"]:
                        self.data.loc[self.data.index[i], "gain"] = self.data.iloc[i]["Close"] - self.data.iloc[i-1]["Close"]
                        self.data.loc[self.data.index[i], "loss"] = 0
                    elif self.data.iloc[i]["Close"] < self.data.iloc[i-1]["Close"]:
                        self.data.loc[self.data.index[i], "loss"] = self.data.iloc[i-1]["Close"] - self.data.iloc[i]["Close"]
                        self.data.loc[self.data.index[i], "gain"] = 0
                    else:
                        self.data.loc[self.data.index[i], "gain"] = 0
                        self.data.loc[self.data.index[i], "loss"] = 0
                self.relatedColumn[indicatorName].extend(["gain", "loss"])

            self.data["averageGain" + str(averageInterval)] = self.data.gain.ewm(span=averageInterval, min_periods=averageInterval).mean()
            self.data["averageLoss" + str(averageInterval)] = self.data.loss.ewm(span=averageInterval, min_periods=averageInterval).mean()
            self.data["rs" + str(averageInterval)] = self.data["averageGain" + str(averageInterval)] / self.data["averageLoss" + str(averageInterval)]
            self.data["RSI"+ str(averageInterval)] = 100 - (100 / (1 + self.data["rs" + str(averageInterval)]))
            self.data["RSI"+ str(averageInterval)] = self.data["RSI"+ str(averageInterval)] / 100

            self.relatedColumn[indicatorName].extend(["averageGain" + str(averageInterval), "averageLoss" + str(averageInterval), "rs"+ str(averageInterval)])

            self.addIndicator(indicatorType, indicatorName)
        return str(indicatorName)

    def makeStochRSI(self, averageInterval):

        indicatorType = "StochRSI"
        indicatorName = str(indicatorType) + str(averageInterval)
        if not self.hasIndicator(indicatorType, indicatorName):
            self.relatedColumn[indicatorName] = [indicatorName]

            RSIName = "RSI" + str(averageInterval)
            
            if not self.hasIndicator("RSI", RSIName):
                self.makeRSI(averageInterval=averageInterval)
                self.relatedColumn[indicatorName].extend([RSIName, "gain", "loss", "averageGain" + str(averageInterval), "averageLoss" + str(averageInterval), "rs" + str(averageInterval)])

            maxName = "max" + str(averageInterval)
            minName = "min" + str(averageInterval)

            self.relatedColumn[indicatorName].extend([maxName, minName])

            self.data[maxName] = self.data[RSIName].rolling(window=averageInterval, min_periods=averageInterval).max()
            self.data[minName] = self.data[RSIName].rolling(window=averageInterval, min_periods=averageInterval).min()
            self.data[indicatorName] = (self.data[RSIName] - self.data[minName]) / (self.data[maxName] - self.data[minName])

            self.addIndicator(indicatorType, indicatorName)
        return str(indicatorName)
    
    def smoothLine(self, indicatorType: str, indicatorName: str, smoothFactor: int):

        indicatorName = str(indicatorName) + "-" + str(smoothFactor)

        if not self.hasIndicator(indicatorType, indicatorName):

            self.data[indicatorName] = self.data.Close.rolling(smoothFactor, min_periods=smoothFactor).mean()

        self.relatedColumn[indicatorName] = [indicatorName]
        return str(indicatorName)
        
    def __str__(self) -> str:
        stringToReturn = "List of Indicator: \n\n"
        for indicatorType in self.indicatorSet:
            stringToReturn += str(indicatorType) + " => "
            for indicator in self.indicatorSet[indicatorType]:
                stringToReturn += str(indicator) + ", "
            stringToReturn += "\n"

        return stringToReturn
    
if __name__ == "__main__":
    import pandas as pd
    import yfinance as yf

    ticker_symbol = "AAPL"
    apple_stock = yf.Ticker(ticker_symbol)
    hist = apple_stock.history(period="1mo")

    indicator = Indicator(hist)

    indicator.makeMACD(2,3,4)
    indicator.makeMACD(2,3,5)
    print(indicator.getRelatedColumn('Signal(2, 3, 4)'))
    print(indicator)
    print(indicator.getData())
    indicator.remove_indicators(indicator.getRelatedColumn('Signal(2, 3, 4)'))
    print(indicator)
    print(indicator.getData())