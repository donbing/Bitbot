import ccxt
from datetime import datetime, timedelta, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpl_finance
import matplotlib.dates as mdates
import random
import tzlocal

def fetch_OHLCV_chart_data(candleFreq, chartDuration, config):
    startdate = datetime.utcnow() - chartDuration
    exchange = config["currency"]["exchange"]
    instrument = config["currency"]["instrument"]
    print('fetching data from ' + exchange)
    # create exchange wrapper based on user exchange config
    exchange = getattr(ccxt, exchange)({ 
        #'apiKey': '<YOUR API KEY HERE>',
        #'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()
    #print(" supported exchanges: " + str(cccxt.exchanges))
    #print(" supported time frames: " + str(exchange.timeframes))
    #print(" supported markets: " + " ".join(exchange.markets.keys()))

    candleData = exchange.fetchOHLCV(instrument, candleFreq, limit=1000, params={'startTime':startdate})
    
    return list(map(lambda x: clean_element(x), candleData))

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
    print(order['side'] + ':' + str(order['amount']) + '@' + str(order['price']))

#DejaVu Sans Mono, Bitstream Vera Sans Mono, Andale Mono, Nimbus Mono L, Courier New, Courier, Fixed, Terminal, monospace
def get_plot():
    # pyplot setup for 4X3 100dpi screen
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
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
    def __init__(self, config):   
        layouts = [
            ('1d', timedelta(days=60), 0.01, mdates.DayLocator(interval=7), mdates.DateFormatter('%d'), mdates.MonthLocator(), mdates.DateFormatter('%B')),
            ('1h', timedelta(hours=40), 0.005, mdates.HourLocator(interval=4), mdates.DateFormatter(''), mdates.DayLocator(), mdates.DateFormatter('%D')),
            ('1h', timedelta(hours=24), 0.01, mdates.HourLocator(interval=1), mdates.DateFormatter(''), mdates.HourLocator(interval=4), mdates.DateFormatter('%I %p')),
            ('5m', timedelta(minutes=5*60), 0.0005, mdates.MinuteLocator(interval=30), mdates.DateFormatter(''), mdates.HourLocator(interval=1), mdates.DateFormatter('%I%p'))
        ]
        
        self.layout = layouts[random.randrange(len(layouts))]
        self.candle_width = self.layout[0]
        self.fig, ax = get_plot()
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