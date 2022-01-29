from dataclasses import dataclass
from flask import Flask, render_template, request, jsonify, Response
import requests
import matplotlib
import tzlocal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import EngFormatter
import matplotlib.font_manager as font_manager
from mplfinance.original_flavor import candlestick_ohlc, volume_overlay
import pathlib
from os.path import join as pjoin


matplotlib.use('Agg')
local_timezone = tzlocal.get_localzone()


class Files:
    def __init__(self):
        current_dir = pathlib.Path(__file__).parent.resolve()
        self.base_dir = pjoin(current_dir, 'resources/')

        self.base_style = pjoin(self.base_dir, 'base.mplstyle')
        self.inset_style = pjoin(self.base_dir, 'inset.mplstyle')
        self.default_style = pjoin(self.base_dir, 'default.mplstyle')
        self.volume_style = pjoin(self.base_dir, 'volume.mplstyle')
        self.fonts_folder = pjoin(self.base_dir, 'resources/')
        self.logging_ini = pjoin(self.base_dir, 'logging.ini')


@dataclass
class Config:
    def expand_chart(self):
        return False

    def show_volume(self):
        return False


@dataclass
class Display:
    WIDTH: int
    HEIGHT: int
    DPI: int


files = Files()
config = Config()

for font_file in font_manager.findSystemFonts(fontpaths=files.fonts_folder):
    font_manager.fontManager.addfont(font_file)


class PlottedChart:
    layouts = {
        '3mo': (20,     mdates.YearLocator(),                           plt.NullFormatter(),    mdates.YearLocator(1),             mdates.DateFormatter('%Y'), local_timezone),
        '1mo': (0.01,   mdates.MonthLocator(),                          plt.NullFormatter(),    mdates.YearLocator(1),             mdates.DateFormatter('%Y'), local_timezone),
        '1d': (0.01,    mdates.DayLocator(bymonthday=range(1, 31, 7)),  plt.NullFormatter(),    mdates.MonthLocator(),             mdates.DateFormatter('%b'), local_timezone),
        '1h': (0.005,   mdates.HourLocator(byhour=range(0, 23, 4)),     plt.NullFormatter(),    mdates.DayLocator(),               mdates.DateFormatter('%a %d %b', local_timezone)),
        "5m": (0.0005,  mdates.MinuteLocator(byminute=[0, 30]),         plt.NullFormatter(),    mdates.HourLocator(interval=1),    mdates.DateFormatter('%-I.%p', local_timezone)),
    }

    def __init__(self, config, display, files, chart_data):
        self.candle_width = chart_data.candle_width
        # 🖨️ create MPL plot
        self.fig, ax = self.create_chart_figure(
            display,
            files,
            config.expand_chart(),
            config.show_volume())
        # 📐 find suiteable layout for timeframe
        layout = self.layouts[self.candle_width]
        # ➖ locate/format x axis ticks for chosen layout
        ax[0].xaxis.set_minor_locator(layout[1])
        ax[0].xaxis.set_minor_formatter(layout[2])
        ax[0].xaxis.set_major_locator(layout[3])
        ax[0].xaxis.set_major_formatter(layout[4])
        # 💲currency amount uses custom formatting
        ax[0].yaxis.set_major_formatter(EngFormatter)
        # 🗓️ clean up dates in raw price data
        candles = self.replace_dates(chart_data.candle_data)

        self.plot_chart(layout, ax, candles, config.show_volume())

    def replace_dates(self, candle_data):
        return [(mdates.date2num(row[0]),) + row[1:] for row in candle_data]

    def plot_chart(self, layout, ax, price_data, show_volume):
        # ✒️ draw candles to MPL plot
        candlestick_ohlc(
            ax[0],
            price_data,
            colorup='green',
            colordown='red',
            width=layout[0])
        # ✒️ draw volumes to MPL plot
        if show_volume:
            ax[1].yaxis.set_major_formatter(EngFormatter)
            dates, opens, highs, lows, closes, volumes = list(zip(*price_data))
            volume_overlay(
                ax[1],
                opens,
                closes,
                volumes,
                colorup='white',
                colordown='red',
                width=1)

    def create_chart_figure(self, display, files, expand_chart, show_volume):
        # 📏 apply global base style
        plt.style.use(files.base_style)
        # 📏 select mpl style
        stlye = files.inset_style if expand_chart else files.default_style
        num_plots = 2 if show_volume else 1
        heights = [4, 1] if show_volume else [1]
        plt.tight_layout()
        # 📏 scope styles to just this plot
        with plt.style.context(stlye):
            fig = plt.figure(figsize=(display.WIDTH / 100, display.HEIGHT / 100))
            gs = fig.add_gridspec(num_plots, hspace=0, height_ratios=heights)
            ax1 = fig.add_subplot(gs[0], zorder=1)
            ax2 = None
            if show_volume:
                with plt.style.context(files.volume_style):
                    ax2 = fig.add_subplot(gs[1], zorder=0)

            return (fig, (ax1, ax2))

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
        stream.seek(0)
        plt.close(self.fig)


app = Flask(__name__)


def process_prices(price_data, settings):
    PlottedChart(
        config,
        Display(settings.width, settings.height, settings.dpi),
        files,
        price_data)
    return''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        content = request.json or request.form
        data_url = content['data_url']
        target_url = content['target_url']
        settings = content['settings']
        price_data = jsonify(requests.get(data_url))
        chart_image = process_prices(price_data, settings)
        post = requests.post(target_url, chart_image)
    return Response(status=200)


if(__name__ == '__main__'):
    app.run(debug=False, host='0.0.0.0')
