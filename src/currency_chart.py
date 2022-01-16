import matplotlib, ccxt, mpl_finance, random, tzlocal, logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
from datetime import datetime
from src import price_humaniser

matplotlib.use('Agg')

def fetch_OHLCV_chart_data(candleFreq, num_candles, exchange_name, instrument):
   
    # create exchange wrapper and load market data
    exchange = getattr(ccxt, exchange_name)({ 
        #'apiKey': '<YOUR API KEY HERE>',
        #'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()

    logging.debug("Supported exchanges: \n" + "\n".join(ccxt.exchanges))
    logging.debug("Supported time frames: \n" + "\n".join(exchange.timeframes))
    logging.debug("Supported markets: \n" + "\n".join(exchange.markets.keys()))

    # fetch the chart data
    logging.info("Fetching "+ str(num_candles) + " " + candleFreq + " " + instrument + " candles from " + exchange_name)

    candleData = exchange.fetchOHLCV(instrument, candleFreq, limit=num_candles)
    cleaned_candle_data = list(map(lambda x: make_matplotfriendly_date(x), candleData))

    logging.debug("Candle data: " + "\n".join(map(str, cleaned_candle_data)))
    logging.info("Fetched " + str(len(cleaned_candle_data)) + " candles")

    return cleaned_candle_data

def make_matplotfriendly_date(element):
    datetime_field = element[0]/1000
    datetime_utc = datetime.utcfromtimestamp(datetime_field)
    datetime_num = mdates.date2num(datetime_utc)
    return replace_at_index(element, 0, datetime_num)

def replace_at_index(tup, ix, val):
   lst = list(tup)
   lst[ix] = val
   return tuple(lst)

def get_chart_plot(display):
    # pyplot setup for 4X3 100dpi screen
    fig, ax = plt.subplots(figsize=(display.WIDTH / 100, display.HEIGHT / 100), dpi=100)
    # fills screen with graph
    # fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
    
    # set default attempt at mpl font / style
    print(font_manager.fontManager.ttflist)
    matplotlib.rcParams["font.sans-serif"] = "04b03"
    matplotlib.rcParams["font.family"] = "sans-serif"
    matplotlib.rcParams['font.weight'] = 'light'  

    plt.rcParams['text.hinting_factor'] = 1
    plt.rcParams['text.hinting'] = 'native'
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['patch.antialiased'] = False
    plt.rcParams['timezone'] = tzlocal.get_localzone_name()

    # human readable short-format y-axis currency amount
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(price_humaniser.format_scale_price))
    
    # bring labels closer to the axis
    ax.tick_params(axis='x', pad=4)
    ax.tick_params(axis='y', pad=1)

    # style axis ticks
    ax.tick_params(labelsize='12', color='red', which='both', labelcolor='black')

    # hide the top/right border
    ax.spines['bottom'].set_color('red')
    ax.spines['left'].set_color('red')
    ax.spines['bottom'].set_linewidth(0.8)
    ax.spines['left'].set_linewidth(0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    return (fig, ax)

# locate/format x axis tick labels
def configure_axes(ax, minor_label_locator, minor_label_format, major_label_locator,  major_label_format):
    ax.xaxis.set_minor_locator(minor_label_locator)
    ax.xaxis.set_minor_formatter(minor_label_format)
    ax.xaxis.set_major_locator(major_label_locator)
    ax.xaxis.set_major_formatter(major_label_format)

# single instance for lifetime of app
class crypto_chart:
    def __init__(self, config, display):   
        self.config = config
        self.display = display
    
    def createChart(self):
        return charted_plot(self.config, self.display)

class charted_plot:
    layouts = [
        ('1d', 60, 0.01, mdates.DayLocator(interval=7), mdates.DateFormatter(''), mdates.MonthLocator(), mdates.DateFormatter('%b')),
        ('1h', 40, 0.005, mdates.HourLocator(interval=4), mdates.DateFormatter(''), mdates.DayLocator(), mdates.DateFormatter('%a %d %b')),
        ('1h', 24, 0.01, mdates.HourLocator(interval=1), mdates.DateFormatter(''), mdates.HourLocator(interval=4), mdates.DateFormatter('%I%p')),
        ('5m', 60, 0.0005, mdates.MinuteLocator(interval=30), mdates.DateFormatter(''), mdates.HourLocator(interval=1), mdates.DateFormatter('%I%p'))
    ]
    def __init__(self, config, display):
        # create MPL plot
        self.fig, ax = get_chart_plot(display)
        # select a random chart layout 
        self.layout = self.layouts[random.randrange(len(self.layouts))]
        self.candle_width = self.layout[0]
        # apply chosen layouts axis labelling to plot 
        configure_axes(ax, self.layout[3], self.layout[4], self.layout[5], self.layout[6])

        exchange_name = config["currency"]["exchange"]
        instrument = config["currency"]["instrument"]
        # get market data for layout
        self.candleData = fetch_OHLCV_chart_data(self.layout[0], self.layout[1], exchange_name, instrument)
        # draw candles to MPL plot
        mpl_finance.candlestick_ohlc(ax, self.candleData, width=self.layout[2], colorup='black', colordown='red') 

    def last_close(self):
        return self.candleData[-1][4]

    def end_price(self):
        return self.candleData[0][3]

    def start_price(self):
        return self.candleData[0][4]

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
