import random
from datetime import datetime
from PIL import ImageDraw
from src.drawing import price_humaniser
from src.configuration.log_decorator import info_log
from src.drawing.image_utils import bottom_right_text, bottom_left_text, top_right_text
from src.drawing.image_utils import border, rotated_center_right_text, DrawText
from src.drawing.image_utils import TextBlock, least_intrusive_position
from src.configuration.network_utils import get_ip


class ChartOverlay():

    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data

    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing on top of our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🖊️ draw configured overlay
        if self.config.overlay_type() == "2":
            self.draw_overlay2(draw_plot_image, self.chart_data)
        else:
            self.draw_overlay1(draw_plot_image, self.chart_data)

        self.draw_border(draw_plot_image)
        self.draw_current_time(draw_plot_image)
        self.draw_ip(draw_plot_image)

    def draw_overlay1(self, image_draw, chartdata):
        title_font = self.display.title_font
        price_font = self.display.price_font
        tb = TextBlock([
            [
                self.instrument_and_timeframe(chartdata, title_font),
                self.percentage_change(chartdata, title_font),
            ],
            [self.current_price(chartdata, price_font)],
            [self.draw_price_comment(chartdata, self.config, title_font)],
        ])
        # 🏳️ find some empty space in the image and place our title block
        selectedArea = least_intrusive_position(image_draw.im, tb)
        tb.draw_on(image_draw, selectedArea)

    def draw_overlay2(self, image_draw, chartdata):
        title_font = self.display.title_font
        price_font = self.display.price_font
        medium_font = self.display.medium_font
        tb = TextBlock([
            [self.percentage_change(chartdata, title_font)],
            [self.current_price(chartdata, price_font)],
            [self.draw_price_comment(chartdata, self.config, title_font)],
        ])
        # 🏳️ find some empty space in the image and place our title block
        selectedArea = least_intrusive_position(image_draw.im, tb)
        tb.draw_on(image_draw, selectedArea)
        # 🎹 draw instrument name
        rotated_center_right_text(image_draw, chartdata.instrument, medium_font)
        # 🕎 candle width
        top_right_text(image_draw, chartdata.candle_width, medium_font)

    # 🕒 add the time if configured
    def draw_current_time(self, draw_plot_image):
        if self.config.show_timestamp() == 'true':
            bottom_right_text(
                draw_plot_image,
                datetime.now().strftime("%b %-d %-H:%M"),
                self.display.tiny_font)

    # 📡 add the ip address if configured
    def draw_ip(self, draw):
        if self.config.show_ip() == 'true':
            bottom_left_text(draw, get_ip(), self.display.tiny_font)

    # 🔲 add a border if configured
    def draw_border(self, draw_plot_image):
        border_type = self.config.border_type()
        if border_type != 'none':
            border(draw_plot_image, border_type)

    # 💬 draw a random comment depending on price action
    def draw_price_comment(self, chartdata, config, font):
        if config.portfolio_size():
            portfolio_value = config.portfolio_size() * chartdata.last_close()
            formatted_value = "{:,}".format(portfolio_value)
            return DrawText(formatted_value, font, 'black')
        else:
            trending_up = chartdata.start_price() < chartdata.last_close()
            direction = 'up' if trending_up else 'down'
            trend_comments = config.get_price_action_comments(direction)
            comments = random.choice(trend_comments)
            return DrawText(comments, font, 'red')

    # 🎹 draw instrument name and cangle width text
    def instrument_and_timeframe(self, chartdata, font):
        text = chartdata.instrument + ' (' + chartdata.candle_width + ') '
        return DrawText(text, font)

    # 🔀 draw percentage change text
    def percentage_change(self, chartdata, font):
        percentage = chartdata.percentage_change()
        return DrawText.percentage(percentage, font)

    # 🖊️ draw current price text
    def current_price(self, chartdata, font):
        last_close = chartdata.last_close()
        himanised_price = price_humaniser.format_title_price(last_close)
        return DrawText(himanised_price, font)

    def __repr__(self):
        return f'<Overlay: {self.config.overlay_type()}>'
