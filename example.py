from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr
import yfinance as yf

stock = yf.Ticker("BTC-USD")
data = stock.history(period="5y", interval="1d").reset_index(drop=True)

indicator = Indicator(data)
strategy = Strategy(data)

firstLine, secondLine = indicator.makeMACD(firstAverageInterval=12, secondAverageInterval=27, signalAverageInterval=9)
strategy.useCrossOver(action="buy", logic=True, firstLine=firstLine, secondLine=secondLine)
strategy.useCrossOver(action="sell", logic=True, firstLine=firstLine, secondLine=secondLine)
backtestr = Backtestr(data, "BTC-USD")

netValue = backtestr.runTest(100000, 1)
print(netValue)
