from bitkub import Bitkub
from datetime import datetime, timedelta
import pandas as pd
from Portfolio import portfolio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

bitkub = Bitkub()
data = bitkub.tradingview(sym='BTC_THB', int=15, frm=(bitkub.servertime()-58500*60), to=bitkub.servertime()-10)

def macd(data):
    df = pd.DataFrame(data)

    average1 = 12
    average2 = 14
    average3 = 9
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
    df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
    df['MACD'] = df['EMA1'] - df['EMA2']
    df['signal'] = df.MACD.ewm(span=average3, adjust=False, min_periods=average3).mean()
    df['Dif'] = df['signal'] - df['MACD']
    port = portfolio()
    port.addFund(10000)
    holdposition = False
    for i in range(1, len(df) - 1):
        if holdposition == False and (df.Dif[i-1] < 0) and (df.Dif[i] > 0):
            action = port.buy(0.001, df.o[i+1])
            if action != "do nothing":
                port.addLog('buy', 0.001, df.o[i+1], str(i+1))
                holdposition = True
                buyat = df.o[i+1]

        if holdposition == True and (df.o[i+1]/buyat >= 1.01):
            action = port.sell(df.o[i+1])
            if action != "do nothing":
                port.addLog('sell', "all", df.o[i+1], str(i+1))

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Candlestick(open=df['o'], high=df['h'], low=df['l'], close=df['c'], name='Candle Stick'),
        row=1, col=1
    )

    # Combine stochrsi_K and stochrsi_D into a single Scatter trace
    fig.add_trace(
        go.Scatter(y=df.MACD, line=dict(color='orange', width=1), name='RSI K'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(y=df.signal, line=dict(color='blue', width=1), name='RSI D'),
        row=2, col=1
    )

    fig.show()
    return port.getNetValue(), port.getLog()


print(macd(data))