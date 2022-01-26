import ccxt
from datetime import datetime
import random
import collections
from src.configuration.log_decorator import info_log


class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width count')
    candle_configs = [
        CandleConfig("5m", 60),
        CandleConfig("1h", 24),
        CandleConfig("1d", 60),
    ]

    def fetch_history(self, exchange_name, instrument, candle_width):
        if(candle_width == "random"):
            random_index = random.randrange(len(self.candle_configs))
            candle_config = self.candle_configs[random_index]
        else:
            candle_config, = (
                conf for conf in self.candle_configs
                if conf.width == candle_width)

        candle_data = fetch_OHLCV(
            candle_config.width,
            candle_config.count,
            exchange_name,
            instrument)
        return CandleData(exchange_name, instrument, candle_config.width, candle_data)

    def __repr__(self):
        return '<ccxt crypto exchange>'


def fetch_OHLCV(candle_freq, num_candles, exchange_name, instrument):
    exchange = load_exchange(exchange_name)
    dirty_chart_data = fetch_market_data(
        exchange,
        instrument,
        candle_freq,
        num_candles)
    return list(map(make_matplotfriendly_date, dirty_chart_data))


# @info_log
def fetch_market_data(exchange, instrument, candle_freq, num_candles):
    return exchange.fetchOHLCV(instrument, candle_freq, limit=num_candles)


# @info_log
def load_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)({
        # 'apiKey': '<YOUR API KEY HERE>',
        # 'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()
    return exchange


def make_matplotfriendly_date(element):
    datetime_field = element[0]/1000
    datetime_utc = datetime.utcfromtimestamp(datetime_field)
    return replace_at_index(element, 0, datetime_utc)


def replace_at_index(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)


class CandleData():
    def __init__(self, exchange, instrument, candle_width, candle_data):
        self.exchange = exchange
        self.instrument = instrument
        self.candle_width = candle_width
        self.candle_data = candle_data

    def percentage_change(self):
        current_price = self.last_close()
        start_price = self.start_price()
        return ((current_price - start_price) / current_price) * 100

    def last_close(self):
        return self.candle_data[-1][4]

    def end_price(self):
        return self.candle_data[0][3]

    def start_price(self):
        return self.candle_data[0][4]

    def __repr__(self):
        return f'<{self.instrument} {self.candle_width} candle data>'
