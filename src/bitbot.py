from PIL import Image
import io, socket, time
from src import crypto_exchanges, kinky
from src.market_chart import MarketChart
from src.log_decorator import info_log
from src.chart_overlay import ChartOverlay

class Cartographer():
    def __init__(self, config, display, files, chart_data):
        self.plot = MarketChart(config, display, files).create_plot(chart_data)
    
    @info_log
    def draw_to(self, file_stream):
        self.plot.write_to_stream(file_stream)

    def __repr__(self):
        return 'Cartographer'
        
class BitBot():
    def __init__(self, config, files):
        self.config = config
        self.files = files
        # select inky display or file output (nice for testing)
        self.display = kinky.Inker(self.config) if self.config.use_inky() else kinky.Disker()
        # initialise exchange
        self.exchange = crypto_exchanges.Exchange(config)

    def run(self):
        # await internet connection
        self.wait_for_internet_connection(self.display)
        # fetch chart data
        chart_data = self.exchange.fetch_random()
        # draw the chart on the display
        with io.BytesIO() as file_stream:
            # draw chart to image
            chart_plot = Cartographer(self.config, self.display, self.files, chart_data)
            chart_plot.draw_to(file_stream)
            chart_image = Image.open(file_stream)
            # draw overlay on image   
            ChartOverlay(self.config, self.display, chart_data).draw_on(chart_image)
            # display the image
            self.display.show(chart_image)
    
    @info_log
    def wait_for_internet_connection(self, display):
        # test if internet is available
        def network_connected(hostname="google.com"):
            try:
                host = socket.gethostbyname(hostname)
                socket.create_connection((host, 80), 2).close()
                return True
            except:
                time.sleep(1)
            return False
            
        connection_error_shown = False
        while network_connected() == False:
            # draw error message if not already drawn
            if connection_error_shown == False:
                connection_error_shown = True
                display.draw_connection_error()
            time.sleep(10)

    def __repr__(self):
        return 'BitBot inky:' + str(self.config.use_inky())