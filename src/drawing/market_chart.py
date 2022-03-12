import matplotlib
import tzlocal
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
from mplfinance.original_flavor import candlestick_ohlc, volume_overlay
from src.drawing import price_humaniser

matplotlib.use('Agg')
local_tz = tzlocal.get_localzone()

price_formatter = matplotlib.ticker.FuncFormatter(
    price_humaniser.format_scale_price
)


# ☝️ single instance for lifetime of app
class MarketChart:
    def __init__(self, config, display, files):
        self.config = config
        self.display = display
        self.files = files
        fonts = font_manager.findSystemFonts(fontpaths=files.resource_folder)
        for font_file in fonts:
            font_manager.fontManager.addfont(font_file)

    def create_plot(self, chart_data):
        return PlottedChart(self.config, self.display, self.files, chart_data)


class PlottedChart:
    layouts = {
        '3mo': (20, mdates.YearLocator(), mdates.YearLocator(1), mdates.DateFormatter('%Y', local_tz)),
        '1mo': (0.01, mdates.MonthLocator(), mdates.YearLocator(1), mdates.DateFormatter('%Y', local_tz)),
        '1d': (0.01, mdates.DayLocator(bymonthday=range(1, 31, 7)), mdates.MonthLocator(), mdates.DateFormatter('%b', local_tz)),
        '1h': (0.005, mdates.HourLocator(byhour=range(0, 23, 4)), mdates.DayLocator(), mdates.DateFormatter('%a %d %b', local_tz)),
        "5m": (0.0005, mdates.MinuteLocator(byminute=[0, 30]), mdates.HourLocator(interval=1), mdates.DateFormatter('%-I.%p', local_tz)),
    }

    def __init__(self, config, display, files, chart_data):
        self.candle_width = chart_data.candle_width
        # 🖨️ create MPL plot
        self.fig, ax = self.create_chart_figure(config, display, files)
        # 📐 find suiteable layout for timeframe
        layout = self.layouts[self.candle_width]
        # ➖ locate/format x axis ticks for chosen layout
        ax[0].xaxis.set_minor_locator(layout[1])
        ax[0].xaxis.set_minor_formatter(plt.NullFormatter())
        ax[0].xaxis.set_major_locator(layout[2])
        ax[0].xaxis.set_major_formatter(layout[3])
        # 💲currency amount uses custom formatting
        ax[0].yaxis.set_major_formatter(price_formatter)

        self.plot_chart(config, layout, ax, chart_data.candle_data)

    def plot_chart(self, config, layout, ax, candle_data):
        # ✒️ draw candles to MPL plot
        candlestick_ohlc(ax[0], candle_data, colorup='green', colordown='red', width=layout[0])
        # ✒️ draw volumes to MPL plot
        if config.show_volume():
            ax[1].yaxis.set_major_formatter(price_formatter)
            _, opens, _, _, closes, volumes = list(zip(*candle_data))
            volume_overlay(ax[1], opens, closes, volumes, colorup='white', colordown='red', width=1)
            self.fig.subplots_adjust(bottom=0.01)

    def get_default_styles(self, config, display, files):
        if config.expand_chart():
            yield files.expanded_style
        else:
            yield files.default_style
        if display.size()[0] < 300:
            yield files.small_screen_style

    def create_chart_figure(self, config, display, files):
        # 📏 apply global base style
        plt.style.use(files.base_style)
        num_plots = 2 if config.show_volume() else 1
        heights = [4, 1] if config.show_volume() else [1]
        plt.tight_layout()
        # 📏 select mpl style
        stlyes = list(self.get_default_styles(config, display, files))
        # 📏 scope styles to just this plot
        with plt.style.context(stlyes):
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
