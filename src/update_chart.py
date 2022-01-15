from src import price_humaniser, currency_chart, kinky
from PIL import Image, ImageDraw
import io, random, socket, logging, time

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

# wait for network connection
def wait_for_internet_connection(display):
    logging.info('Await network')
    connection_error_shown = False
    while network_connected() == False:
        # draw error message if not already drawn
        if connection_error_shown == False:
            connection_error_shown = True
            display.draw_connection_error()
        time.sleep(10)

class bitbot:
    def __init__(self, config):
        self.config = config
        # select inky display or file output (nice for testing)
        self.display = kinky.inker(self.config) if self.use_inky() else kinky.disker()
        # initialise chart for current display/config
        self.chart = currency_chart.crypto_chart(self.config, self.display)

    def use_inky(self):
        return self.config["display"]["output"] == "inky"

    def get_price_action_comments(self, direction):
        return self.config.get('comments', direction).split(',')

    def configured_instrument(self):
        return self.config["currency"]["instrument"]

    def run(self):
        # check internet connection
        wait_for_internet_connection(self.display)

        # fetch the chart data
        chartdata = self.chart.createChart()

        with io.BytesIO() as file_stream:
            logging.info('Formatting chart for display')

            # write mathplot fig to stream and open as a PIL image
            chartdata.write_to_stream(file_stream)
            file_stream.seek(0)
            plot_image = Image.open(file_stream)
            
            # find some empty graph space to place our text
            title_positions = [(60, 5), (210, 5), (140, 5), (60, 200), (210, 200), (140, 200)] 
            selectedArea = least_intrusive_position(plot_image, title_positions)
            
            # handle for drawing on our chart image
            draw_plot_image = ImageDraw.Draw(plot_image)

            # draw instrument / candle width
            title = self.configured_instrument() + ' (' + chartdata.candle_width + ') '
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
                messages=self.get_price_action_comments(direction)
                draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)
            
            # add a border and show the image
            draw_plot_image.rectangle([(0, 0), (self.display.WIDTH -1, self.display.HEIGHT-1)], outline='red')
            self.display.show(plot_image) 
