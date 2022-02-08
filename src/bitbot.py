from PIL import Image
import io
from src import crypto_exchanges, stock_exchanges
from src.market_chart import MarketChart
from src.configuration.log_decorator import info_log
from src.chart_overlay import ChartOverlay
from src.kinky import picker as display_picker
from src.network_utils import wait_for_internet_connection


class Cartographer():
    def __init__(self, config, display, files):
        self.market = MarketChart(config, display, files)

    @info_log
    def draw_to(self, chart_data, file_stream):
        self.market.create_plot(chart_data).write_to_stream(file_stream)

    def __repr__(self):
        return '<Cartographer>'


class BitBot():
    def __init__(self, config, files):
        self.config = config
        self.files = files
        self.display = display_picker(config)
        self.plot = Cartographer(self.config, self.display, self.files)

    # 🏛️ stock or crypto exchange
    def market_exchange(self):
        if self.config.stock_symbol():
            return stock_exchanges.Exchange(self.config)
        else:
            return crypto_exchanges.Exchange(self.config)

    @info_log
    def display_chart(self):
        # 📡 await internet connection
        wait_for_internet_connection(self.display.draw_connection_error)
        # 📈 fetch chart data
        chart_data = self.market_exchange().fetch_history()
        # 🖊️ draw the chart on the display
        with io.BytesIO() as file_stream:
            # 🖊️ draw chart plot to image
            self.plot.draw_to(chart_data, file_stream)
            chart_image = Image.open(file_stream)
            # 🖊️ draw overlay on image
            overlay = ChartOverlay(self.config, self.display, chart_data)
            overlay.draw_on(chart_image)
            # 📺 display the image
            self.display.show(chart_image)

    @info_log
    def display_photo(self):
        self.display.show(Image.open(self.config.photo_image_file()))

    def __repr__(self):
        return f'<BitBot inky: {str(self.config.use_inky())}>'
