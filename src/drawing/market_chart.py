import matplotlib
import tzlocal
import matplotlib.font_manager as font_manager
from src.drawing.legacy_mpf_plotted_chart import PlottedChart
from src.drawing.mpf_plotted_chart import NewPlottedChart

matplotlib.use('Agg')
local_tz = tzlocal.get_localzone()


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
        return NewPlottedChart(self.config, self.display, self.files, chart_data)

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

            # 📏 align price tick labels for expanded chart
            if(config.expand_chart()):
                ax1.set_yticklabels(ax1.get_yticklabels(), ha='left')

            if config.show_volume():
                with plt.style.context(files.volume_style):
                    ax2 = fig.add_subplot(gs[1], zorder=0)

            return (fig, (ax1, ax2))

    def write_to_stream(self, stream):
        self.fig.savefig(stream, dpi=self.fig.dpi, pad_inches=0)
        stream.seek(0)
        plt.close(self.fig)
