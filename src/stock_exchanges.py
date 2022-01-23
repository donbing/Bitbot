import yfinance
from datetime import datetime
import matplotlib.dates as mdates

class Exchange():
    def __init__(self, config):
        self.config = config

    def fetch_history(self):
        ticker = yfinance.Ticker(self.config.stock_symbol())
        history =ticker.history(interval='1d', period='1mo')
        return CandleData('1d', history)


def make_matplotfriendly_date(element):
    datetime_field = element[0]/1000
    datetime_utc = datetime.utcfromtimestamp(datetime_field)
    datetime_num = mdates.date2num(datetime_utc)
    return replace_at_index(element, 0, datetime_num)

def replace_at_index(tup, ix, val):
   lst = list(tup)
   lst[ix] = val
   return tuple(lst)
   

class CandleData():
    def __init__(self, candle_width, candle_data):
        self.candle_width = candle_width
        self.candle_data = list(map(make_matplotfriendly_date, candle_data.to_numpy()))
        
    def percentage_change(self):
        return ((self.last_close() - self.start_price()) / self.last_close()) * 100

    def last_close(self):
        return self.candle_data[-1][4]

    def end_price(self):
        return self.candle_data[0][3]

    def start_price(self):
        return self.candle_data[0][4]