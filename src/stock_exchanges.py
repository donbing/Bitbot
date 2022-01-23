import yfinance
from datetime import datetime
import matplotlib.dates as mdates

class Exchange():
    interval='1mo'
    period='5y'
    def __init__(self, config):
        self.config = config

    def fetch_history(self):
        instrument = self.config.stock_symbol()
        ticker = yfinance.Ticker(instrument)
        history =ticker.history(interval=self.interval, period=self.period)
        return CandleData(instrument, self.interval, history)

def make_matplotfriendly_date(element):
    datetime_field = element[0]
    datetime_num = mdates.date2num(datetime_field)
    return replace_at_index(element, 0, datetime_num)

def replace_at_index(tup, ix, val):
   lst = list(tup)
   lst[ix] = val
   return tuple(lst)
   

class CandleData():
    def __init__(self, instrument, candle_width, candle_data):
        self.instrument = instrument
        self.candle_width = candle_width
        candle_data.reset_index(level=0, inplace=True)
        self.candle_data = list(map(make_matplotfriendly_date, candle_data.to_numpy()))
        
    def percentage_change(self):
        return ((self.last_close() - self.start_price()) / self.last_close()) * 100

    def last_close(self):
        return self.candle_data[-1][4]

    def end_price(self):
        return self.candle_data[0][3]

    def start_price(self):
        return self.candle_data[0][4]