from PIL import Image, ImageChops
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.bitbot import BitBot
import os
import pathlib
import unittest

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))


class screen_output_renderers:
    wave27b = {'output': 'waveshare.epd2in7b_V2'}
    inky = {'output': 'inky'}


class disk_output_renderers:
    disk_small = {'output': 'disk', 'resolution': "264,176"}
    disk_med = {'output': 'disk', 'resolution': "400,300"}
    disk_large = {'output': 'disk', 'resolution': "640,448"}
    all = [disk_small, disk_med, disk_large]


config_defaults = {
    'currency': {
        'stock_symbol': '',
        'exchange': 'bitmex',
        'instrument': 'BTC/USD',
        'holdings': '0',
        'chart_since': '2021-08-22T00:00:00Z'
    },
    'display': {
        'output': 'disk',
        'resolution': '400x300',
        'overlay_layout': '1',
        'expanded_chart': 'false',
        'show_volume': 'falsae',
        'candle_width': '1h',
        'rotation': '0',
        'show_ip': 'false',
        'timestamp': 'false',
    },
    'comments': {
        'up': 'moon',
        'down': 'doom'
    }
}


# load config
test_params = [
    ("APPLE 1mo defaults", "", "", "AAPL", "1", "false", "false", "1mo", ""),
    ("APPLE 3mo defaults", "", "", "AAPL", "1", "false", "false", "3mo", ""),
    ("GBPJPY 1mo defaults", "", "", "GBPJPY=X", "1", "false", "false", "1mo", ""),

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
]  # name, exch, token, stock, overlay, expand, volume, candle_width, holdings

os.makedirs('tests/images/', exist_ok=True)


class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict, output):
        def gen_test(name, custom_config):
            def test(self):
                config = load_config()
                image_file_name = f'tests/images/{name}.png'
                config.set('currency', 'stock_symbol', stock)
                config.set('currency', 'exchange', exch)
                config.set('currency', 'instrument', token)
                config.set('currency', 'holdings', holdings)
                config.set('currency', 'chart_since', '2021-08-22T00:00:00Z')
                config.set('display', 'output', output['output'])
                config.set('display', 'resolution', output.get('resolution', ''))

                image_file_name = f'tests/images/{name}.png'
                config.set('display', 'disk_file_name', image_file_name)

                app = BitBot(config, files)

                image_should_not_change_when(app.display_chart, image_file_name)

                if True:
                    os.system(f"code '{image_file_name}'")

            def image_should_not_change_when(action, file_name):
                previous_image = Image.open(file_name)
                action()
                new_image = Image.open(file_name)

                assert_image_matches_size(new_image)
                assert_image_unchanged(previous_image, new_image, file_name)

            def assert_image_matches_size(new_image):
                expected_res = output.get('resolution', '')
                actual_res = f"{new_image.width},{new_image.height}"
                assert expected_res == actual_res, f"expected {expected_res}, actual {actual_res}"

            def assert_image_unchanged(previous_image, new_image, file_name):
                diff = ImageChops.difference(new_image, previous_image)
                if diff.getbbox():
                    diff.save(file_name)
                    assert False, f"images differ '{file_name}'"

            return test

        for test_key in test_configs:
            output_res = output['output'].split('.')[-1]
            screen_res = output.get('resolution', output_res)
            test_name = f"test_{screen_res}_{test_key}"
            dict[test_name] = gen_test(test_name, test_configs[test_key])

        return type.__new__(mcs, name, bases, dict)


class SmallChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_small, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class MediumChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_med, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class LargeChartRenderingTests(unittest.TestCase, output=disk_output_renderers.disk_large, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs a waveshare display")
class Wave27bChartRenderingTests(unittest.TestCase, output=screen_output_renderers.wave27b, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs an inky display")
class InkyChartRenderingTests(unittest.TestCase, output=screen_output_renderers.inky, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta
