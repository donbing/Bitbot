import ccxt
import random
import collections
import pandas as pd
import logging
from src.configuration.log_decorator import info_log
from ccxt.base.errors import BadSymbol
from src.exchanges.CandleData import CandleData

# 🪙 CCXT based crypto exchange client
class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width count')
    candle_configs = [
        CandleConfig("5m", 40),
        CandleConfig("1h", 40),
        CandleConfig("1d", 40),
    ]

    def fetch_history(self, config):
        configred_candle_width = config.candle_width()
        if(configred_candle_width == "random"):
            random_index = random.randrange(len(self.candle_configs))
            candle_config = self.candle_configs[random_index]
        else:
            candle_config, = (
                conf for conf in self.candle_configs
                if conf.width == configred_candle_width)

        instrument = config.instrument_name()
        chart_start = config.chart_since()

        exchange = load_exchange(config.exchange_name())

        dirty_chart_data = fetch_market_data(
            exchange,
            instrument,
            candle_config.width,
            candle_config.count,
            chart_start)
        
        candle_data = parse_to_dataframe(dirty_chart_data)

        return CandleData(instrument, candle_config.width, candle_data)

    def __repr__(self):
        return '<ccxt crypto exchange>'


def parse_to_dataframe(candle_data):
    data_frame = pd.DataFrame(candle_data)
    data_frame.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    data_frame.index = pd.DatetimeIndex(data_frame['Date'], dtype="datetime64[ms]")
    return data_frame

@info_log
def fetch_market_data(exchange, instrument, candle_freq, num_candles, since):
    try:
        return exchange.fetchOHLCV(
            instrument,
            candle_freq,
            limit=num_candles,
            since=since and exchange.parse8601(since.strftime('%Y-%m-%dT%H:%M:%S.%f%z')))
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
