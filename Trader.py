import schedule
from datetime import datetime
import pandas as pd
from bitkub import Bitkub
import plotly.graph_objects as go

bitkub = Bitkub()
period = 60
MA_Period1 = 9
MA_period2 = 55
buffer = 5
timeframe = 1

def job():
    data = bitkub.tradingview(sym='ETH_THB', int=timeframe, frm=(bitkub.servertime()-58500), to=bitkub.servertime()-10)
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=MA_Period1, min_periods=MA_Period1, adjust=False).mean()
    df['EMA2'] = df.c.ewm(span=MA_period2, min_periods=MA_period2, adjust=False).mean()
    df['dif'] = df['EMA1'] - df['EMA2']

    if df['dif'].iloc[-2] <= 0 and df['dif'].iloc[-1] > 0:
        print("buy " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    elif df['dif'].iloc[-2] >= 0 and df['dif'].iloc[-1] < 0:
        print("sell " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    else:
        print("do nothing " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    fig = go.Figure(data=[go.Candlestick(open=df['o'], high=df['h'], low=df['l'], close=df['c'], name='Candle Stick'),
                      go.Scatter(y=df.EMA1, line=dict(color='orange', width=1), name='EMA1'),
                      go.Scatter(y=df.EMA2, line=dict(color='green', width=1), name='EMA2')
                      ])

    fig.show()


def MACD():
    data = bitkub.tradingview(sym='BTC_THB', int=timeframe, frm=(bitkub.servertime()-58500), to=bitkub.servertime()-10)
    average1 = 49
    average2 = 46
    average3 = 49
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=average1, adjust=False, min_periods=average1).mean()
    df['EMA2'] = df.c.ewm(span=average2, adjust=False, min_periods=average2).mean()
    df['MACD'] = df['EMA1'] - df['EMA2']
    df['signal'] = df.MACD.ewm(span=average3, adjust=False, min_periods=average3).mean()
    df['dif'] = df['signal'] - df['MACD']

    if df['dif'].iloc[-2] <= 0 and df['dif'].iloc[-1] > 0:
        print("buy " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    elif df['dif'].iloc[-2] >= 0 and df['dif'].iloc[-1] < 0:
        print("sell " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    else:
        print("do nothing " + str(datetime.now()) + str(df['dif'].iloc[-2]) + str(df['dif'].iloc[-1]))

    fig = go.Figure(data=[
                      go.Scatter(y=df.MACD, line=dict(color='orange', width=1), name='MACD'),
                      go.Scatter(y=df.signal, line=dict(color='green', width=1), name='signal')
                      ])

    fig.show()

    
# schedule.every().hours.at(":00").do(job)
# schedule.every().hours.at(":15").do(job)
# schedule.every().hours.at(":30").do(job)
# schedule.every().hours.at(":45").do(job)

# schedule.every(4).minutes.at(":00").do(job)

schedule.every().minutes.at(":00").do(MACD)

while True:
    schedule.run_pending()