import matplotlib.pyplot as plt
import numpy
import mplfinance as mpf
import pandas as pd
from matplotlib.ticker import EngFormatter


class NewPlottedChart:
    def __init__(self, config, display, files, chart_data):
        self.candle_width = chart_data.candle_width

        # 🖼️ prep chart data frame
        data_frame = pd.DataFrame(chart_data.candle_data)
        data_frame = data_frame.drop([6, 7], axis=1, errors='ignore')
        data_frame.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
       #  data_frame.index = pd.to_datetime(data_frame['date']) # pd.DatetimeIndex(data_frame['date'].astype('datetime64[ms]'))
        data_frame.index = pd.DatetimeIndex(data_frame['date'])

        # 🎨 chart colours
        mpf_colours = mpf.make_marketcolors(
                alpha=1.0,
                up='black', down='red',
                edge={'up': 'black', 'down': 'red'},  # 'none',
                wick={'up': 'black', 'down': 'red'},
                volume={'up': 'black', 'down': 'red'})

        # 📏 create styles list
        style_files = list(self.get_default_styles(config, display, files))

        # 📏 setup MLF styling
        mpf_style = mpf.make_mpf_style(
            marketcolors=mpf_colours,
            base_mpl_style=style_files,
            mavcolors=['#1f77b4', '#ff7f0e', '#2ca02c'])

        # 📈 settings for chart plot
        kwargs = dict(
            volume=config.show_volume(),
            style=mpf_style,
            tight_layout=True,
            figsize=tuple(dim/100 for dim in display.size()),
            xrotation=0,
            datetime_format=self.date_format(data_frame),
        )

        # 🚪 add a line indicating entry price, if configured
        entry = config.entry_price()
        if entry != 0:
            kwargs['hlines'] = dict(hlines=[entry], colors=['g'], linestyle='-.')

        # 📈 create the chart plot
        self.fig, ax = mpf.plot(
            data_frame,
            scale_width_adjustment=dict(volume=0.9, candle=0.7, lines=0.05),
            update_width_config=dict(candle_linewidth=0.6),
            returnfig=True,
            type='candle',
            # mav=(10, 20),
            **kwargs
        )

        plt.subplots_adjust(left=0.0, bottom=0.0, right=1, top=1, wspace=0.1, hspace=0.0)
        plt.margins(x=0)

        # 🪓 make axes look nicer
        for a in ax:
            # a.set_adjustable('box')
            a.yaxis.set_major_formatter(EngFormatter(sep=''))
            a.autoscale(enable=True, axis="both", tight=True)
            # margin between candles and axes
            a.margins(0.05, 0.2)
            # a.xaxis.labelpad = 0
            # a.tick_params(pad=0, axis='both')
            a.locator_params(axis='both', tight=True)
            # remove labels
            _ = a.set_ylabel("")
            _ = a.set_xlabel("")
            a.autoscale_view(True)
            # a.reset_position()

            # _ = a.set_frame_on(False)
            # a.use_sticky_edges = False
            # expand the axes!!
            # TODO: this needs to deal with the volume axes :(
            if config.expand_chart():
                for ylabel in a.yaxis.get_ticklabels():
                    ylabel.set_horizontalalignment('left')
                for xlabel in a.xaxis.get_ticklabels():
                    xlabel.set_verticalalignment('bottom')
                plt.gca().set_position((0, 0, 1, 1))

        # self.fig.set_tight_layout(True)
        # self.fig.set_constrained_layout_pads(w_pad=0, h_pad=0)

    # 📑 styles overid left to right
    def get_default_styles(self, config, display, files):
        yield files.base_style
        yield files.default_style

        small_display = self.is_small_display(display)
        if small_display:
            yield files.small_screen_style

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
            return '%b%d'
        elif(candle_time_delta <= numpy.timedelta64(4, 'W')):
            return '%y/%b'
        elif(candle_time_delta <= numpy.timedelta64(16, 'W')):
            return '%y/%b'
        else:
            return '%b'

    # 🛶 save plot to image stream
    def write_to_stream(self, stream):
        self.fig.savefig(
            stream,
            dpi=self.fig.dpi,
            # bbox_inches='tight',
            pad_inches=0.0,
            transparent=True,
        )
        stream.seek(0)
        plt.close(self.fig)
