import schedule
from datetime import datetime
import pandas as pd
from bitkub import Bitkub

bitkub = Bitkub()
period = 60
MA_Period1 = 7
MA_period2 = 25
buffer = 10
timeframe = 1

def job():
    data = bitkub.tradingview(sym='BTC_THB', int=timeframe, frm=(bitkub.servertime()-60*timeframe* (MA_period2+buffer)), to=bitkub.servertime())
    df = pd.DataFrame(data)
    df['EMA1'] = df.c.ewm(span=MA_Period1, min_periods=MA_Period1, adjust=False).mean()
    df['EMA2'] = df.c.ewm(span=MA_period2, min_periods=MA_period2, adjust=False).mean()

    if df['EMA1'].iloc[-3] < df['EMA2'].iloc[-3] and df['EMA1'].iloc[-2] > df['EMA2'].iloc[-2]:
        print("buy " + str(datetime.now()))

    elif df['EMA1'].iloc[-3] > df['EMA2'].iloc[-3] and df['EMA1'].iloc[-2] < df['EMA2'].iloc[-2]:
        print("sell " + str(datetime.now()))

    else:
        print("do nothing " + str(datetime.now()))

# schedule.every().hours.at(":05").do(job)
# schedule.every().hours.at(":10").do(job)
# schedule.every().hours.at(":15").do(job)

# schedule.every(4).minutes.at(":00").do(job)

schedule.every().minutes.at(":00").do(job)

while True:
    schedule.run_pending()