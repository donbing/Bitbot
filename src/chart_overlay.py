import socket
import random
from datetime import datetime
from PIL import Image, ImageDraw
from src import price_humaniser
from src.configuration.log_decorator import info_log


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


class ChartOverlay():

    # 🏳️ select image area with the most white pixels
    @staticmethod
    def least_intrusive_position(img, possibleTextPositions):
        # 🔢 count the white pixels in an area of the image
        def count_white_pixels(x, y, height, width, image):
            count = 0
            print("width:" + str((width,height)))
            x_range = range(x, x + width)
            print("x:" + str(x_range))
            y_range = range(y, y + height)
            print("y:" + str(x_range))
            for x in x_range:
                for y in y_range:
                    pix = image.getpixel((x, y))
                    count += 1 if pix == (255, 255, 255) else 0
            return count

        rgb_im = img.convert('RGB')
        height_of_section = 60
        width_of_section = 60
        ordredByAveColour = sorted(
            possibleTextPositions,
            key=lambda item: (
                count_white_pixels(item[0], item[1], height_of_section, width_of_section, rgb_im),
                item[0])
            )

        return ordredByAveColour[-1]

    def flatten(t):
        return [item for sublist in t for item in sublist]

    def possible_title_positions(self):
        x_range = range(60, self.display.WIDTH - 70, 10)
        y_range = [6, self.display.HEIGHT // 2 , self.display.HEIGHT - 80]
        return ChartOverlay.flatten(
            map(lambda y: 
                map(lambda x: (x, y), x_range), y_range))

    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data

    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing over our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🏳️ find some empty space in the image to place our text
        selectedArea = ChartOverlay.least_intrusive_position(chart_image, self.possible_title_positions())
        # 🖊️ draw configured overlay
        if self.config.overlay_type() == "2":
            self.draw_overlay2(draw_plot_image, self.chart_data, selectedArea, chart_image)
        else:
            self.draw_overlay1(draw_plot_image, self.chart_data, selectedArea, chart_image)

    # 🕒 add the time if configured
    def draw_current_time(self, draw_plot_image):
        if self.config.show_timestamp() == 'true':
            formatted_time = datetime.now().strftime("%b %-d %-H:%M")
            text_width, text_height = draw_plot_image.textsize(formatted_time, self.display.tiny_font)
            draw_plot_image.text(
                (self.display.WIDTH - text_width - 1, self.display.HEIGHT - text_height - 2),
                formatted_time,
                'black',
                self.display.tiny_font)

    # 🕒 add the ip address if configured
    def draw_ip(self, draw):
        if self.config.show_ip() == 'true':
            ip = get_ip()
            text_width, text_height = draw.textsize(ip, self.display.tiny_font)
            draw.text(
                (1, self.display.HEIGHT - text_height - 2),
                ip,
                'black',
                self.display.tiny_font)

    # 🔲 add a border if configured
    def draw_border(self, draw_plot_image):
        border_type = self.config.border_type()
        if border_type != 'none':
            draw_plot_image.rectangle(
                [(0, 0), (self.display.WIDTH - 1, self.display.HEIGHT - 1)],
                outline=border_type)

    # 💬 draw a random comment depending on price action
    def draw_price_comment(self, draw_plot_image, chartdata, selectedArea):
        if self.config.portfolio_size():
            messages = "{:,}".format(self.config.portfolio_size() * chartdata.last_close())
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), messages, 'black', self.display.title_font)
        elif random.random() < 0.5:
            direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
            messages = self.config.get_price_action_comments(direction)
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)

    # 🖊️ draw current price text
    def draw_current_price(self, draw_plot_image, chartdata, selectedArea):
        price = price_humaniser.format_title_price(chartdata.last_close())
        draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', self.display.price_font)

    def draw_overlay1(self, draw_plot_image, chartdata, selectedArea, base_plot_image):
        # 🎹 🕎 draw instrument / candle width
        title = chartdata.instrument + ' (' + chartdata.candle_width + ') '
        draw_plot_image.text(selectedArea, title, 'black', self.display.title_font)
        # 🖊️ draw % change text
        title_width, title_height = draw_plot_image.textsize(title, self.display.title_font)
        change = ((chartdata.last_close() - chartdata.start_price()) / chartdata.last_close())*100
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0]+title_width, selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)

        self.draw_current_price(draw_plot_image, chartdata, selectedArea)
        self.draw_price_comment(draw_plot_image, chartdata, selectedArea)
        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)
        self.draw_ip(draw_plot_image)

    def draw_overlay2(self, draw_plot_image, chartdata, selectedArea, base_plot_image):
        # 🎹 draw instrument name
        title = chartdata.instrument
        title_width, title_height = draw_plot_image.textsize(title, self.display.medium_font)
        txt = Image.new('RGBA', (title_width, title_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), title, 'black', self.display.medium_font)
        w = txt.rotate(270, expand=True)
        title_paste_pos = (self.display.WIDTH-title_height - 2, int((self.display.HEIGHT - title_width) / 2))
        base_plot_image.paste(w, title_paste_pos, w)
        # 🕎 candle width
        candle_width_right_padding = 2
        candle_width_width, candle_width_height = draw_plot_image.textsize(chartdata.candle_width, self.display.medium_font)
        draw_plot_image.text((self.display.WIDTH-candle_width_width, candle_width_right_padding), chartdata.candle_width, 'red', self.display.medium_font)
        # 🖊️ draw % change text
        change = chartdata.percentage_change()
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0], selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)

        self.draw_current_price(draw_plot_image, chartdata, selectedArea)
        self.draw_price_comment(draw_plot_image, chartdata, selectedArea)
        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)
        self.draw_ip(draw_plot_image)

    def __repr__(self):
        return f'<Overlay: {self.config.overlay_type()}>'
