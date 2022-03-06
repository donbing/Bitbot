
from datetime import datetime
from PIL import ImageDraw
from src.configuration.log_decorator import info_log
from src.drawing.image_utils import Align
from src.drawing.image_utils import DrawText, RotatedTextBlock
from src.drawing.image_utils import TextBlock, Border
from src.configuration.network_utils import get_ip


class ChartOverlay():
    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data
        self.title_font = self.display.title_font
        self.price_font = self.display.price_font
        self.medium_font = self.display.medium_font
        self.tiny_font = self.display.tiny_font

    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing on top of our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🖊️ draw each of the configured display elements
        for elem in self.display_elements():
            elem.draw_on(draw_plot_image)

    def display_elements(self):
        # 🕒 add the time if configured
        if self.config.show_timestamp() == 'true':
            yield DrawText(self.format_time(), self.tiny_font, align=Align.BottomRight)
        # 📡 add the ip address if configured
        if self.config.show_ip() == 'true':
            yield DrawText(get_ip(), self.tiny_font, align=Align.BottomLeft)
        # 🔲 add a border if configured
        yield Border(self.config.border_type())
        # 🖊️ add configured overlay
        if self.config.overlay_type() == "2":
            for element in self.overlay2(self.chart_data):
                yield element
        if self.config.overlay_type() == "1":
            for element in self.overlay1(self.chart_data):
                yield element

    def overlay1(self, chartdata):
        portfolio_value = self.value_held(chartdata)
        yield TextBlock([
            [
                # 🎹 draw instrument name and candle width text
                DrawText(f'{chartdata.instrument} ({chartdata.candle_width}) ', self.title_font),
                # ➗ draw coloured change percentage
                DrawText.percentage(chartdata.percentage_change(), self.title_font),
            ],
            # 🐘 large font price text
            [DrawText.humanised_price(chartdata.last_close(), self.price_font)],
            # 💬 draw holdings or comment
            [DrawText.number(portfolio_value, self.title_font)
                if portfolio_value
                else DrawText.random_from_bool(self.ai_comments(), self.price_increasing(chartdata), self.title_font)]
        ], align=Align.LeastIntrusive)

    def overlay2(self, chartdata):
        portfolio_value = self.value_held(chartdata)
        # 🏳️ title block
        yield TextBlock([
            # ➗ draw coloured change percentage
            [DrawText.percentage(chartdata.percentage_change(), self.title_font)],
            # 🐘 large font price text
            [DrawText.humanised_price(chartdata.last_close(), self.price_font)],
            # 💬 draw holdings or comment
            [DrawText.number(portfolio_value, self.title_font)
                if portfolio_value
                else DrawText.random_from_bool(self.ai_comments(), self.price_increasing(chartdata), self.title_font)]
        ], align=Align.LeastIntrusive)
        # 🎹 draw instrument name
        yield RotatedTextBlock(chartdata.instrument, self.medium_font)
        # 🕎 candle width
        yield DrawText(chartdata.candle_width, self.medium_font, colour='red', align=Align.TopRight)

    def price_increasing(self, chartdata):
        return chartdata.start_price() < chartdata.last_close()

    def format_time(self):
        return datetime.now().strftime("%b %-d %-H:%M")

    def ai_comments(self):
        return self.config.get_price_action_comments()

    def value_held(self, market):
        return self.config.portfolio_size() * market.last_close()

    def __repr__(self):
        return f'<Overlay: {self.config.overlay_type()}>'
