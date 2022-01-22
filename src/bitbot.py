from datetime import datetime
from PIL import Image, ImageDraw
import io, random, socket, time
from src import chart_data_fetcher, price_humaniser, currency_chart, kinky
from src.log_decorator import info_log

# test if internet is available
def network_connected(hostname="google.com"):
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2).close()
        return True
    except:
        time.sleep(1)
    return False

# select image area with the most white pixels
def least_intrusive_position(img, possibleTextPositions):
    rgb_im = img.convert('RGB')
    height_of_section = 60
    ordredByAveColour = sorted(possibleTextPositions, key=lambda item: (count_white_pixels(*item, height_of_section, rgb_im), item[0]))
    return ordredByAveColour[-1]

# count the white pixels in an area of the image
def count_white_pixels(x, y, n, image):
    count = 0
    for s in range(x, x+(n*3)+1):
        for t in range(y, y+n+1):
            pix = image.getpixel((s, t))
            count += 1 if pix == (255,255,255) else 0
    return count

@info_log
def wait_for_internet_connection(display):
    connection_error_shown = False
    while network_connected() == False:
        # draw error message if not already drawn
        if connection_error_shown == False:
            connection_error_shown = True
            display.draw_connection_error()
        time.sleep(10)

def flatten(t):
    return [item for sublist in t for item in sublist]

class cartographer():
    def __init__(self, config, display, files):
        self.config = config 
        self.display = display
        # initialise chart for current display/config
        self.chart = currency_chart.crypto_chart(self.config, self.display, files)
    
    @info_log
    def draw_chart(self, chart_data, file_stream):
        chartdata = self.chart.createChart(chart_data)
        # write chart plot to stream and open as a PIL image
        chartdata.write_to_stream(file_stream)
        file_stream.seek(0)
        return Image.open(file_stream)

class ChartEditor():
    possible_title_positions = flatten(map(lambda y: map(lambda x: (x, y), range(60, 200, 10)), [6, 200]))
    def __init__(self, config, display):
        self.config = config
        self.display = display
    
    def overlay_on(self, chart_image, chart_data):
        # handles drawing over our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # find some empty space in the image to place our text
        selectedArea = least_intrusive_position(chart_image, self.possible_title_positions)
        # draw configured overlay
        if self.config.overlay_type() == "2":
            self.draw_overlay2(draw_plot_image, chart_data, selectedArea)
        else:
            self.draw_overlay1(draw_plot_image, chart_data, selectedArea)
        return chart_image

    # add a time if configured
    def draw_current_time(self, draw_plot_image):
        if self.config.show_timestamp() == 'true':
            formatted_time = datetime.now().strftime("%b %-d %-H:%M")
            text_width, text_height = draw_plot_image.textsize(formatted_time, self.display.tiny_font)
            draw_plot_image.text((self.display.WIDTH - text_width - 1, self.display.HEIGHT - text_height - 2), formatted_time, 'black', self.display.tiny_font)

    # add a border if configured
    def draw_border(self, draw_plot_image):
        border_type = self.config.border_type()
        if border_type != 'none':
            draw_plot_image.rectangle([(0, 0), (self.display.WIDTH -1, self.display.HEIGHT-1)], outline=border_type)

    def draw_overlay1(self, draw_plot_image, chartdata, selectedArea):
        # draw instrument / candle width
        title = self.config.instrument_name() + ' (' + chartdata.candle_width + ') '
        draw_plot_image.text(selectedArea, title, 'black', self.display.title_font)
        # draw % change text
        title_width, title_height = draw_plot_image.textsize(title, self.display.title_font)
        change = ((chartdata.last_close() - chartdata.start_price()) / chartdata.last_close())*100
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0]+title_width, selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)
        # draw current price text
        price = price_humaniser.format_title_price(chartdata.last_close())
        draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', self.display.price_font)
        # select some random comment depending on price action
        if random.random() < 0.5:
            direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
            messages=self.config.get_price_action_comments(direction)
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)
        
        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)

    def draw_overlay2(self, draw_plot_image, chartdata, selectedArea):
        # draw instrument name
        title = self.config.configured_instrument()
        title_width, title_height = draw_plot_image.textsize(title, self.display.medium_font)
        txt=Image.new('RGBA', (title_width, title_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), title, 'black', self.display.medium_font)
        w=txt.rotate(270, expand=True)
        title_paste_pos = (self.display.WIDTH-title_height - 2, int((self.display.HEIGHT - title_width) / 2))
        draw_plot_image.paste(w, title_paste_pos, w)
        # candle width
        candle_width_right_padding = 2
        candle_width_width, candle_width_height = draw_plot_image.textsize(chartdata.candle_width, self.display.medium_font)
        draw_plot_image.text((self.display.WIDTH-candle_width_width, candle_width_right_padding), chartdata.candle_width, 'red', self.display.medium_font)
        # draw % change text
        change = chartdata.percentage_change()
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0], selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)
        # draw current price text
        price = price_humaniser.format_title_price(chartdata.last_close())
        draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', self.display.price_font)
        # select some random comment depending on price action
        if random.random() < 0.5:
            direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
            messages=self.get_price_action_comments(direction)
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)

        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)

class chart_updater:
    def __init__(self, config, files):
        self.config = config
        self.files = files
        # select inky display or file output (nice for testing)
        self.display = kinky.inker(self.config) if self.config.use_inky() else kinky.disker()
        # initialise exchange
        self.exchange = chart_data_fetcher.Exchange(config)

    def run(self):
        # await internet connection
        wait_for_internet_connection(self.display)
        # fetch chart data
        chart_data = self.exchange.fetch_random()
        
        with io.BytesIO() as file_stream:
            # draw chart to image
            chart_image = cartographer(self.config, self.display, self.files).draw_chart(chart_data, file_stream)
            # draw overlay on image   
            overlaid_chart_image = ChartEditor(self.config, self.display).overlay_on(chart_image, chart_data)
            # display the image
            self.display.show(overlaid_chart_image)