import ccxt, datetime
from datetime import datetime
import matplotlib.dates as mdates
from src.log_decorator import info_log

def fetch_OHLCV_chart_data(candleFreq, num_candles, exchange_name, instrument):
    exchange = load_exchange(exchange_name)
    dirty_chart_data = get_chart_data(exchange, instrument, candleFreq, num_candles)
    clean_chart_data = replace_dates(dirty_chart_data)
    return clean_chart_data

def replace_dates(chart_data):
    return list(map(make_matplotfriendly_date, chart_data))

@info_log
def get_chart_data(exchange, instrument, candleFreq, num_candles):
    return exchange.fetchOHLCV(instrument, candleFreq, limit=num_candles)

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
   