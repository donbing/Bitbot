from PIL import Image, ImageChops, ImageOps
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.bitbot import BitBot
import os
import pathlib
import unittest

# check config files
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))


# physical screen renderers for approval testing
class screen_output_renderers:
    wave27b = {'output': 'waveshare.epd2in7b_V2'}
    inky = {'output': 'inky'}


# s/m/l image file renderers for automated testing
class disk_output_renderers:
    disk_small = {'output': 'disk', 'resolution': "264,176"}
    disk_med = {'output': 'disk', 'resolution': "400,300"}
    disk_large = {'output': 'disk', 'resolution': "640,448"}
    all = [disk_small, disk_med, disk_large]


# basic config
config_defaults = {
    'currency': {
        'stock_symbol': '',
        'exchange': 'bitmex',
        'instrument': 'BTC/USD',
        'holdings': '0',
        'chart_since': '2021-08-22T00:00:00Z',
        'entry_price': 0,
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
        'down': 'doom',
    }
}


# test-specific config
test_configs = {
    "APPLE 1mo defaults": {
        'currency': {'stock_symbol': 'AAPL'},
        'display': {'candle_width': '1mo'},
    },
    "APPLE 3mo defaults": {
        'currency': {'stock_symbol': 'AAPL'},
        'display': {'candle_width': '3mo'},
    },
    "GBPJPY 3mo defaults with entry": {
        'display': {'candle_width': '3mo'},
        'currency': {
            'stock_symbol': 'GBPJPY=X',
            'entry_price': '167',
            'chart_since': '2022-04-22T00:00:00Z', # yfinance limits to gathering 7 days of low-timeframe from the last 60 days
            'holdings': '10',
        },
        'display': {'candle_width': '5m', },
    },
    "AUDCAD 3mo defaults with entry": {
        'currency': {
            'stock_symbol': 'AUDCAD=X',
            'entry_price': '0.89332',
            'chart_since': '', # yfinance limits to gathering 7 days of low-timeframe from the last 60 days
            'holdings': '450000',
        },
        'display': {'candle_width': '1h', },
    },
    "bitmex BTC 5m defaults": {
        'display': {'candle_width': '5m'},
    },
    "bitmex BTC 1h defaults": {
        'display': {'candle_width': '1h'},
    },
    "bitmex BTC 1d defaults": {
        'display': {'candle_width': '1d'},
    },
    "BTC HOLDINGS": {
        'currency': {'holdings': "100"},
    },
    "BTC VOLUME": {
        'display': {'show_volume': 'true'},
    },
    "BTC EXPANDED": {
        'display': {'expanded_chart': 'true'},
    },
    "BTC VOLUME EXPANDED": {
        'display': {'show_volume': 'true', 'expanded_chart': 'true'},
    },
    "BTC VOLUME OVERLAY2": {
        'display': {'overlay_layout': '2', 'show_volume': 'true'},
    },
    "BTC OVERLAY2": {
        'display': {'overlay_layout': '2'},
    },
    "bitmex ETH 5m defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '5m'},
    },
    "bitmex ETH 1h defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '1h'},
    },
    "bitmex ETH 1d defaults": {
        'currency': {'instrument': 'ETH/USD'},
        'display': {'candle_width': '1d'},
    },
    "cryptocom CRO 5m defaults": {
        'currency': {'instrument': 'CRO/USDC', 'exchange': 'cryptocom'},
        'display': {'candle_width': '5m'},
    },
    "cryptocom CRO 1h defaults": {
        'currency': {'instrument': 'CRO/USDC', 'exchange': 'cryptocom'},
        'display': {'candle_width': '1h'},
    },
    "cryptocom CRO 1d defaults": {
        'currency': {'instrument': 'CRO/USDC', 'exchange': 'cryptocom'},
        'display': {'candle_width': '1d'},
    },
}

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

                previous_image = None  # Image.open(file_name)
                app.display_chart()
                new_image = Image.open(file_name)

                assert_image_matches_size(new_image, output.get('resolution', ''))
                # assert_image_unchanged(previous_image, new_image, file_name)

            def assert_image_matches_size(new_image):
                expected_res = output.get('resolution', '')
                actual_res = f"{new_image.width},{new_image.height}"
                assert expected_res == actual_res, f"exp {expected_res}, act {actual_res}"

            def assert_image_unchanged(previous_image, new_image, file_name):
                diff = ImageChops.difference(new_image, previous_image)
                if diff.getbbox():
                    diff_file_path = f'tests/images/failed_{name}.png'
                    diff.save(diff_file_path)
                    assert False, f"{file_name} images differ, see '{diff_file_path}'"

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
