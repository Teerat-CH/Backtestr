from bitkub import Bitkub
from datetime import datetime, timedelta
import pandas as pd

API_KEY = 'YOUR API KEY'
API_SECRET = 'YOUR API SECRET'

bitkub = Bitkub()

period = 60

MA_Period1 = 7
MA_period2 = 25
buffer = 10
timeframe = 1


data = bitkub.tradingview(sym='BTC_THB', int=timeframe, frm=(bitkub.servertime()-60*timeframe* (MA_period2+buffer)), to=bitkub.servertime())
df = pd.DataFrame(data)
df['EMA1'] = df.c.ewm(span=MA_Period1, min_periods=MA_Period1, adjust=False).mean()
df['EMA2'] = df.c.ewm(span=MA_period2, min_periods=MA_period2, adjust=False).mean()

if df['EMA1'].iloc[-3] < df['EMA2'].iloc[-3] and df['EMA1'].iloc[-2] > df['EMA2'].iloc[-2]:
    print("buy")

elif df['EMA1'].iloc[-3] > df['EMA2'].iloc[-3] and df['EMA1'].iloc[-2] < df['EMA2'].iloc[-2]:
    print("buy")

else:
    print("do nothing")
    
print(data)