import matplotlib, random, tzlocal, pathlib
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
from src import price_humaniser, chart_data_fetcher
from os.path import join as pjoin

matplotlib.use('Agg')

curdir = pathlib.Path(__file__).parent.resolve()

config_path = pjoin(curdir, '../config/') 
base_style = pjoin(config_path, 'base.mplstyle') 
inset_style = pjoin(config_path, 'inset.mplstyle') 
default_style = pjoin(config_path, 'default.mplstyle') 

fonts_path = pjoin(curdir, '../src/resources')
font_files = font_manager.findSystemFonts(fontpaths=fonts_path)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

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

# single instance for lifetime of app
class crypto_chart:
    layouts = [
        ('1d', 60, 0.01,    mdates.DayLocator(bymonthday=range(1,31,7)),    plt.NullFormatter(), mdates.MonthLocator(),             mdates.DateFormatter('%b')),
        ('1h', 40, 0.005,   mdates.HourLocator(byhour=range(0,23,4)),       plt.NullFormatter(), mdates.DayLocator(),               mdates.DateFormatter('%a %d %b')),
        ('1h', 24, 0.01,    mdates.HourLocator(interval=1),                 plt.NullFormatter(), mdates.HourLocator(interval=4),    mdates.DateFormatter('%-I.%p')),
        ('5m', 60, 0.0005,  mdates.MinuteLocator(byminute=[0,30]),          plt.NullFormatter(), mdates.HourLocator(interval=1),    mdates.DateFormatter('%-I.%p'))
    ]
    def __init__(self, config, display):   
        self.config = config
        self.display = display
    
    def createChart(self):
        return charted_plot(self.config, self.display, self.get_random_layout())

    def get_random_layout(self):
        return self.layouts[random.randrange(len(self.layouts))]

class charted_plot:
    def __init__(self, config, display, layout):
        # create MPL plot
        self.fig, ax = get_chart_plot(display, config)
        self.candle_width = layout[0]
        num_candles = layout[1]

        # get market data
        self.candleData = chart_data_fetcher.fetch_OHLCV_chart_data(
            self.candle_width, 
            num_candles,
            config["currency"]["exchange"], 
            config["currency"]["instrument"])

        # locate/format x axis ticks for chosen layout
        ax.xaxis.set_minor_locator(layout[3])
        ax.xaxis.set_minor_formatter(layout[4])
        ax.xaxis.set_major_locator(layout[5])
        ax.xaxis.set_major_formatter(layout[6])

        # draw candles to MPL plot
        candlestick_ohlc(ax, self.candleData, width=layout[2], colorup='black', colordown='red') 

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
