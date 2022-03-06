import unittest
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.bitbot import BitBot
import os
import pathlib

from src.drawing.image_utils import DrawText, TextBlock

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))


def load_config():
    config = load_config_ini(files)
    config.set('display', 'output', 'waveshare.epd2in7b_V2')
    return config


# name, exch, token, stock, overlay, expand, volume, candle_width, holdings
# load config
test_params = [
    ("APPLE 1mo defaults", "", "", "AAPL", "1", "false", "false", "1mo", ""),
    ("APPLE 3mo defaults", "", "", "AAPL", "1", "false", "false", "3mo", ""),

    ("bitmex BTC 5m defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "5m", ""),
    ("bitmex BTC 1h defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "1h", ""),
    ("bitmex BTC 1d defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "1d", ""),

    ("BTC HOLDINGS", "bitmex", "BTC/USD", "", "1", "false", "false", "1d", "100"),
    ("BTC VOLUME", "bitmex", "BTC/USD", "", "1", "false", "true", "1d", ""),
    ("BTC EXPANDED", "bitmex", "BTC/USD", "", "1", "true", "false", "1d", ""),
    ("BTC VOLUME EXPANDED", "bitmex", "BTC/USD", "", "1", "true", "true", "1d", ""),
    ("BTC VOLUME OVERLAY2", "bitmex", "BTC/USD", "", "2", "false", "true", "1d", ""),
    ("BTC OVERLAY2", "bitmex", "BTC/USD", "", "2", "false", "false", "1d", ""),

    ("bitmex ETH 5m defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "5m", ""),
    ("bitmex ETH 1h defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "1h", ""),
    ("bitmex ETH 1d defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "1d", ""),

    ("cryptocom CRO 5m defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "5m", ""),
    ("cryptocom CRO 1h defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "1h", ""),
    ("cryptocom CRO 1d defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "1d", ""),
]

os.makedirs('tests/images/', exist_ok=True)


class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test(name, exch, token, stock, overlay, expand, volume, candle_width, holdings):
            def test(self):
                config = load_config()
                image_file_name = f'tests/images/{name}.png'
                config.set('currency', 'stock_symbol', stock)
                config.set('currency', 'exchange', exch)
                config.set('currency', 'instrument', token)
                config.set('currency', 'holdings', holdings)
                config.set('currency', 'chart_since', '2021-08-22T00:00:00Z')
                config.set('display', 'overlay_layout', overlay)
                config.set('display', 'expanded_chart', 'true')
                config.set('display', 'show_volume', 'false')
                config.set('display', 'candle_width', candle_width)
                config.set('display', 'disk_file_name', image_file_name)
                config.set('display', 'rotation', '90')
                config.set('display', 'show_ip', 'false')
                config.set('display', 'timestamp', 'false')
                app = BitBot(config, files)
                app.display_chart()
                # os.system(f"code '{image_file_name}'")
            return test

        for test_param in test_params:
            test_name = "test_%s" % test_param[0]
            dict[test_name] = gen_test(*test_param)
        return type.__new__(mcs, name, bases, dict)


class ChartRenderingTests(unittest.TestCase, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta

from PIL import ImageFont, Image, ImageDraw
transparent = (0, 0, 0, 0)
white = (255,255,255)


class TestTextBlocks(unittest.TestCase):
    fontPath = str(files.resource_folder) + '/04B_03__.TTF'
    title_font = ImageFont.truetype(fontPath, 16)
    price_font = ImageFont.truetype(fontPath, 32)

    def test_text_block(self):
        lines = [
            [
                DrawText('balls' + ' (' + 'arse' + ') ', self.title_font, colour=white),
                DrawText.percentage(-50, self.title_font),
            ],
            [
                DrawText("48,000", self.price_font),
            ],
        ]
        
        block = TextBlock(lines)
        image = Image.new('RGBA', block.size(), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        block.draw_on(draw)
        image_file_name = "arse.png"
        image.save(image_file_name)
        # os.system(f"code '{image_file_name}'")
