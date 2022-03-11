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


def load_config():
    return load_config_ini(files)


class disks:
    disk_small = {'output': 'disk', 'resolution': "264,176"}
    disk_med = {'output': 'disk', 'resolution': "400,300"}
    disk_large = {'output': 'disk', 'resolution': "640,448"}
    all = [disk_small, disk_med, disk_large]


class screens:
    wave27b = {'output': 'waveshare.epd2in7b_V2'}
    inky = {'output': 'inky'}


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
]  # name, exch, token, stock, overlay, expand, volume, candle_width, holdings

os.makedirs('tests/images/', exist_ok=True)


class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict, output):
        def gen_test(file_name, test_name, exch, token, stock, overlay, expand, volume, candle_width, holdings):
            def test(self):
                config = load_config()
                image_file_path = f'tests/images/{file_name}.png'
                config.set('currency', 'stock_symbol', stock)
                config.set('currency', 'exchange', exch)
                config.set('currency', 'instrument', token)
                config.set('currency', 'holdings', holdings)
                config.set('currency', 'chart_since', '2021-08-22T00:00:00Z')
                config.set('display', 'output', output['output'])
                config.set('display', 'resolution', output.get('resolution', ''))
                config.set('display', 'overlay_layout', overlay)
                config.set('display', 'expanded_chart', expand)
                config.set('display', 'show_volume', volume)
                config.set('display', 'candle_width', candle_width)
                config.set('display', 'disk_file_name', image_file_path)
                config.set('display', 'rotation', '0')
                config.set('display', 'show_ip', 'false')
                config.set('display', 'timestamp', 'false')
                config.set('comments', 'up', 'moon')
                config.set('comments', 'down', 'doom')
                app = BitBot(config, files)

                image_should_not_change_when(app.display_chart, file_name, image_file_path)

                if config.shoud_show_image_in_vscode():
                    os.system(f"code '{image_file_path}'")

            def image_should_not_change_when(action, file_name, image_file_path):
                try:
                    previous_image = Image.open(image_file_path)
                except FileNotFoundError:
                    pass

                action()
                new_image = Image.open(image_file_path)
                diff = ImageChops.difference(new_image, previous_image)
                if diff.getbbox():
                    failure_file_path = f'tests/images/failed_{file_name}.png'
                    diff.save(failure_file_path)
                    if False:
                        os.system(f"code '{failure_file_path}'")
                    assert False, f"images differ '{failure_file_path}'"

            return test
        for test_param in test_params:
            test_name = f"test_{output.get('resolution', output['output'].split('.')[-1])}_{test_param[0]}"

            dict[test_name] = gen_test(test_name, *test_param)
        return type.__new__(mcs, name, bases, dict)


class SmallChartRenderingTests(unittest.TestCase, output=disks.disk_small, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class MediumChartRenderingTests(unittest.TestCase, output=disks.disk_med, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class LargeChartRenderingTests(unittest.TestCase, output=disks.disk_large, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs a waveshare display")
class Wave27bChartRenderingTests(unittest.TestCase, output=screens.wave27b, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


@unittest.skip("needs an inky display")
class InkyChartRenderingTests(unittest.TestCase, output=screens.inky, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta
