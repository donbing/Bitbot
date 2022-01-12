
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.use('Agg')
import ccxt
from datetime import datetime, timedelta, timezone
import mpl_finance
import random
import tzlocal
import logging

def fetch_OHLCV_chart_data(candleFreq, num_candles, config):
   
    exchange_name = config["currency"]["exchange"]
    instrument = config["currency"]["instrument"]
    # create exchange wrapper based on user exchange config
    exchange = getattr(ccxt, exchange_name)({ 
        #'apiKey': '<YOUR API KEY HERE>',
        #'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()

    logging.debug("Supported exchanges: \n" + "\n".join(ccxt.exchanges))
    logging.debug("Supported time frames: \n" + "\n".join(exchange.timeframes))
    logging.debug("Supported markets: \n" + "\n".join(exchange.markets.keys()))
    logging.info("Fetching "+ str(num_candles) + " " + candleFreq + " of " + instrument + " candles from: " + exchange_name)

    candleData = exchange.fetchOHLCV(instrument, candleFreq, limit=num_candles)
    cleaned_candle_data = list(map(lambda x: clean_element(x), candleData))
    logging.debug("Candle data: " + "\n".join(map(str, cleaned_candle_data)))

    return cleaned_candle_data

def clean_element(element):
    datetime_field = element[0]/1000
    dateime_utc = datetime.fromtimestamp(datetime_field)
    dateime_num = mdates.date2num(dateime_utc)
    return replace_at_index(element, 0, dateime_num)

def replace_at_index(tup, ix, val):
   lst = list(tup)
   lst[ix] = val
   return tuple(lst)

def make_sell_order(instrument):
    order = exchange.create_order(instrument, 'Market', 'sell', 2.0, None)
    logging.info(order['side'] + ':' + str(order['amount']) + '@' + str(order['price']))

#DejaVu Sans Mono, Bitstream Vera Sans Mono, Andale Mono, Nimbus Mono L, Courier New, Courier, Fixed, Terminal, monospace
def get_plot(display):
    # pyplot setup for 4X3 100dpi screen
    fig, ax = plt.subplots(figsize=(display.WIDTH / 100, display.HEIGHT / 100), dpi=100)
    # fills screen with graph
    #fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.monospace"] = "Terminal"
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['patch.antialiased'] = False
    plt.rcParams['timezone'] = tzlocal.get_localzone_name()
    return (fig, ax)

def human_format(num, pos):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def configure_axes(ax, minor_format, minor_locator, major_format, major_locator):
    # style axis ticks
    ax.tick_params(labelsize='8', color='red', which='both', labelcolor='black')
    # hide the top/right border
    ax.spines['bottom'].set_color('red')
    ax.spines['left'].set_color('red')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # format/locate x axis labels
    ax.xaxis.set_minor_locator(minor_format)
    #ax.xaxis.set_minor_formatter(minor_locator)
    ax.xaxis.set_major_locator(major_format)
    ax.xaxis.set_major_formatter(major_locator)
    # human readable short-format y-axis currency amount
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(human_format))
    # use current timezone for date formating?
    ax.xaxis_date(tz=datetime.now(timezone.utc).astimezone().tzinfo)
    # this will hide the axis/labels
    ax.autoscale_view(tight=False)

class chart_data:
    def __init__(self, config, display):   
        layouts = [
            ('1d', 60, 0.01, mdates.DayLocator(interval=7), mdates.DateFormatter('%d'), mdates.MonthLocator(), mdates.DateFormatter('%B')),
            ('1h', 40, 0.005, mdates.HourLocator(interval=4), mdates.DateFormatter(''), mdates.DayLocator(), mdates.DateFormatter('%a %d %b')),
            ('1h', 24, 0.01, mdates.HourLocator(interval=1), mdates.DateFormatter(''), mdates.HourLocator(interval=4), mdates.DateFormatter('%I %p')),
            ('5m', 60, 0.0005, mdates.MinuteLocator(interval=30), mdates.DateFormatter(''), mdates.HourLocator(interval=1), mdates.DateFormatter('%I%p'))
        ]
        
        self.layout = layouts[random.randrange(len(layouts))]
        self.candle_width = self.layout[0]
        self.fig, ax = get_plot(display)
        self.candleData = fetch_OHLCV_chart_data(self.layout[0], self.layout[1], config)
        mpl_finance.candlestick_ohlc(ax, self.candleData, width=self.layout[2], colorup='black', colordown='red') 
        configure_axes(ax, self.layout[3], self.layout[4], self.layout[5], self.layout[6])

    def last_close(self):
        return self.candleData[-1][4]

    def end_price(self):
        return self.candleData[0][3]

    def start_price(self):
        return self.candleData[0][4]

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)