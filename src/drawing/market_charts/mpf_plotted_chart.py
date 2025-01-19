import datetime
from matplotlib import font_manager
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter, DayLocator
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from matplotlib.ticker import EngFormatter


class MplFinanceChart:
    def __init__(self, config, display, files):
        self.config = config
        self.display = display
        self.files = files
        # 🔤 load fonts
        fonts = font_manager.findSystemFonts(fontpaths=files.resource_folder)
        for font_file in fonts:
            font_manager.fontManager.addfont(font_file)

    # 📑 styles overlaid left to right
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

    # 🛶 save plot to image stream
    def write_to_stream(self, stream, chart_data):
        
        # 🎨 chart colours
        mpf_colours = mpf.make_marketcolors(
                alpha=1.0,
                up='black', down='red',
                edge={'up': 'black', 'down': 'red'},  # 'none',
                wick={'up': 'black', 'down': 'red'},
                volume={'up': 'black', 'down': 'red'})

        # 📏 create styles list
        style_files = list(self.get_default_styles(self.config, self.display, self.files))

        # 📏 setup MPF styling
        mpf_style = mpf.make_mpf_style(
            marketcolors=mpf_colours,
            base_mpl_style=style_files,
            mavcolors=['#1f77b4', '#ff7f0e', '#2ca02c'])

        # 📈 settings for chart plot
        plot_args = dict(
            volume=self.config.show_volume(),
            style=mpf_style,
            tight_layout=True,
            figsize=tuple(dim/self.display.dpi() for dim in self.display.size()),
            xrotation=0
        )

        # 🚪 add a line indicating entry price, if configured
        entry = self.config.entry_price()
        if entry != 0:
            plot_args['hlines'] = dict(hlines=[entry], colors=['g'], linestyle='-.')
        # 🖼️ prep chart data frame
        data_frame = chart_data.candle_data

        # 📈 create the chart plot
        fig, ax = mpf.plot(
            data_frame,
            scale_width_adjustment=dict(volume=0.9, candle=0.7, lines=0.05),
            update_width_config=dict(candle_linewidth=0.6),
            returnfig=True,
            type='candle',
            # mav=(10, 20),
            **plot_args
        )
        #plt.rcParams['figure.figsize'] = [8.0, 8.0]
        #plt.rcParams['savefig.dpi'] = display.dpi()
        #plt.subplots_adjust(left=0.0, bottom=0.0, right=1, top=1, wspace=0.1, hspace=0.0)
        #plt.margins(x=0)

        # 🪓 make axes look nicer
        for a in ax:
            # a.set_adjustable('box')
            a.yaxis.set_major_formatter(EngFormatter(sep='', places=1))
            a.xaxis.set_major_locator(AutoDateLocator(minticks = 2, maxticks = 3))
            
            a.autoscale(enable=True, axis="both", tight=True)
            # margin between candles and axes
            a.margins(0.05, 0.2)
            a.xaxis.labelpad = 0
            # a.tick_params(pad=0, axis='both')
            a.locator_params(axis='both', tight=True)
            # remove labels
            _ = a.set_ylabel("")
            _ = a.set_xlabel("")
            a.autoscale_view(True)
            # a.reset_position()
            # _ = a.set_frame_on(False)
            # ✔️ align tick labels inside edges
            if self.config.expand_chart():
                for ylabel in a.yaxis.get_ticklabels():
                    ylabel.set_horizontalalignment('left')
                for xlabel in a.xaxis.get_ticklabels():
                    xlabel.set_verticalalignment('bottom')

        if self.config.expand_chart():
            if(len(ax) == 2):
                ax[0].set_position((0, 0, 1, 1))
                ax[1].set_position((0, 0, 1, 1))
            if(len(ax) == 4):
                ax[3].set_position((0, 0, 1, 0.3))
                ax[2].set_position((0, 0, 1, 0.3))
                ax[0].set_position((0, 0.3, 1, 0.7))
                ax[1].set_position((0, 0.3, 1, 0.7))

        fig.set_tight_layout(True)
        fig.set_constrained_layout_pads(w_pad=0, h_pad=0)

        fig.savefig(
            stream,
            dpi=fig.dpi,
            # bbox_inches='tight',
            pad_inches=0.0,
            transparent=True,
        )
        stream.seek(0)
        plt.close(fig)
