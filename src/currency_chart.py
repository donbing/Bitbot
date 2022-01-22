import matplotlib, random, tzlocal, pathlib
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
volume_style = pjoin(config_path, 'volume.mplstyle') 

fonts_path = pjoin(curdir, '../src/resources')
font_files = font_manager.findSystemFonts(fontpaths=fonts_path)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

local_timezone = tzlocal.get_localzone()

# single instance for lifetime of app
class crypto_chart:
    layouts = [
        ('1d', 60, 0.01,    mdates.DayLocator(bymonthday=range(1,31,7)),    plt.NullFormatter(), mdates.MonthLocator(),             mdates.DateFormatter('%b'), local_timezone),
        ('1h', 40, 0.005,   mdates.HourLocator(byhour=range(0,23,4)),       plt.NullFormatter(), mdates.DayLocator(),               mdates.DateFormatter('%a %d %b', local_timezone)),
        ('1h', 24, 0.01,    mdates.HourLocator(interval=1),                 plt.NullFormatter(), mdates.HourLocator(interval=4),    mdates.DateFormatter('%-I.%p', local_timezone)),
        ('5m', 60, 0.0005,  mdates.MinuteLocator(byminute=[0,30]),          plt.NullFormatter(), mdates.HourLocator(interval=1),    mdates.DateFormatter('%-I.%p', local_timezone))
    ]
    def __init__(self, config, display):   
        self.config = config
        self.display = display
    
    def createChart(self):
        return charted_plot(self.config, self.display, self.get_random_layout())

    def get_random_layout(self):
        return self.layouts[random.randrange(len(self.layouts))]

class charted_plot:
    def get_chart_plot(self, display, config):
        # apply global base style
        plt.style.use(base_style)
        # select mpl style
        stlye = inset_style if self.expand_chart() else default_style
        num_plots =  2 if self.show_volume() else 1
        heights = [4,1] if self.show_volume() else [1]
        plt.tight_layout()
        # scope styles to just this plot
        with plt.style.context(stlye):
            fig = plt.figure(figsize=(display.WIDTH / 100, display.HEIGHT / 100))
            gs = fig.add_gridspec(num_plots, hspace=0, height_ratios=heights)
            ax1 = fig.add_subplot(gs[0], zorder = 0)
            ax2 = None
            if self.show_volume():
                with plt.style.context(volume_style):
                    ax2 = fig.add_subplot(gs[1], zorder = 1)

            return (fig,(ax1,ax2))

    def __init__(self, config, display, layout):
        # get market data
        self.candle_width = layout[0]
        self.config = config
        num_candles = layout[1]
        candle_size = layout[2]
        self.candleData = chart_data_fetcher.fetch_OHLCV_chart_data(
            self.candle_width, 
            num_candles,
            self.exchange_name(), 
            self.instrument_name())

        # create MPL plot
        self.fig, ax = self.get_chart_plot(display, config)

        # locate/format x axis ticks for chosen layout
        ax[0].xaxis.set_minor_locator(layout[3])
        ax[0].xaxis.set_minor_formatter(layout[4])
        ax[0].xaxis.set_major_locator(layout[5])
        ax[0].xaxis.set_major_formatter(layout[6])

        # currency amount uses custom formatting 
        ax[0].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(price_humaniser.format_scale_price))

        # ax[1].xaxis.set_minor_locator(layout[3])
        # ax[1].xaxis.set_minor_formatter(layout[4])
        # ax[1].xaxis.set_major_locator(layout[5])
        # ax[1].xaxis.set_major_formatter(layout[6])

        from mplfinance.original_flavor import candlestick_ohlc, volume_overlay, plot_day_summary2_ohlc, candlestick2_ohlc
        
        # draw candles to MPL plot
        candlestick_ohlc(ax[0], self.candleData, colorup='green', colordown='red', width=candle_size) 
        # draw volumes to MPL plot
        if self.show_volume():
            ax[1].yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(price_humaniser.format_scale_price))
            dates, opens, highs, lows, closes, volumes = list(zip(*self.candleData))
            volume_overlay(ax[1], opens, closes, volumes, colorup='green', colordown='red', width=1)

    def expand_chart(self):
        return self.config["display"]["expanded_chart"] == 'true'
    
    def show_volume(self):
        return self.config["display"]["show_volume"] == 'true'

    def exchange_name(self):
        return self.config["currency"]["exchange"]

    def instrument_name(self):
        return self.config["currency"]["instrument"]

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
