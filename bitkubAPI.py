from bitkub import Bitkub
from datetime import datetime, timedelta

API_KEY = 'YOUR API KEY'
API_SECRET = 'YOUR API SECRET'

bitkub = Bitkub()

period = 60

EMA_Period1 = 25
EMA_period2 = 9


data = bitkub.tradingview(sym='BTC_THB', int=1, frm=(bitkub.servertime()-120), to=bitkub.servertime()-60)
print(data)