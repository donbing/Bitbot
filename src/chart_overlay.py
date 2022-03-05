import socket
import random
from datetime import datetime
from PIL import ImageDraw
from src import price_humaniser
from src.configuration.log_decorator import info_log
from src.image_utils import bottom_right_text, bottom_left_text, top_right_text, border, rotated_center_right_text, DrawText, TextBlock, least_intrusive_position


padding = 2


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

    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data

    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing over our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🖊️ draw configured overlay
        if self.config.overlay_type() == "2":
            self.draw_overlay2(draw_plot_image, self.chart_data)
        else:
            self.draw_overlay1(draw_plot_image, self.chart_data)

    # 🕒 add the time if configured
    def draw_current_time(self, draw_plot_image):
        if self.config.show_timestamp() == 'true':
            bottom_right_text(
                draw_plot_image,
                datetime.now().strftime("%b %-d %-H:%M"),
                self.display.tiny_font)

    # 🕒 add the ip address if configured
    def draw_ip(self, draw):
        if self.config.show_ip() == 'true':
            bottom_left_text(draw, get_ip(), self.display.tiny_font)

    # 🔲 add a border if configured
    def draw_border(self, draw_plot_image):
        border_type = self.config.border_type()
        if border_type != 'none':
            border(draw_plot_image, border_type)

    # 💬 draw a random comment depending on price action
    def draw_price_comment(self, chartdata, config):
        if config.portfolio_size():
            portfolio_value = config.portfolio_size() * chartdata.last_close()
            formatted_value = "{:,}".format(portfolio_value)
            return DrawText(formatted_value, self.display.title_font, 'black')
        else:
            trending_up = chartdata.start_price() < chartdata.last_close()
            direction = 'up' if trending_up else 'down'
            trend_comments = config.get_price_action_comments(direction)
            comments = random.choice(trend_comments)
            return DrawText(comments, self.display.title_font, 'red')

    # 🎹 draw instrument name and cangle width text
    def instrument_and_timeframe(self, chartdata):
        text = chartdata.instrument + ' (' + chartdata.candle_width + ') '
        return DrawText(text, self.display.title_font)

    # 🎹 draw percentage change text
    def percentage_change(self, chartdata):
        return DrawText.percentage(chartdata.percentage_change(), self.display.title_font)

    # 🖊️ draw current price text
    def current_price(self, chartdata):
        return DrawText(price_humaniser.format_title_price(chartdata.last_close()), self.display.price_font)

    def draw_overlay1(self, image_draw, chartdata):
        tb = TextBlock([
            [
                self.instrument_and_timeframe(chartdata),
                self.percentage_change(chartdata),
            ],
            [self.current_price(chartdata)],
            [self.draw_price_comment(chartdata, self.config)],
        ])

        # 🏳️ find some empty space in the image and place our title block
        selectedArea = least_intrusive_position(image_draw.im, tb)
        tb.draw_on(image_draw, selectedArea)

        self.draw_border(image_draw)
        self.draw_current_time(image_draw)
        self.draw_ip(image_draw)

    def draw_overlay2(self, image_draw, chartdata):
        tb = TextBlock([
            [self.percentage_change(chartdata)],
            [self.current_price(chartdata)],
            [self.draw_price_comment(chartdata, self.config)],
        ])

        # 🏳️ find some empty space in the image and place our title block
        selectedArea = least_intrusive_position(image_draw.im, tb)
        tb.draw_on(image_draw, selectedArea)

        # 🎹 draw instrument name
        rotated_center_right_text(image_draw, chartdata.instrument, self.display.medium_font)
        # 🕎 candle width
        top_right_text(image_draw, chartdata.candle_width, self.display.medium_font)

        self.draw_border(image_draw)
        self.draw_current_time(image_draw)
        self.draw_ip(image_draw)

    def __repr__(self):
        return f'<Overlay: {self.config.overlay_type()}>'
