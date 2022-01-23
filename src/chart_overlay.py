from datetime import datetime
from PIL import Image, ImageDraw
import random
from src import price_humaniser
from src.log_decorator import info_log

class ChartOverlay():

    # 🏳️ select image area with the most white pixels
    @staticmethod
    def least_intrusive_position(img, possibleTextPositions):
        # 🔢 count the white pixels in an area of the image
        def count_white_pixels(x, y, n, image):
            count = 0
            for s in range(x, x+(n*3)+1):
                for t in range(y, y+n+1):
                    pix = image.getpixel((s, t))
                    count += 1 if pix == (255,255,255) else 0
            return count

        rgb_im = img.convert('RGB')
        height_of_section = 60
        ordredByAveColour = sorted(possibleTextPositions, key=lambda item: (count_white_pixels(*item, height_of_section, rgb_im), item[0]))
        return ordredByAveColour[-1]

    def flatten(t):
        return [item for sublist in t for item in sublist]

    possible_title_positions = flatten(map(lambda y: map(lambda x: (x, y), range(60, 200, 10)), [6, 200]))
    
    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data
    
    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing over our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🏳️ find some empty space in the image to place our text
        selectedArea = ChartOverlay.least_intrusive_position(chart_image, self.possible_title_positions)
        # 🖊️ draw configured overlay
        if self.config.overlay_type() == "2":
            self.draw_overlay2(draw_plot_image, self.chart_data, selectedArea)
        else:
            self.draw_overlay1(draw_plot_image, self.chart_data, selectedArea)

    # 🕒 add the time if configured
    def draw_current_time(self, draw_plot_image):
        if self.config.show_timestamp() == 'true':
            formatted_time = datetime.now().strftime("%b %-d %-H:%M")
            text_width, text_height = draw_plot_image.textsize(formatted_time, self.display.tiny_font)
            draw_plot_image.text((self.display.WIDTH - text_width - 1, self.display.HEIGHT - text_height - 2), formatted_time, 'black', self.display.tiny_font)

    # 🔲 add a border if configured
    def draw_border(self, draw_plot_image):
        border_type = self.config.border_type()
        if border_type != 'none':
            draw_plot_image.rectangle([(0, 0), (self.display.WIDTH -1, self.display.HEIGHT-1)], outline=border_type)

    def draw_overlay1(self, draw_plot_image, chartdata, selectedArea):
        # 🎹 🕎 draw instrument / candle width
        title = chartdata.instrument + ' (' + chartdata.candle_width + ') '
        draw_plot_image.text(selectedArea, title, 'black', self.display.title_font)
        # 🖊️ draw % change text
        title_width, title_height = draw_plot_image.textsize(title, self.display.title_font)
        change = ((chartdata.last_close() - chartdata.start_price()) / chartdata.last_close())*100
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0]+title_width, selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)
        # 🖊️ draw current price text
        price = price_humaniser.format_title_price(chartdata.last_close())
        draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', self.display.price_font)
        # 💬 select some random comment depending on price action
        if random.random() < 0.5:
            direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
            messages=self.config.get_price_action_comments(direction)
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)
        
        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)

    def draw_overlay2(self, draw_plot_image, chartdata, selectedArea):
        # 🎹 draw instrument name
        title = chartdata.instrument
        title_width, title_height = draw_plot_image.textsize(title, self.display.medium_font)
        txt=Image.new('RGBA', (title_width, title_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), title, 'black', self.display.medium_font)
        w=txt.rotate(270, expand=True)
        title_paste_pos = (self.display.WIDTH-title_height - 2, int((self.display.HEIGHT - title_width) / 2))
        draw_plot_image.paste(w, title_paste_pos, w)
        # 🕎 candle width
        candle_width_right_padding = 2
        candle_width_width, candle_width_height = draw_plot_image.textsize(chartdata.candle_width, self.display.medium_font)
        draw_plot_image.text((self.display.WIDTH-candle_width_width, candle_width_right_padding), chartdata.candle_width, 'red', self.display.medium_font)
        # 🖊️ draw % change text
        change = chartdata.percentage_change()
        change_colour = ('red' if change < 0 else 'black')
        draw_plot_image.text((selectedArea[0], selectedArea[1]), '{:+.2f}'.format(change) + '%', change_colour, self.display.title_font)
        # 🖊️ draw current price text
        price = price_humaniser.format_title_price(chartdata.last_close())
        draw_plot_image.text((selectedArea[0], selectedArea[1]+11), price, 'black', self.display.price_font)
        # 💬 select some random comment depending on price action
        if random.random() < 0.5:
            direction = 'up' if chartdata.start_price() < chartdata.last_close() else 'down'
            messages=self.get_price_action_comments(direction)
            draw_plot_image.text((selectedArea[0], selectedArea[1]+52), random.choice(messages), 'red', self.display.title_font)

        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)
