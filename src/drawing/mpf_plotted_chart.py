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
        mc = mpf.make_marketcolors(
                alpha=1.0,
                up='black', down='red',
                edge={'up': 'black', 'down': 'red'},  # 'none',
                wick={'up': 'black', 'down': 'red'},
                volume={'up': 'black', 'down': 'red'})

        # 📏 setup MLF styling
        s = mpf.make_mpf_style(
            marketcolors=mc,
            base_mpl_style=files.base_style,
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
            style=s,
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
