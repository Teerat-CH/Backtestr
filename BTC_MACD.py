import time

def timed(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute")
        return result
    return wrapper

from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr
import yfinance as yf

maxReturn = 0
maxFirstAverage = 0
maxSecondAverage = 0
maxSignalAverage = 0

stock = yf.Ticker("BTC-USD")

iter = 0

for firstAverage in range(1, 50, 2):
    for secondAverage in range(1, 50, 2):
        if firstAverage != secondAverage:
            data = stock.history(period="5y", interval="1d").reset_index(drop=True)
            for signalAverage in range(1, 50, 2):

                iter += 1

                indicator = Indicator(data)
                strategy = Strategy(data)

                firstLine, secondLine = indicator.makeMACD(firstAverageInterval=firstAverage, secondAverageInterval=secondAverage, signalAverageInterval=signalAverage)
                strategy.useCrossOver(action="buy", logic=True, firstLine=firstLine, secondLine=secondLine)
                strategy.useCrossOver(action="sell", logic=True, firstLine=firstLine, secondLine=secondLine)
                backtestr = Backtestr(data, "BTC-USD")

                netValue = backtestr.runTest(1000, 0.01)
                if netValue > maxReturn:
                    maxReturn = netValue
                    maxFirstAverage = firstAverage
                    maxSecondAverage = secondAverage
                    maxSignalAverage = signalAverage

                print(netValue, firstAverage, secondAverage, signalAverage, iter)

print("Maximum return = " + str(maxReturn))
print("Maximum first average = " + str(maxFirstAverage))
print("Maximum second average = " + str(maxSecondAverage))
print("Maximum signal average = " + str(maxSignalAverage))
