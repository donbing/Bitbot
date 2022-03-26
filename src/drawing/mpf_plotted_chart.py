import matplotlib
import matplotlib.pyplot as plt
import numpy
import mplfinance as mpf
import pandas as pd
from matplotlib.ticker import EngFormatter

matplotlib.use('Agg')


class NewPlottedChart:
    def __init__(self, config, display, files, chart_data):
        self.candle_width = chart_data.candle_width

        # 🖼️ prep chart data frame
        data_frame = pd.DataFrame(
            chart_data.candle_data,
            columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        data_frame.index = pd.DatetimeIndex(data_frame['date'])

        # 🎨 chart colours
        mpf_colours = mpf.make_marketcolors(
                alpha=1.0,
                up='black', down='red',
                edge={'up': 'black', 'down': 'red'},  # 'none',
                wick={'up': 'black', 'down': 'red'},
                volume={'up': 'black', 'down': 'red'})

        # 📏 MPF doesnt support multiple styles, so we hack them into rcparams
        style_files = list(self.get_default_styles(config, display, files))

        # 📏 setup MLF styling
        mpf_style = mpf.make_mpf_style(
            marketcolors=mpf_colours,
            base_mpl_style=style_files,
            mavcolors=['#1f77b4', '#ff7f0e', '#2ca02c'])

        # 📈 create the chart plot
        self.fig, ax = mpf.plot(
            data_frame,
            scale_width_adjustment=dict(volume=0.9, candle=0.7, lines=0.05),
            update_width_config=dict(candle_linewidth=0.6),
            returnfig=True,
            type='candle',
            # mav=(10, 20),
            # volume=True,
            style=mpf_style,
            tight_layout=True,
            figsize=tuple(dim/100 for dim in display.size()),
            xrotation=0,
            datetime_format=self.date_format(data_frame),
        )

        # 🪓 make axes look nicer
        for a in ax:
            a.yaxis.set_major_formatter(EngFormatter(sep=''))
            a.autoscale(enable=True, axis="x", tight=True)
            a.autoscale(enable=True, axis="y", tight=True)
            a.margins(0.05, 0.2)
            _ = a.set_ylabel("")
            _ = a.set_xlabel("")

    # 📑 styles overide each other left to right?
    def get_default_styles(self, config, display, files):
        small_display = self.is_small_display(display)

        if small_display:
            yield files.small_screen_style
        yield files.default_style

        if config.expand_chart():
            yield files.expanded_style
            if small_display:
                yield files.small_expanded_style

    def is_small_display(self, display):
        small_display = display.size()[0] < 300
        return small_display

    # 🕐 format for date axis labels
    def date_format(self, df):
        candle_time_delta = df.index.values[1] - df.index.values[0]
        if(candle_time_delta <= numpy.timedelta64(1, 'h')):
            return '%H:%M'
        elif(candle_time_delta <= numpy.timedelta64(1, 'D')):
            return '%b.%d'
        else:
            return '%b'

    # 🛶 save plot to image stream
    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
        stream.seek(0)
        plt.close(self.fig)
