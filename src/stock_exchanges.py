import yfinance
import collections
import random
from datetime import datetime, timedelta
from src.configuration.log_decorator import info_log


class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width duration')
    candle_configs = [
        CandleConfig('1mo', timedelta(weeks=4*24)),
        CandleConfig('1h', timedelta(hours=40)),
        CandleConfig('1wk', timedelta(weeks=60)),
        CandleConfig('3mo', timedelta(weeks=12*24))
    ]

    def fetch_history(self, instrument, candle_width):
        ticker = yfinance.Ticker(instrument)
        candle_config = self.select_candle_config(candle_width)

        end_date = datetime.utcnow()
        start_date = end_date - candle_config.duration

        history = self.get_stock_history(
            ticker,
            candle_config.width,
            start_date,
            end_date)

        return CandleData(instrument, candle_width, history, ticker)

    @info_log
    def get_stock_history(self, ticker, candle_width, start_date, end_date):
        return ticker.history(
            interval=candle_width,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"))

    def select_candle_config(self, candle_width):
        if(candle_width == "random"):
            return self.get_random_candle_config()
        else:
            candle_config = self.get_candle_config_matching(candle_width)
            return candle_config

    def get_candle_config_matching(self, configred_candle_width):
        candle_config, = (
                conf for conf in self.candle_configs
                if conf.width == configred_candle_width
            )
        return candle_config

    def get_random_candle_config(self):
        randomised_index = random.randrange(len(self.candle_configs))
        new_var = self.candle_configs[randomised_index]
        return new_var

    def __repr__(self):
        return '<yfinance stock Exchange>'


def make_matplotfriendly_date(element):
    datetime_field = element[0]
    return replace_at_index(element, 0, datetime_field)


def replace_at_index(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)


class CandleData():
    def __init__(self, instrument, candle_width, candle_data, ticker):
        self.instrument = f'{instrument}/{ticker.info["currency"]}'
        self.candle_width = candle_width
        candle_data.reset_index(level=0, inplace=True)
        self.candle_data = self.clean_candle_data(candle_data)

    def clean_candle_data(self, candle_data):
        return list(map(make_matplotfriendly_date, candle_data.to_numpy()))

    def percentage_change(self):
        current_price = self.last_close()
        starting_price = self.start_price()
        return ((current_price - starting_price) / current_price) * 100

    def last_close(self):
        return float(self.candle_data[-1][4])

    def end_price(self):
        return float(self.candle_data[0][3])

    def start_price(self):
        return float(self.candle_data[0][4])

    def __repr__(self):
        return f'<{self.instrument} {self.candle_width} candle data>'
