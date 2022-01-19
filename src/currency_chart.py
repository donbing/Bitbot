import matplotlib, mpl_finance, ccxt, random, tzlocal, logging, pathlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from src import price_humaniser
from os.path import join as pjoin

matplotlib.use('Agg')

curdir = pathlib.Path(__file__).parent.resolve()
base_style = pjoin(curdir, '../config/', 'base.mplstyle') 
inset_style = pjoin(curdir, '../config/', 'inset.mplstyle') 
default_style = pjoin(curdir, '../config/', 'default.mplstyle') 

import matplotlib.font_manager as font_manager
fonts_path = pjoin(curdir, '../src/resources') #/', 'Pixel12x10.ttf'
font_files = font_manager.findSystemFonts(fontpaths=fonts_path)
custom_font_manager = font_manager.fontManager

# log font names 
# logging.info([f.name for f in matplotlib.font_manager.fontManager.ttflist])

for font_file in font_files:
    custom_font_manager.addfont(font_file)

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
   
def get_chart_plot(display, config):
    # apply global base style
    plt.style.use(base_style)
    # may not need to do this anymore
    plt.rcParams['timezone'] = tzlocal.get_localzone_name()
    # select mpl style
    stlye = inset_style if config["display"]["expanded_chart"] == 'true' else default_style
    plt.tight_layout()
    # scope styles to just this plot
    with plt.style.context(stlye):
        fig, ax = plt.subplots(figsize=(display.WIDTH / 100, display.HEIGHT / 100), dpi=100)
        # currency amount uses custom formatting 
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(price_humaniser.format_scale_price))
        return (fig, ax)

# locate/format x axis tick labels
def configure_axis_format(ax, minor_label_locator, minor_label_format, major_label_locator,  major_label_format):
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
    noop_date_formatter = plt.NullFormatter()
    layouts = [
        ('1d', 60, 0.01, mdates.DayLocator(bymonthday=range(1,31,7)), noop_date_formatter, mdates.MonthLocator(), mdates.DateFormatter('%b')),
        ('1h', 40, 0.005, mdates.HourLocator(byhour=range(0,23,4)), noop_date_formatter, mdates.DayLocator(), mdates.DateFormatter('%a %d %b')),
        ('1h', 24, 0.01, mdates.HourLocator(interval=1), noop_date_formatter, mdates.HourLocator(interval=4), mdates.DateFormatter('%-I.%p')),
        ('5m', 60, 0.0005, mdates.MinuteLocator(byminute=[0,30]), noop_date_formatter, mdates.HourLocator(interval=1), mdates.DateFormatter('%-I.%p'))
    ]
    def __init__(self, config, display):
        # create MPL plot
        self.fig, ax = get_chart_plot(display, config)

        # select a random chart layout 
        layout = self.layouts[random.randrange(len(self.layouts))]
        self.candle_width = layout[0]
        self.num_candles = layout[1]

        # get market data
        exchange_name = config["currency"]["exchange"]
        instrument = config["currency"]["instrument"]
        self.candleData = fetch_OHLCV_chart_data(self.candle_width, self.num_candles, exchange_name, instrument)

        # apply chosen layouts axis labelling to plot 
        configure_axis_format(ax, layout[3], layout[4], layout[5], layout[6])

        # draw candles to MPL plot
        mpl_finance.candlestick_ohlc(ax, self.candleData, width=layout[2], colorup='black', colordown='red') 

    def percentage_change(self):
        return ((self.last_close() - self.start_price()) / self.last_close()) * 100

    def last_close(self):
        return self.candleData[-1][4]

    def end_price(self):
        return self.candleData[0][3]

    def start_price(self):
        return self.candleData[0][4]

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
        plt.close(self.fig)
