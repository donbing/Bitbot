import matplotlib
import tzlocal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
from mplfinance.original_flavor import candlestick_ohlc, volume_overlay
from src.drawing import price_humaniser

matplotlib.use('Agg')
local_timezone = tzlocal.get_localzone()

price_formatter = matplotlib.ticker.FuncFormatter(
    price_humaniser.format_scale_price
)


# ☝️ single instance for lifetime of app
class MarketChart:
    def __init__(self, config, display, files):
        self.config = config
        self.display = display
        self.files = files
        for font_file in font_manager.findSystemFonts(fontpaths=files.resource_folder):
            font_manager.fontManager.addfont(font_file)

    def create_plot(self, chart_data):
        return PlottedChart(self.config, self.display, self.files, chart_data)


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
        self.fig, ax = self.create_chart_figure(config, display, files)
        # 📐 find suiteable layout for timeframe
        layout = self.layouts[self.candle_width]
        # ➖ locate/format x axis ticks for chosen layout
        ax[0].xaxis.set_minor_locator(layout[1])
        ax[0].xaxis.set_minor_formatter(layout[2])
        ax[0].xaxis.set_major_locator(layout[3])
        ax[0].xaxis.set_major_formatter(layout[4])
        # 💲currency amount uses custom formatting
        ax[0].yaxis.set_major_formatter(price_formatter)

        self.plot_chart(config, layout, ax, chart_data.candle_data)

    def plot_chart(self, config, layout, ax, candle_data):
        # ✒️ draw candles to MPL plot
        candlestick_ohlc(ax[0], candle_data, colorup='green', colordown='red', width=layout[0])
        # ✒️ draw volumes to MPL plot
        if config.show_volume():
            ax[1].yaxis.set_major_formatter(price_formatter)
            dates, opens, highs, lows, closes, volumes = list(zip(*candle_data))
            volume_overlay(ax[1], opens, closes, volumes, colorup='white', colordown='red', width=1)
            self.fig.subplots_adjust(bottom=0.01)

    def create_chart_figure(self, config, display, files):
        # 📏 apply global base style
        plt.style.use(files.base_style)
        # 📏 select mpl style
        stlye = files.expanded_style if config.expand_chart() else files.default_style
        num_plots = 2 if config.show_volume() else 1
        heights = [4, 1] if config.show_volume() else [1]
        plt.tight_layout()
        # 📏 scope styles to just this plot
        with plt.style.context(stlye):
            display_width, display_height = display.size()
            fig = plt.figure(figsize=(display_width / 100, display_height / 100))
            gs = fig.add_gridspec(num_plots, hspace=0, height_ratios=heights)
            ax1 = fig.add_subplot(gs[0], zorder=1)
            ax2 = None
            if config.show_volume():
                with plt.style.context(files.volume_style):
                    ax2 = fig.add_subplot(gs[1], zorder=0)

            return (fig, (ax1, ax2))

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
        stream.seek(0)
        plt.close(self.fig)
