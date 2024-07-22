from bitkub import Bitkub
from datetime import datetime, timedelta
import pandas as pd
from Portfolio import portfolio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

bitkub = Bitkub()
data = bitkub.tradingview(sym='BTC_THB', int=1, frm=(bitkub.servertime()-58500*30), to=bitkub.servertime()-10)

def testStochRSI(data):

    df = pd.DataFrame(data)

    for i in range(len(df)):
        if i > 0:
            if df.iloc[i]['c'] > df.iloc[i-1]['c']:
                df.at[i, 'gain'] = df.iloc[i]['c'] - df.iloc[i-1]['c']
                df.at[i, 'loss'] = 0
            elif df.iloc[i]['c'] < df.iloc[i-1]['c']:
                df.at[i, 'loss'] = df.iloc[i-1]['c'] - df.iloc[i]['c']
                df.at[i, 'gain'] = 0
            else:
                df.at[i, 'gain'] = 0
                df.at[i, 'loss'] = 0

    average = 14
    smoothK=4
    smoothD=4

    df['average gain'] = df.gain.ewm(span=average, adjust=False, min_periods=average).mean()
    df['average loss'] = df.loss.ewm(span=average, adjust=False, min_periods=average).mean()
    df['rs'] = df['average gain'] / df['average loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    df['max'] = df['rsi'].rolling(window=average, min_periods=average).max()
    df['min'] = df['rsi'].rolling(window=average, min_periods=average).min()
    df['StochRSI'] = (df['rsi'] - df['min']) / (df['max'] - df['min'])

    df['stochrsi_K'] = df['StochRSI'].ewm(span=smoothK, adjust=False, min_periods=smoothK).mean()
    df['stochrsi_D'] = df['stochrsi_K'].ewm(span=smoothD, adjust=False, min_periods=smoothD).mean()

    port = portfolio()
    port.addFund(10000)
    holdposition = False
    for i in range(1, len(df) - 1):
        if holdposition == False and df.stochrsi_K[i] < 0.1 and df.stochrsi_K[i+1] > 0.1:
            # Buy condition: StochRSI K rises from below 0.1 to above 0.1
            action = port.buy(0.0001, df.o[i+1])
            if action != "do nothing":
                port.addLog('buy', 0.0001, df.o[i+1], str(i+1))
                buyat = df.o[i+1]
                holdposition = True
                pass
        
        if holdposition == True and df.o[i+1]/buyat > 1.006:
            action = port.sell(df.o[i+1])
            if action != "do nothing":
                port.addLog('sell', "all", df.o[i+1], str(i+1))
                holdposition = False

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
    go.Candlestick(open=df['o'], high=df['h'], low=df['l'], close=df['c'], name='Candle Stick'),
    row=1, col=1
)

# Combine stochrsi_K and stochrsi_D into a single Scatter trace
    fig.add_trace(
        go.Scatter(y=df.stochrsi_K, line=dict(color='orange', width=1), name='RSI K'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(y=df.stochrsi_D, line=dict(color='blue', width=1), name='RSI D'),
        row=2, col=1
    )

    fig.show()
    
    return port.getNetValue(), port.getLog()


    

print(testStochRSI(data))