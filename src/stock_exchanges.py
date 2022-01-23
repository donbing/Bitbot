import yfinance
import collections
import random
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from src.log_decorator import info_log


class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width duration')
    candle_configs = [
        CandleConfig('1mo', timedelta(weeks=4*24)),
        CandleConfig('1h', timedelta(hours=40)),
        CandleConfig('1wk', timedelta(weeks=60)),
        CandleConfig('3mo', timedelta(weeks=12*24))
    ]

    def __init__(self, config):
        self.config = config

    def fetch_history(self):
        instrument = self.config.stock_symbol()
        ticker = yfinance.Ticker(instrument)
        candle_config = self.select_candle_config()
        end_date = datetime.utcnow()
        start_date = end_date - candle_config.duration
        history = self.get_stock_history(ticker, candle_config.width, start_date, end_date)
        return CandleData(instrument, candle_config.width, history, ticker)

    @info_log
    def get_stock_history(self, ticker, candle_width, start_date, end_date):
        return ticker.history(
            interval=candle_width,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"))

    def select_candle_config(self):
        configred_candle_width = self.config.candle_width()
        if(configred_candle_width == "random"):
            return self.candle_configs[random.randrange(len(self.candle_configs))]
        else:
            candle_config, = (conf for conf in self.candle_configs if conf.width == configred_candle_width)
            return candle_config


def make_matplotfriendly_date(element):
    datetime_field = element[0]
    datetime_num = mdates.date2num(datetime_field)
    return replace_at_index(element, 0, datetime_num)


def replace_at_index(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)


class CandleData():
    def __init__(self, instrument, candle_width, candle_data, ticker):
        self.instrument = f'{instrument}/{ticker.info["currency"]}'
        self.candle_width = candle_width
        candle_data.reset_index(level=0, inplace=True)
        self.candle_data = list(map(make_matplotfriendly_date, candle_data.to_numpy()))

    def percentage_change(self):
        return ((self.last_close() - self.start_price()) / self.last_close()) * 100

    def last_close(self):
        return float(self.candle_data[-1][4])

    def end_price(self):
        return float(self.candle_data[0][3])

    def start_price(self):
        return float(self.candle_data[0][4])
    
    def __repr__(self):
        return f'<{self.instrument} {self.candle_width} candle data>'
