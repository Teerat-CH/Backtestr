from bitkub import Bitkub
from datetime import datetime, timedelta
import pandas as pd
from Portfolio import portfolio

bitkub = Bitkub()
data = bitkub.tradingview(sym='BTC_THB', int=60*24, frm=bitkub.servertime()-86400*1000, to=bitkub.servertime())

def findbestEMA():
    maxReturn = 0
    average1Max = 0
    average2Max = 0
    for average1 in range(1,120,1):
        for average2 in range(1,120,1):
            df = pd.DataFrame(data)
            df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
            df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
            df['Dif'] = df['EMA1'] - df['EMA2']
            port = portfolio()
            port.addFund(10000)
            for i in range(1, len(df) - 1):
                if (df.Dif[i-1] < 0) and (df.Dif[i] > 0):
                    action = port.buy(0.001, df.o[i+1])
                    if action != "do nothing":
                        port.addLog('buy', 0.001, df.o[i+1], str(i+1))
                if (df.Dif[i-1] > 0) and (df.Dif[i] < 0):
                    action = port.sell(df.o[i+1])
                    if action != "do nothing":
                        port.addLog('sell', "all", df.o[i+1], str(i+1))

            if port.getNetValue() > maxReturn:
                maxReturn = port.getNetValue()
                average1Max = average1
                average2Max = average2
    return average1Max, average2Max, maxReturn

def testEMA():
    average1 = 51
    average2 = 12
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
    df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
    df['Dif'] = df['EMA1'] - df['EMA2']
    port = portfolio()
    port.addFund(10000)
    for i in range(1, len(df) - 1):
        if (df.Dif[i-1] < 0) and (df.Dif[i] > 0):
            action = port.buy(0.001, df.o[i+1])
            if action != "do nothing":
                port.addLog('buy', 0.001, df.o[i+1], str(i+1))
        if (df.Dif[i-1] > 0) and (df.Dif[i] < 0):
            action = port.sell(df.o[i+1])
            if action != "do nothing":
                port.addLog('sell', "all", df.o[i+1], str(i+1))
    return port.getNetValue()

def testMACD():
    average1 = 20
    average2 = 12
    average3 = 12
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
    df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
    df['MACD'] = df['EMA1'] - df['EMA2']
    df['signal'] = df.MACD.ewm(span=average3, adjust=False, min_periods=average3).mean()
    df['Dif'] = df['signal'] - df['MACD']
    port = portfolio()
    port.addFund(10000)
    for i in range(1, len(df) - 1):
        if (df.Dif[i-1] < 0) and (df.Dif[i] > 0):
            action = port.buy(0.001, df.o[i+1])
            if action != "do nothing":
                port.addLog('buy', 0.001, df.o[i+1], str(i+1))
        if (df.Dif[i-1] > 0) and (df.Dif[i] < 0):
            action = port.sell(df.o[i+1])
            if action != "do nothing":
                port.addLog('sell', "all", df.o[i+1], str(i+1))
    return port.getNetValue()

def findbestMACD():
    maxReturn = 0
    average1Max = 0
    average2Max = 0
    average3Max = 0
    for average1 in range(10,50,2):
        for average2 in range(10,50,2):
            for average3 in range(10,50,2):
                df = pd.DataFrame(data)
                df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
                df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
                df['MACD'] = df['EMA1'] - df['EMA2']
                df['signal'] = df.MACD.ewm(span=average3, adjust=False, min_periods=average3).mean()
                df['Dif'] = df['signal'] - df['MACD']
                port = portfolio()
                port.addFund(10000)
                for i in range(1, len(df) - 1):
                    if (df.Dif[i-1] < 0) and (df.Dif[i] > 0):
                        action = port.buy(0.001, df.o[i+1])
                        if action != "do nothing":
                            port.addLog('buy', 0.001, df.o[i+1], str(i+1))
                    if (df.Dif[i-1] > 0) and (df.Dif[i] < 0):
                        action = port.sell(df.o[i+1])
                        if action != "do nothing":
                            port.addLog('sell', "all", df.o[i+1], str(i+1))

                if port.getNetValue() > maxReturn:
                    maxReturn = port.getNetValue()
                    average1Max = average1
                    average2Max = average2
                    average3Max =average3
    return average1Max, average2Max, average3Max, maxReturn


print(testMACD())