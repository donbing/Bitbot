import ccxt, datetime, random, collections
from datetime import datetime
import matplotlib.dates as mdates
from src.log_decorator import info_log

class Exchange():
    CandleConfig = collections.namedtuple('CandleConfig', 'width count')
    candle_configs = [ CandleConfig("5m", 60), CandleConfig("1h", 24), CandleConfig("1h", 40), CandleConfig("1d", 60) ]
    
    def __init__(self, config):
        self.config = config
    
    def fetch_history(self):
        candle_config = self.candle_configs[random.randrange(len(self.candle_configs))]
        candle_data = fetch_OHLCV_chart_data(
            candle_config.width, 
            candle_config.count,
            self.config.exchange_name(), 
            self.config.instrument_name()
        )
        return CandleData(candle_config.width, candle_data)

def fetch_OHLCV_chart_data(candle_freq, num_candles, exchange_name, instrument):
    exchange = load_exchange(exchange_name)
    dirty_chart_data = fetch_market_data(exchange, instrument, candle_freq, num_candles)
    return list(map(make_matplotfriendly_date, dirty_chart_data))

@info_log
def fetch_market_data(exchange, instrument, candle_freq, num_candles):
    return exchange.fetchOHLCV(instrument, candle_freq, limit=num_candles)

@info_log
def load_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)({ 
        #'apiKey': '<YOUR API KEY HERE>',
        #'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()
    return exchange

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
        self.candle_data = candle_data
        
    def percentage_change(self):
        return ((self.last_close() - self.start_price()) / self.last_close()) * 100

    def last_close(self):
        return self.candle_data[-1][4]

    def end_price(self):
        return self.candle_data[0][3]

    def start_price(self):
        return self.candle_data[0][4]