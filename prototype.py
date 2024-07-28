from Core.Indicator import Indicator
from Core.Strategy import Strategy
from Core.Backtestr import Backtestr

import streamlit as st
import yfinance as yf

data = yf.download()

Backtestr = Backtestr(data)
Indicator = Indicator(data)
Strategy = Strategy(data)

# test for macd cross over strategy with config (12, 26, 9)

MACDLine, SignalLine = Indicator.makeMACD(firstAverageInterval=12, secondAverageInterval=26, signalAverageInterval=9)
Strategy.useCrossOver(MACDLine, SignalLine)
Backtestr.runTest()
