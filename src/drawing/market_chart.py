import matplotlib
import tzlocal
import matplotlib.font_manager as font_manager


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
