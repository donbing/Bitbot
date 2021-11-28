import ccxt
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpl_finance
import matplotlib.dates as mdates
import random

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
    # clean up dates in data
    return list(map(lambda x: replace_at_index(x, 0, mdates.date2num(datetime.utcfromtimestamp(x[0]/1000))), candleData))

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
    #plt.axis('off')
    plt.set_cmap('hot')
    # fill screen
    # fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.monospace"] = "Terminal"
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['patch.antialiased'] = False
    return (fig, ax)

def configure_axes(ax, minor_format, minor_locator, major_format, major_locator):
    ax.set_yticklabels(['{:.1f}'.format(x / 1000) + 'K' for x in ax.get_yticks()])
    #ax.yaxis.set_tick_params(pad=-26, direction="in", width=1, labelsize='7', color='black', which='both', labelcolor='black')
    #ax.xaxis.set_tick_params(pad=-12, direction="in", width=1, labelsize='7', color='black', which='both', labelcolor='black')
    ax.xaxis.set_tick_params(width=1, labelsize='7', color='black', which='both', labelcolor='red')
 
    ax.xaxis.set_minor_locator(minor_format)
    ax.xaxis.set_minor_formatter(minor_locator)
    ax.xaxis.set_major_locator(major_format)
    ax.xaxis.set_major_formatter(major_locator)
    ax.xaxis_date()
    ax.autoscale_view()

class chart_data:
    def __init__(self, config):   
        # 1h 1d 5m 1m
        layouts = [
           # ('1d', timedelta(days=80), 0.01, mdates.DayLocator(interval=7), mdates.DateFormatter('%d'), mdates.MonthLocator(), mdates.DateFormatter('')),
           # ('1h', timedelta(hours=80), 0.005, mdates.HourLocator(interval=4), mdates.DateFormatter('%H'), mdates.DayLocator(), mdates.DateFormatter('')),
           # ('1h', timedelta(hours=24), 0.01, mdates.HourLocator(interval=1), mdates.DateFormatter(''), mdates.HourLocator(interval=4), mdates.DateFormatter('%I %p')),
            ('5m', timedelta(minutes=5*60), 0.0005, mdates.MinuteLocator(interval=10), mdates.DateFormatter(''), mdates.HourLocator(interval=1), mdates.DateFormatter('%I:%M'))
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
        self.fig.savefig(stream, dpi=self.fig.dpi)