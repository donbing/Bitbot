import ccxt
from datetime import datetime
import random
import collections
from src.configuration.log_decorator import info_log
from ccxt.base.errors import BadSymbol
import logging


class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width count')
    candle_configs = [
        CandleConfig("5m", 40),
        CandleConfig("1h", 40),
        CandleConfig("1d", 40),
    ]

    def __init__(self, config):
        self.config = config
        self.name = self.config.exchange_name()

    def fetch_history(self):
        configred_candle_width = self.config.candle_width()
        instrument = self.config.instrument_name()

        if(configred_candle_width == "random"):
            random_index = random.randrange(len(self.candle_configs))
            candle_config = self.candle_configs[random_index]
        else:
            candle_config, = (
                conf for conf in self.candle_configs
                if conf.width == configred_candle_width)

        candle_data = fetch_OHLCV(
            candle_config.width,
            candle_config.count,
            self.config.exchange_name(),
            self.config.instrument_name(),
            self.config.chart_since()
        )
        return CandleData(instrument, candle_config.width, candle_data)

    def __repr__(self):
        return '<ccxt crypto exchange>'


def fetch_OHLCV(candle_freq, num_candles, exchange_name, instrument, since):
    exchange = load_exchange(exchange_name)
    dirty_chart_data = fetch_market_data(
        exchange,
        instrument,
        candle_freq,
        num_candles,
        since)
    clean_chart_data = map(make_matplotfriendly_date, dirty_chart_data)
    return list(clean_chart_data)


@info_log
def fetch_market_data(exchange, instrument, candle_freq, num_candles, since):
    try:
        return exchange.fetchOHLCV(
            instrument,
            candle_freq,
            limit=num_candles,
            since=since and exchange.parse8601(since))
    except BadSymbol:
        logging.warning(f'"{instrument}" is not available')
        return []

@info_log
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
    def __init__(self, instrument, candle_width, candle_data):
        self.instrument = instrument
        self.candle_width = candle_width
        self.candle_data = candle_data

    def percentage_change(self):
        current_price = self.last_close()
        start_price = self.start_price()
        return ((current_price - start_price) / current_price) * 100

    def last_close(self):
        return self.candle_data[-1][4]

    def start_price(self):
        return self.candle_data[0][4]

    def __repr__(self):
        return f'<{self.instrument} {self.candle_width} candle data>'
